from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.db import connection, IntegrityError
from .models import Project, TempLoad, Phase, Tn, Tp, outcome_reason_action
from .forms import TemploadForm, KpiListForm, ProjectForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def loginUser(request):
    if request.user.is_authenticated:
        return redirect('prj-list')

    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'Username does not exist')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('prj-list')
        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'login_register.html')

def logoutUser(request):
    logout(request)
    messages.error(request, 'User was logged out!')
    return redirect('login')

def PrjListView(request):
    user_connected = request.user.username
    listprj = Project.objects.filter(username=user_connected)
    noproject = 1 if len(listprj) == 0 else 0
    if (not user_connected) or (user_connected is None):
        messages.error(request, 'Log in to see or create projects')
    return render(request, "prjlist.html", {"listprj": listprj,"noproject":noproject})

@login_required(login_url="login")
def createPrjView(request):
    form = ProjectForm()

    if request.method == 'POST':
        # print (request.POST)
        form = ProjectForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.username = request.user
            instance.save()
            project_id = instance.project_id
            # Below procedure: create records in database table 'phase' for this new project_id
            procedure_name = 'upd_phase_prc'
            argument = project_id
            sql = f"CALL {procedure_name}('{argument}')"
            with connection.cursor() as c:
                c.execute(sql)
            c.close()
            return redirect('prj-list')

    context = {'form': form}
    return render(request, "prjform.html", context)

def TemploadListView(request, id):
    # List below has elements (project_id and username) and is used to filter the following query
    placeholders_lst = [id,str(request.user)]
    with connection.cursor() as cursor:
        cursor.execute('SELECT ph.phase_name, tl.task_name, tl.startdate, tl.enddate\
                                     , tl.budget ,tl.startdate_is, tl.enddate_is, tl.budget_is, tl.temp_load_id, tl.project_id \
                                FROM (SELECT * FROM temp_load WHERE project_id = %s AND username = %s) tl\
                                JOIN (SELECT * FROM phase) ph\
        						ON tl.phase_id = ph.phase_id ORDER by tl.temp_load_id', placeholders_lst)

        # cursor.execute('SELECT ph.phase_name, tl.task_name, tl.startdate, tl.enddate\
        #                      , tl.budget ,tl.startdate_is, tl.enddate_is, tl.budget_is, tl.temp_load_id, ph.project_id \
        #                 FROM temp_load tl\
        #                 JOIN (SELECT * FROM phase WHERE project_id = %s) ph\
		# 				ON tl.phase_id = ph.phase_id', [id])

        data = cursor.fetchall()
        # Below some prints for test (data[-1] is last record, data[-1][0] is 1st column of last record)
        # print(type(data)) # print(data[-1]) # print(data[-1][0])
        notask = 1 if len(data) == 0 else 0
        if notask == 1:
            messages.error(request, 'Enter some data to make the KPI calculations')

        cursor.close()
        prj = get_object_or_404(Project, pk=id)
    return render(request, 'temploadlist.html', {'data': data, 'project_id': id, 'project_name': prj.project_name, 'notask': notask})

def KpiCalculation(request, project_id):
    # print("request.GET = ") # print(request.GET)
    form = KpiListForm()
    data = []
    stichtag = None
    pv, ev, ac, spi, cpi, bac, bac_minus_ac, tcpi, eac = 0, 0, 0, 0, 0, 0, 0, 0, 0
    scenario = None
    reason_action = []

    if request.method == 'POST':
        # print("request.POST = ") # print (request.POST)
        #
        with connection.cursor() as c:
            c.execute('CALL upd_tbls_prc();')
            c.close()

        stichtag = request.POST["stichtag"]
        placeholders_lst = [stichtag,project_id,str(request.user)]
        placeholders2_lst = [project_id,str(request.user)]

        try:
            with connection.cursor() as cursor:
                # Planned Value : pv
                cursor.execute('SELECT sum(vw.budget) as pv FROM (SELECT temp_load_id,project_id,budget FROM show_all WHERE enddate<=%s::date) vw\
                                JOIN (SELECT * FROM temp_load WHERE project_id = %s and username = %s) tl ON vw.temp_load_id = tl.temp_load_id'
                               , placeholders_lst)
                data = cursor.fetchall()
                pv = data[0][0]
                pv = 0 if (pv is None) else pv
                cursor.close()
        except:
            #return JsonResponse({"error": "Database connection error"}, status=500)
            return HttpResponse(status=500)

        with connection.cursor() as cursor:
            # Earned Value : ev
            cursor.execute('SELECT sum(vw.budget) as ev FROM (SELECT temp_load_id,project_id,budget FROM show_all WHERE enddate_is <=%s::date) vw\
                            JOIN (SELECT * FROM temp_load WHERE project_id = %s and username = %s) tl ON vw.temp_load_id = tl.temp_load_id'
                           , placeholders_lst)
            data = cursor.fetchall()
            ev = data[0][0]
            ev = 0 if (ev is None) else ev
            cursor.close()

        with connection.cursor() as cursor:
            # Actual Cost: ac
            cursor.execute('SELECT sum(vw.budget_is) as ac FROM (SELECT temp_load_id,project_id,budget_is FROM show_all WHERE enddate_is <=%s::date) vw\
                            JOIN (SELECT * FROM temp_load WHERE project_id = %s and username = %s) tl ON vw.temp_load_id = tl.temp_load_id'
                           , placeholders_lst)
            data = cursor.fetchall()
            ac = data[0][0]
            ac = 0 if (ac is None) else ac
            cursor.close()

        with connection.cursor() as cursor:
            # Budget at completion : bac
            cursor.execute('SELECT sum(vw.budget) as ac FROM (SELECT temp_load_id,project_id,budget FROM show_all) vw\
                            JOIN (SELECT * FROM temp_load WHERE project_id = %s and username = %s) tl ON vw.temp_load_id = tl.temp_load_id'
                           , placeholders2_lst)
            data = cursor.fetchall()
            bac = data[0][0]
            bac = 0 if (bac is None) else bac
            cursor.close()

            spi = round((ev / pv)*100,2) if not (pv == 0) else 0

            cpi = round((ev / ac)*100,2) if not (ac == 0) else 0

            bac_minus_ac = bac - ac

            tcpi = round((bac-ev)/bac_minus_ac*100,2) if not (bac_minus_ac == 0) else 0

            eac = round((bac / cpi)*100,2) if not (cpi == 0) else 0

            # schedule_variance
            if ev < pv:
                schedule_variance = 'Negativ'
            elif ev == pv:
                schedule_variance = 'Neutral'
            else:
                schedule_variance = 'Positiv'

            # cost_variance
            if ev < ac:
                cost_variance = 'Negativ'
            elif ev == ac:
                cost_variance = 'Neutral'
            else:
                cost_variance = 'Positiv'

            # For testing:
            # schedule_variance = 'Positiv'; cost_variance = 'Negativ'
            # schedule_variance = 'Positiv'; cost_variance = 'Neutral'
            # schedule_variance = 'Positiv'; cost_variance = 'Positiv'
            # schedule_variance = 'Neutral'; cost_variance = 'Negativ'
            # schedule_variance = 'Neutral'; cost_variance = 'Neutral'
            # schedule_variance = 'Neutral'; cost_variance = 'Positiv'
            # schedule_variance = 'Negativ'; cost_variance = 'Negativ'
            # schedule_variance = 'Negativ'; cost_variance = 'Neutral'
            # schedule_variance = 'Negativ'; cost_variance = 'Positiv'


            # Dictionary mapping tuples of conditions to outcome scenario
            # 1st condition is schedule_variance / 2nd condition is  cost_variance
            outcome_scenario = {
                ('Positiv', 'Negativ'): 1,
                ('Positiv', 'Neutral'): 2,
                ('Positiv', 'Positiv'): 3,
                ('Neutral', 'Negativ'): 4,
                ('Neutral', 'Neutral'): 5,
                ('Neutral', 'Positiv'): 6,
                ('Negativ', 'Negativ'): 7,
                ('Negativ', 'Neutral'): 8,
                ('Negativ', 'Positiv'): 9,
            }

            scenario = outcome_scenario.get((schedule_variance, cost_variance))

            # Variable outcome_reason_action gets loaded in file models.py
            reason_action = outcome_reason_action.get(scenario)

    try:
        prj = Project.objects.get(pk=project_id)
    except:
        #return JsonResponse({"error": "Database connection error"}, status=500)
        return HttpResponse(status=500)


    return render(request, 'kpilist.html', {'form': form,'st': stichtag,'pv': pv,'ev': ev,'ac': ac,'spi': spi,'cpi': cpi,'bac': bac,'tcpi': tcpi,'eac': eac,\
                                            'scenario': scenario, 'reason_action': reason_action, 'project_id': project_id,'project_name': prj.project_name})

@login_required(login_url="login")
def createTemploadView(request, project_id):
    filtered_choices = Phase.objects.filter(project_id=project_id).values_list('phase_id', 'phase_name')
    form = TemploadForm(filtered_choices=filtered_choices)

    if request.method == 'POST':
        # print (request.POST)
        form = TemploadForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.project_id = project_id
            instance.username = request.user
            instance.save()
            with connection.cursor() as c:
                c.execute('CALL upd_tbls_prc();')
            c.close()
            return redirect('tempload-list', project_id)

    prj = get_object_or_404(Project, pk=project_id)
    context = {'form': form, 'project_id': project_id, 'project_name': prj.project_name}
    return render(request, "temploadform.html", context)

@login_required(login_url="login")
def updateTemploadView(request, project_id, temp_load_id):
    temp_load = get_object_or_404(TempLoad, pk=temp_load_id)
    filtered_choices = Phase.objects.filter(project_id=project_id).values_list('phase_id', 'phase_name')
    form = TemploadForm(instance=temp_load,filtered_choices=filtered_choices)

    if request.method == 'POST':
        # print (request.POST)
        form = TemploadForm(request.POST, instance=temp_load)
        if form.is_valid():
            form.save()
            with connection.cursor() as c:
                c.execute('CALL upd_tbls_prc();')
            c.close()
            return redirect('tempload-list', project_id)

    prj = get_object_or_404(Project, pk=project_id)
    context = {'form': form, 'project_id': project_id, 'project_name': prj.project_name}
    return render(request, "temploadform.html", context)
@login_required(login_url="login")
def deleteTemploadView(request, project_id, temp_load_id):
    #temp_load = get_object_or_404(TempLoad, pk=temp_load_id)
    temp_load = TempLoad.objects.get(pk=temp_load_id)

    if request.method == 'POST':
        try:
            temp_load.delete()
        except IntegrityError:
            messages.error(request, 'Integrity Error: Deletion not possible')
        return redirect('tempload-list', project_id)

    prj = get_object_or_404(Project, pk=project_id)
    context = {'object': temp_load, 'project_id': project_id, 'project_name': prj.project_name}
    return render(request, "delete_template.html", context)

@login_required(login_url="login")
def singleTempLoadView(request, project_id, temp_load_id, phase_name):
    #temp_load = get_object_or_404(TempLoad, pk=temp_load_id)
    temp_load = TempLoad.objects.get(pk=temp_load_id)
    print(temp_load)
    phase_name = phase_name
    prj = get_object_or_404(Project, pk=project_id)
    context = {'phase_name': phase_name, 'temp_load': temp_load, 'project_id': project_id,'project_name': prj.project_name}
    return render(request, "singletempload.html", context)
