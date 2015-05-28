from django import forms
from django.forms import ModelForm, Form

FRAME_AND_ALIGNMENT_CHOICES = [("derailleur", "Align Derailleur Hanger"), ("clean", "Basic Clean"),
                               ("basket", "Install Front Basket")]
HANDLEBARS_CHOICES = [("grips", "Install Grips"), ("handlebars", "Install Handlebars")]
BRAKES_CHOICES = [("rim-brake", "Adjust Rim Brake"), ("disk-brake", "Adjust Disc Brake")]


class CustomerForm(Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    affiliation = forms.CharField(max_length=100)


class RepairsForm(Form):
    frame_and_alignment = forms.MultipleChoiceField(
        choices=FRAME_AND_ALIGNMENT_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )
    handlebar_choices = forms.MultipleChoiceField(
        choices=HANDLEBARS_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )
    brakes_choices = forms.MultipleChoiceField(
        choices=BRAKES_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )
    # handlebars = forms.MultipleChoiceField(choices=HANDLEBARS_CHOICES, widget=forms.CheckboxSelectMultiple)
    # brakes = forms.MultipleChoiceField(choices=BRAKES_CHOICES, widget=forms.CheckboxSelectMultiple)