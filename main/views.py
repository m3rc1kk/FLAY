from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView, DetailView
from .models import Award, Nominee, Vote, Winner


class IndexView(TemplateView):
    template_name = 'main/index.html'

    ALLOWED_USERS = ['m3rc1k']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.username not in self.ALLOWED_USERS:
            return redirect('auth')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_votes = []
        if self.request.user.is_authenticated:
            user_votes = Vote.objects.filter(
                user=self.request.user
            ).values_list('award_id', flat=True)

        context['user_votes'] = list(user_votes)
        context['awardsMajor'] = Award.objects.filter(is_major=True)
        context['awardsMinor'] = Award.objects.filter(is_major=False)
        context['winners'] = Winner.objects.all()
        return context

class NomineesView(DetailView):
    model = Award
    template_name = 'main/nominees.html'
    context_object_name = 'award'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        voted_nominee_id = None
        if self.request.user.is_authenticated:
            vote = Vote.objects.filter(
                user=self.request.user,
                award=self.object
            ).first()
            if vote:
                voted_nominee_id = vote.nominee_id

        context['voted_nominee_id'] = voted_nominee_id
        return context


def vote_for_nominee(request, award_id, nominee_id):
    award = get_object_or_404(Award, id=award_id)
    nominee = get_object_or_404(Nominee, id=nominee_id)

    if request.user.is_authenticated:
        vote, created = Vote.objects.get_or_create(
            user=request.user,
            award=award,
            defaults={'nominee': nominee}
        )

    if not created:
        vote.nominee = nominee
        vote.save()

    return redirect('nominees', slug=award.slug)