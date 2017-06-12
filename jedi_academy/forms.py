from django import forms
from django.forms import inlineformset_factory
from .models import Jedi, Candidate, Exam, OrderCode


class JediChoiceForm(forms.Form):
    jedi = forms.ModelChoiceField(
        label='Jedi name',
        queryset=Jedi.objects.all()
    )


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ('name', 'life_planet', 'age', 'email')


class ExamForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        for question in OrderCode.objects.last().question_set.all():
            field_name = 'question_%s' % question.pk
            self.fields[field_name] = forms.NullBooleanField(
                label=question.content, required=True)

    def save(self, candidate_pk):
        data = self.cleaned_data
        for key, value in data.items():
            exam = Exam.objects.get_or_create(
                candidate_id=int(candidate_pk),
                question_id=int(key.replace('question_', '')))[0]
            exam.answer = value
            exam.save()