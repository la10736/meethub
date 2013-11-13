'''
Created on 12/nov/2013

@author: michele
'''


# forms.py
from django import forms

class DebugForm(forms.Form):
    start = forms.DateTimeField()
    duration = forms.IntegerField(min_value=1)
    place = forms.CharField()
    argomenti = forms.CharField(widget=forms.Textarea)

    def create_event(self,dbgsrc):
        dbgsrc.new_event(self.cleaned_data['argomenti'],
                         self.cleaned_data['place'],
                         self.cleaned_data['start'],
                         self.cleaned_data['duration'])