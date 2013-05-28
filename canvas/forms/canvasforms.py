from django import forms
from django.forms.extras.widgets import SelectDateWidget

class PlaygroundFilterForm(forms.Form):
	date = forms.DateField(required=False)
	blackwhite = forms.BooleanField(widget=forms.HiddenInput(), required=False)
	intensity0 = forms.BooleanField(widget=forms.HiddenInput(), required=False)
	intensity1 = forms.BooleanField(widget=forms.HiddenInput(), required=False)
	intensity2 = forms.BooleanField(widget=forms.HiddenInput(), required=False)
	intensity3 = forms.BooleanField(widget=forms.HiddenInput(), required=False)
