from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View, DetailView, ListView
from django.views.generic.edit import FormView
from django.db.models import Count

from .models import Candidate, Jedi
from .forms import JediChoiceForm, CandidateForm, ExamForm


class IndexView(TemplateView):
    template_name = 'jedi_academy/index.html'


class JediChoice(FormView):
    template_name = 'jedi_academy/jedi_choice.html'
    form_class = JediChoiceForm

    def form_valid(self, form):
        jedi = form.cleaned_data.get('jedi')
        self.request.session['jedi_pk'] = jedi.pk
        return redirect('academy:jedi:padawans', pk=jedi.pk)


class JediPadawans(View):

    def get(self, request, pk):
        jedi = get_object_or_404(Jedi, pk=pk)
        candidates = Candidate.objects.filter(
            life_planet=jedi.training_planet,
            is_padawan=False
        )
        return render(
            request,
            'jedi_academy/jedi_padawans.html', {'candidates': candidates}
        )


class JediGo(View):
    template_name = 'jedi_academy/warning.html'
    msg = 'Слишком много подаванов. Вы не справетись, мастер.'

    def get(self, request, pk, cand_pk):
        candidate = get_object_or_404(Candidate, pk=cand_pk)
        jedi = get_object_or_404(Jedi, pk=pk)
        if jedi.candidate_set.count() < 3:
            jedi.add_padawan(candidate)
            self.msg = "У Вас новый падаван."
        return render(
            request,
            self.template_name,
            {'msg': self.msg}
        )


class CandidateDetail(DetailView):
    model = Candidate
    template_name = 'jedi_academy/cand_detail.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(CandidateDetail, self).get_context_data(**kwargs)
        context['jedi_pk'] = self.request.session.get('jedi_pk')
        return context


class CandidateCreate(FormView):
    template_name = 'jedi_academy/cand_create.html'
    form_class = CandidateForm

    def form_valid(self, form):
        candidate = form.save()
        return redirect('academy:candidate:exam', pk=candidate.pk)


class CandidateExam(FormView):
    template_name = 'jedi_academy/cand_exam.html'
    form_class = ExamForm

    def form_valid(self, form):
        form.save(self.kwargs['pk'])
        return render(self.request, 'jedi_academy/warning.html', {'msg': 'Успех'})

    def get_context_data(self, **kwargs):
        context = super(CandidateExam, self).get_context_data(**kwargs)
        context['cand_pk'] = self.kwargs['pk']
        return context


# Extends version


class JediListView(ListView):
    template_name = 'jedi_academy/jedi_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Jedi.objects.annotate(
            Count('candidate')).order_by('-candidate__count', 'name')


class JediListViewActive(ListView):
    template_name = 'jedi_academy/jedi_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Jedi.objects.annotate(
            Count('candidate')).filter(
            candidate__count__gt=0).order_by('-candidate__count', 'name')