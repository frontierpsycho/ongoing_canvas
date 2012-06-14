from django import forms
from django.forms.extras.widgets import SelectDateWidget

class PlaygroundFilterForm(forms.Form):
	date = forms.DateField(widget=SelectDateWidget)
