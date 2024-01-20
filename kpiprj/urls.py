from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginUser,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('', views.PrjListView),
    path('prjlist',views.PrjListView,name="prj-list"),
    path('kpi-calculation/<int:project_id>', views.KpiCalculation, name="kpi-calculation"),
    path('<int:id>',views.TemploadListView,name="tempload-list"),
    path('create-tempload/<int:project_id>',views.createTemploadView,name='create-tempload'),
    path('update-tempload/<int:project_id>/<int:temp_load_id>',views.updateTemploadView,name='update-tempload'),
    path('delete-tempload/<int:project_id>/<int:temp_load_id>', views.deleteTemploadView, name='delete-tempload'),
    path('view-tempload/<int:project_id>/<int:temp_load_id>/<str:phase_name>', views.singleTempLoadView, name='view-tempload'),
    path('create-project/',views.createPrjView,name='create-project'),
]