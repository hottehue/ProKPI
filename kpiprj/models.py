from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User

# Constant outcome_reason_action (used in Kpi calculation, should be later stored in a DB table)
OUTCOME_REASON_ACTION_DE = {
    1: ['Schneller als geplant, aber Mehrkosten', ['Team macht Überstunden', 'Zeit wird nicht effizient genutzt',\
                                       'Es wird zu viel Zeit für einzelne Aktivitäten verwendet', 'Zu viele Experten einem Task zugeordnet'],\
        ['Zeiterfassung überprüfen', 'Überstunden begrenzen',\
         'Anzahl Experten reduzieren', 'Zeitvorgaben straffen']],

    2: ['Schneller als geplant, aber keine Mehrkosten', ['Grundsätzlich positiv',\
        'Falls es Abhängigkeiten zwischen Aktivitäten gibt, besteht die Gefahr, dass Arbeiten begonnen werden,\
         die auf eine andere Aktivität hätten warten sollen'],\
        ['Abhängigkeiten überprüfen', 'Sicherstellen, dass die Experten an den richtigen Dingen arbeiten',\
         'Entschleunigen, nicht unnötig, Überstunden anfallen lassen']],

    3: ['Schneller als geplant, aber Minderkosten', ['Bei einem erfahrenen Team positiv, kann aber auch Symptom sein für:',\
        'Scope wird nicht richtig verstanden','Es wird «abgekürzt» und Aufgaben werden auf später verschoben'],\
        ['Sicherstellen, dass Aktivitäten wirklich abgeschlossen sind', 'Sicherstellen, dass der Scope klar definiert ist', \
         'Sicherstellen, dass die Experten an den vorgesehenen Aufgaben arbeiten und nicht einfache Aktivitäten vorziehen']],

    4: ['Im Plan, aber Mehrkosten', ['Ein unerfahrenes Team verbraucht zu viel Zeit',\
                                       'Der Terminplan ist zu grosszügig (Parkinsons Gesetz)'],\
        ['Überstunden überwachen und Effizienz erhöhen', 'Terminplanung straffen', 'Ausbildungsgrad durch Traninig oder Coaching erhöhen']],

    5: ['Voll im Plan', ['Die Performance ist nur so gut wie der Plan. Sind die Schätzungen korrekt und stimmt die Qualität der Lieferobjekte?',\
                                     'Wurde etwas übersehen?'],\
        ['Stichproben von Lieferobjekten erheben und Qualität und Vollständigkeit überprüfen']],

    6: ['Im Plan, aber Minderkosten', ['Ein erfahrenes Team arbeitet hocheffizient oder:',\
        'Experten brauchen weniger Zeit als geplant', 'Experten kürzen ab, um Termine einzuhalten'],\
        ['Lieferobjekte auf Qualität und Vollständigkeit überprüfen', 'Vollständigkeit der Zeiterfassung überprüfen', 'Überprüfen, ob das Team überqualifiziert ist']],

    7: ['Hinter Plan und Mehrkosten', ['Zu viele kleine Änderungen', 'Fehlende Erfahrung im Team',\
                                       'Unklarer Scope führt zu Doppelarbeiten', 'Zu viel Aufwand für Reviews'],\
        ['Meistbetroffene Aktivitäten überprüfen', 'Erfahrene Experten als Mentoren einsetzen',\
         'Sicherstellen, dass das Team den Scope versteht', 'Abnahmeregeln überprüfen']],

    8: ['Hinter Plan, aber keine Mehrkosten', ['Zu wenig Ressourcen','Experten brauchen weniger Zeit als geplant'],\
            ['Zusätzliche Ressourcen beantragen','Zeiterfassung überprüfen']],

    9: ['Hinter Plan und Minderkosten', ['Erfahrenes und effizientes Team', 'Experten arbeiten an einfachen Aufgaben zuerst',\
                                         'Ressourcen sind ausgefallen'],\
        ['Arbeitsaufteilung im Team überprüfen', 'Zusätzliche Ressourcen einsetzen']],
}

OUTCOME_REASON_ACTION_EN = {
    1: ['Faster than planned, but additional costs', ['Team works overtime', 'Time is not used efficiently',\
                                       'Too much time is spent on individual activities', 'Too many experts assigned to one task'],\
        ['Check time tracking', 'Limit overtime',\
         'Reduce number of experts', 'Tighten deadlines']],

    2: ['Faster than planned, but no additional costs', ['Basically positive',\
        'If there are dependencies between activities, there is a risk that work will be started,\
         that should have waited for another activity'],\
        ['Check dependencies', 'Ensure that the experts are working on the right things',\
         'Slow down, do not allow unnecessary overtime']],

    3: ['Faster than planned, but lower costs', ['Positive for an experienced team, but can also be a symptom of:',\
        'Scope is not properly understood','It is "cut short" and tasks are postponed to later'],\
        ['Ensure that activities are really completed', 'Ensure that the scope is clearly defined',\
         'Ensure that the experts work on the intended tasks and do not prioritise simple activities']],

    4: ['On schedule, but additional costs', ['An inexperienced team consumes too much time',\
                                       "The schedule is too generous (Parkinson's law)"],\
        ['Monitor overtime and increase efficiency', 'Streamline scheduling', 'Increase training level through traninig or coaching']],

    5: ['Fully on target', ['Performance is only as good as the plan. Are the estimates correct and is the quality of the deliverables right?',\
                                     'Has anything been overlooked?'],\
        ['Collect samples of delivery items and check quality and completeness']],

    6: ['On schedule, but lower costs', ['An experienced team works highly efficiently or:',\
        'Experts need less time than planned', 'Experts cut corners to meet deadlines'],\
        ['Check delivery objects for quality and completeness', 'Check completeness of time recording', 'Check whether the team is overqualified']],

    7: ['Behind schedule and additional costs', ['Too many small changes', 'Lack of experience in the team',\
                                       'Unclear scope leads to duplication of work', 'Too much effort for reviews'],\
        ['Review most affected activities', 'Use experienced experts as mentors',\
         'Ensure the team understands the scope', 'Review acceptance rules']],

    8: ['Behind schedule, but no additional costs', ['Too few resources','Experts need less time than planned'],\
            ['Request additional resources','Check time recording']],

    9: ['Behind schedule and under budget', ['Experienced and efficient team', 'Experts work on simple tasks first',\
                                         'Limited resource team availability?'],\
        ['Check work distribution in the team', 'Use additional resources']],
}

outcome_reason_action = OUTCOME_REASON_ACTION_EN

class Bf(models.Model):
    budgetfinish_id = models.AutoField(primary_key=True)
    task = models.OneToOneField('Tn', on_delete=models.CASCADE, blank=True, null=True)
    budget_is = models.IntegerField(blank=True, null=True)
    create_at = models.DateTimeField(db_column='create at', blank=True,
                                     null=True)  # Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'bf'


class Bp(models.Model):
    budgetplan_id = models.AutoField(primary_key=True)
    task = models.OneToOneField('Tn', on_delete=models.CASCADE, blank=True, null=True)
    budget = models.IntegerField(blank=True, null=True)
    create_at = models.DateTimeField(db_column='create at', blank=True,
                                     null=True)  # Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'bp'

class Phase_ref(models.Model):
    phase_ref_id = models.AutoField(primary_key=True)
    phase_ref_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'phase_ref'

    def __str__(self):
        return f"phase_ref_name= {self.phase_ref_name}"



class Phase(models.Model):
    phase_id = models.AutoField(primary_key=True)
    phase_name = models.CharField(max_length=255, blank=True, null=True)
    project = models.ForeignKey('Project', models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'phase'

    def __str__(self):
        return f"project= {self.project} , phase_name= {self.phase_name}"

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=150)
    to_delete = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'project'

    def get_absolute_url(self):
        return reverse("tempload-list", args=[self.project_id])

    def __str__(self):
        return f" id={self.project_id}, name= {self.project_name},\
         username= {self.username}, to_delete= {self.to_delete}"

class TempLoad(models.Model):
    temp_load_id = models.AutoField(primary_key=True)
    #phase_id = models.IntegerField(blank=True, null=True, choices=PHASE_CHOICES)
    phase_id = models.IntegerField(blank=True, null=True)
    task_name = models.CharField(max_length=255, blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    budget = models.IntegerField(blank=True, null=True)
    startdate_is = models.DateField(blank=True, null=True)
    enddate_is = models.DateField(blank=True, null=True)
    budget_is = models.IntegerField(blank=True, null=True)
    project_id = models.IntegerField()
    username = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'temp_load'

    def __str__(self):
        return self.task_name


class Tf(models.Model):
    tfinish_id = models.AutoField(primary_key=True)
    task = models.OneToOneField('Tn', on_delete=models.CASCADE, blank=True, null=True)
    startdate_is = models.DateField(blank=True, null=True)
    enddate_is = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tf'


class Tn(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=255)
    temp_load = models.OneToOneField(TempLoad, on_delete=models.CASCADE, blank=True, null=True)
    phase = models.ForeignKey(Phase, models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tn'

    def __str__(self):
        return self.task_name

class Tp(models.Model):
    tplan_id = models.AutoField(primary_key=True)
    task = models.OneToOneField(Tn, on_delete=models.CASCADE, blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tp'
