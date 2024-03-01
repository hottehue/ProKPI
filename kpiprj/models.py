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
outcome_reason_action = {
    1: ['Schneller als geplant, aber Mehrkosten', ['Team macht Überstunden', 'Zeit wird nicht effizient genutzt',\
                                       'Es wird zu viel Zeit für einzelne Aktivitäten verwendet', 'Zu viele Experten einem Task zugeordnet'],\
        ['Zeiterfassung überprüfen', 'Uberstunden begrenzen',\
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
                                       'Der Terminplan ist zu grosszugig (Parkinsons Gesetz)'],\
        ['Überstunden überwachen und Effizienz erhöhen', 'Ausidungsgraratien Traninig oder Coaching erhöhen']],

    5: ['Voll im Plan', ['Die Performance ist nur so gut wie der Plan. Sind die Schätzungen korrekt und stimmt die Qualität der Lieferobjekte?',\
                                     'Wurde etwas übersehen?'],\
        ['Stichproben von Lieferobjekten erheben und Qualität und Vollständigkeit überprüfen']],

    6: ['Im Plan, aber Minderkosten', ['Ein erfahrenes Team arbeitet hocheffizient oder:',\
        'Experten brauchen weniger Zeit als geplant', 'Experten kürzen ab, um Termine einzuhalten'],\
        ['Lieferobjekte auf Qualität und Vollständigkeit überprüfen', 'Vollständigkeit der Zeiterfassung überprüfen. Überprüfen, ob das Team überqualifiziert ist']],

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


class Phase(models.Model):
    phase_id = models.AutoField(primary_key=True)
    phase_name = models.CharField(max_length=255, blank=True, null=True)
    project = models.ForeignKey('Project', models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'phase'

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'project'

    def get_absolute_url(self):
        return reverse("tempload-list", args=[self.project_id])

    def __str__(self):
        return f" id={self.project_id}, name= {self.project_name}"

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
