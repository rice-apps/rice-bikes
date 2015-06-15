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
            for field in self.data:

                print kwargs
                # model_info = str(Transaction.objects.filter(pk=kwargs['pk']).values()[0][str(my_field)])


                my_field = str(field)
                print "my_field = " + my_field
                if my_field not in self.fields:
                    continue

                val = str(self.data[field])
                print "val = " + val

                if val == 'IN_PROGRESS' or val == 'COMPLETE':
                    setattr(entry, my_field, 'COMPLETE')


            for field in self.fields:
                my_field = str(field)
                print "my_field = " + my_field

                if my_field in self.data:
                    continue

                setattr(entry, my_field, 'IN_PROGRESS')

                # model_info = str(Transaction.objects.filter(pk=kwargs['pk']).values()[0][str(my_field)])

        entry.save()
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



