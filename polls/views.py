from django.views.generic import DetailView, ListView, RedirectView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from polls.models import Choice, Poll, Vote
from dboard.models import Chlcontact

class PollListView(ListView):
    model = Poll
    def get_context_data(self, **kwargs):
        context = super(PollListView, self).get_context_data(**kwargs)
        contact = self.request.GET.get('contact')
        context['contact'] = contact
        return context

class PollDetailView(DetailView):
    model = Poll

    def get_context_data(self, **kwargs):
        context = super(PollDetailView, self).get_context_data(**kwargs)
        contact = self.request.GET.get('contact')
        context['poll'].votable = self.object.can_vote(contact)
        context['contact'] = contact
        return context


class PollVoteView(RedirectView):
    def post(self, request, *args, **kwargs):
        poll = Poll.objects.get(id=kwargs['pk'])
        user = request.user
        choice = Choice.objects.get(id=request.POST['choice_pk'])
        contact_key = request.POST['contact']
        kwargs['contact'] = contact_key
        contact = Chlcontact.objects.get(chlkey=contact_key)

        Vote.objects.create(poll=poll, user=user, choice=choice,
                            contact=contact)
        messages.success(request, _("Thanks for your vote."))
        return super(PollVoteView, self).post(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return reverse_lazy('polls:list')+"?contact=%s" % kwargs['contact']
