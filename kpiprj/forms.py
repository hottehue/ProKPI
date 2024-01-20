from django import forms
from .models import TempLoad, Phase, Project

# below: phase_id field not any more filled this way...now  filled with filtered_choices arg from the view
# PHASE_CHOICES = Phase.objects.values_list('phase_id', 'phase_name')
# class TemploadForm(forms.Form):
#   'phase_id': forms.Select(choices=PHASE_CHOICES),

class TemploadForm(forms.ModelForm):
    class Meta:
        model = TempLoad
        fields = '__all__'
        exclude = ['project_id','username']
        # below list include specific fields in form
        # or exclude command (to remove specific fields from form)
        # fields = []
        # exclude = [temp_load_id]
        widgets = {
            'task_name':forms.TextInput(attrs={'required': 'required'}),
            'phase_id': forms.Select(),
            'startdate': forms.DateInput(attrs={'type': 'date','required': 'required'}),
            'enddate': forms.DateInput(attrs={'type': 'date','required': 'required'}),
            'budget': forms.NumberInput(attrs={'required': 'required'}),
            'startdate_is': forms.DateInput(attrs={'type': 'date','required': 'required'}),
            'enddate_is': forms.DateInput(attrs={'type': 'date','required': 'required'}),
            'budget_is': forms.NumberInput(attrs={'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        filtered_choices = kwargs.pop('filtered_choices', None)
        super(TemploadForm, self).__init__(*args, **kwargs)
        if filtered_choices:
            self.fields['phase_id'] = forms.ChoiceField(choices=filtered_choices, widget=forms.Select)

        self.fields['task_name'].widget.attrs.update({'class': 'input', 'placeholder': 'Enter task name'})
        # below method to customise all fields (for information only)
        # for name, field in self.fields.items():
        #    field.widget.attrs.update({'class':'input'})


class KpiListForm(forms.Form):
    stichtag = forms.DateField(required=True)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.fields['project_name'].widget.attrs.update({'class': 'input', 'placeholder': 'Enter project name','required': 'required'})
