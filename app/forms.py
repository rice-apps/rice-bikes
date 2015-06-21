from app.models import Transaction
from django import forms
from django.forms import ModelForm, Form
from django.contrib.auth.models import User

FRAME_AND_ALIGNMENT_CHOICES = [("derailleur", "Align Derailleur Hanger"), ("clean", "Basic Clean"),
                               ("basket", "Install Front Basket")]
HANDLEBARS_CHOICES = [("grips", "Install Grips"), ("handlebars", "Install Handlebars")]
BRAKES_CHOICES = [("rim-brake", "Adjust Rim Brake"), ("disk-brake", "Adjust Disc Brake")]

class CustomerForm(Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    affiliation = forms.CharField(max_length=100)
    no_receipt = forms.BooleanField(required=False)

class RepairsForm(ModelForm):

    fields = ['handlebars', 'brakes', 'frame']
    handlebars = forms.NullBooleanField()
    brakes = forms.NullBooleanField()
    frame = forms.NullBooleanField()

    class Meta:
        model = Transaction
        fields = ['handlebars', 'brakes', 'frame']

    def save(self, commit=True, **kwargs):

        print self.data
        print self.cleaned_data
        entry = super(RepairsForm, self).save(commit=False)
        if commit:

            # save all non NOT_ASSIGNED fields
            all_fields = []
            checked_fields = []

            for field in self.data:

                my_field = str(field)
                print "my_field = " + my_field

                if my_field not in self.fields and my_field[:-4] not in self.fields:
                    continue

                if my_field[-4:] == "_ALL":
                    all_fields.append(my_field)
                else:
                    checked_fields.append(my_field)

            for my_field_all in all_fields:
                my_field = my_field_all[:-4]
                print "my_field in all = " + my_field
                setattr(entry, my_field, 'IN_PROGRESS')
                entry.save(update_fields=[my_field])

            for my_field in checked_fields:
                setattr(entry, my_field, 'COMPLETE')
                entry.save(update_fields=[my_field])

        return entry




class RepairsFormSubmit(Form):
    handlebars = forms.BooleanField(required=False)
    brakes = forms.BooleanField(required=False)
    frame = forms.BooleanField(required=False)
    service_description = forms.CharField(max_length=100)
    price = forms.CharField(max_length=10)


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')



