# -*- coding: utf-8 -*-
# -*- date: 2016-04-11 09:38 -*-
from django import forms


class VotingForm(forms.Form):
    choices = forms.TypedChoiceField(
        choices=[],
        coerce=int,
        widget=forms.RadioSelect()
    )

    def __init__(self, *args, **kwargs):
        poll_choice = kwargs.pop('poll_choice', None)
        print(poll_choice)
        super(VotingForm, self).__init__(*args, **kwargs)
        self.fields['choices'].choices = poll_choice or []
