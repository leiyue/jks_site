# -*- coding: utf-8 -*-
# -*- date: 2016-04-11 10:34 -*-
from django.http import HttpResponseRedirect
from mezzanine.pages.page_processors import processor_for

from apps.polls.forms import VotingForm
from .models import Poll, Vote, Choice


@processor_for(Poll)
def voting_form(request, page):
    poll_user = [
        v.user for v in Vote.objects.filter(choice__poll=page.poll)
        ]
    total_votes = len(poll_user)

    poll_choice = [
        (c.id, c.text)
        for c in page.poll.choice_set.all()
        ]

    if request.user in poll_user:
        poll_results = [
            (
                c.text,
                c.vote_set.count(),
                c.vote_set.count() * 100 / total_votes
            ) for c in page.poll.choice_set.all()
            ]
        return {'poll_results': poll_results}

    else:
        if request.method == 'POST':
            print(request.POST)
            form = VotingForm(request.POST, poll_choice=poll_choice)
            if form.is_valid():
                choice_id = form.cleaned_data['choices']
                choice = Choice.objects.get(pk=choice_id)
                vote = Vote(choice=choice, user=request.user)
                vote.save()
                return HttpResponseRedirect(page.get_absolute_url())
            else:
                return {'form': form}
        form = VotingForm(poll_choice=poll_choice)
        return {'form': form}
