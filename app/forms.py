from app.models import Transaction, RentalBike, RefurbishedBike, RevenueUpdate, PartCategory, PartOrder, \
    MiscRevenueUpdate, BuyBackBike, PartMenuItem
from django import forms
from django.forms import Form, ModelForm
from django.contrib.auth.models import User


class RepairsForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ("service_description", "cost",)


class CustomerForm(ModelForm):
    rental_vin = forms.IntegerField(required=False)
    refurbished_vin = forms.IntegerField(required=False)
    buy_back_vin = forms.IntegerField(required=False)

    class Meta:
        model = Transaction
        fields = ("first_name", "last_name", "email", "affiliation", "service_description")

    def save(self, commit=True):
        # do something with self.cleaned_data['rental_vin']
        return super(CustomerForm, self).save(commit=commit)

    def clean(self):
        return self.cleaned_data


class TaskForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('service_description', 'cost', 'amount_paid',)


class RentalForm(ModelForm):
    class Meta:
        model = RentalBike
        fields = ('vin',)


class RefurbishedForm(ModelForm):
    class Meta:
        model = RefurbishedBike
        fields = ('vin',)


class BuyBackForm(ModelForm):
    class Meta:
        model = BuyBackBike
        fields = ('vin',)


class RevenueForm(ModelForm):
    class Meta:
        model = RevenueUpdate


class PartCategoryForm(ModelForm):
    class Meta:
        model = PartCategory
        exclude = ['transaction', 'date_submitted', ]


class DisabledPartCategoryForm(PartCategoryForm):
    class Meta:
        model = PartCategory
        exclude = ['transaction', 'date_submitted', ]
        widgets = {
            'category': forms.Select(attrs={'disabled': 'True'}),
            'price': forms.NumberInput(attrs={'disabled': 'True'}),
            'description': forms.TextInput(attrs={'disabled': 'True'}),
            'was_used': forms.CheckboxInput(attrs={'disabled': 'True'}),
        }


class PartOrderForm(Form):
    part = forms.ModelChoiceField(queryset=PartMenuItem.objects.all())
    number = forms.IntegerField()
    description = forms.CharField(required=False)


class MiscRevenueUpdateForm(ModelForm):
    class Meta:
        model = MiscRevenueUpdate


class SingleNumberForm(Form):
    number = forms.IntegerField(label='Number', initial=1)


class BuyBackSelectForm(ModelForm):
    class Meta:
        model = BuyBackBike
        include = ['vin', ]
        widgets = {
            'vin': forms.Select()
        }
