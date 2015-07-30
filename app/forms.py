from app.models import Transaction, RentalBike, RefurbishedBike, RevenueUpdate, PartCategory, PartOrder
from django import forms
from django.forms import ModelForm, Form
from django.contrib.auth.models import User


class TasksForm(Form):
    Adjust_derailleur = forms.BooleanField(required=False)
    Install_shifter_cable = forms.BooleanField(required=False)
    Install_derailleur = forms.BooleanField(required=False)
    Install_shifter = forms.BooleanField(required=False)
    Install_grips = forms.BooleanField(required=False)
    Install_handlebars = forms.BooleanField(required=False)
    Wrap_handlebars = forms.BooleanField(required=False)
    Replace_or_install_one_tire = forms.BooleanField(required=False)
    Replace_or_install_two_tires = forms.BooleanField(required=False)
    Replace_one_tube = forms.BooleanField(required=False)
    Replace_two_tubes = forms.BooleanField(required=False)
    Wheel_true = forms.BooleanField(required=False)
    Install_wheel = forms.BooleanField(required=False)
    Front_hub_overhaul = forms.BooleanField(required=False)
    Rear_hub_overhaul = forms.BooleanField(required=False)
    Coaster_hub_overhaul = forms.BooleanField(required=False)
    Adjust_bearings_fw = forms.BooleanField(required=False)
    Adjust_bearings_rw = forms.BooleanField(required=False)
    Wheel_adjust = forms.BooleanField(required=False)
    Basic_clean = forms.BooleanField(required=False)
    Major_clean = forms.BooleanField(required=False)
    Bike_build = forms.BooleanField(required=False)
    Install_front_basket = forms.BooleanField(required=False)
    Install_rear_rack = forms.BooleanField(required=False)
    Align_derailleur_hanger = forms.BooleanField(required=False)
    Install_cartridge_bb = forms.BooleanField(required=False)
    Install_cup_and_spindle_bb = forms.BooleanField(required=False)
    Overhaul_cup_and_spindle = forms.BooleanField(required=False)
    Install_one_piece_bb = forms.BooleanField(required=False)
    Overhaul_one_piece_bb = forms.BooleanField(required=False)
    Adjust_bearings_bb = forms.BooleanField(required=False)
    Install_saddle = forms.BooleanField(required=False)
    Install_seatpost_without_saddle = forms.BooleanField(required=False)
    Install_seatpost_and_saddle = forms.BooleanField(required=False)
    Seat_adjust = forms.BooleanField(required=False)
    Adjust_rim_brake = forms.BooleanField(required=False)
    Adjust_disk_brake = forms.BooleanField(required=False)
    Install_brake_or_lever = forms.BooleanField(required=False)
    Install_brake_cable = forms.BooleanField(required=False)
    Clean_and_lube_train = forms.BooleanField(required=False)
    Replace_pedals = forms.BooleanField(required=False)
    Clean_gears = forms.BooleanField(required=False)
    Replace_chain = forms.BooleanField(required=False)
    Install_freewheel = forms.BooleanField(required=False)
    Replace_crankset = forms.BooleanField(required=False)
    Install_cassette = forms.BooleanField(required=False)
    Install_threadless = forms.BooleanField(required=False)
    Install_threaded = forms.BooleanField(required=False)
    Adjust_bearings_fh_bb_hs = forms.BooleanField(required=False)
    Adjust_bearings = forms.BooleanField(required=False)
    Bearing_overhaul = forms.BooleanField(required=False)

    @staticmethod
    def get_info_dict():
        # TODO(eddiedugan): Move these big dicts into a seperate file?
        info_dict = {
            'Adjust derailleur': {'price': 7, 'category': 'Shifters derailleurs'},
            'Install shifter cable': {'price': 14, 'category': 'Shifters derailleurs'},
            'Install derailleur': {'price': 11, 'category': 'Shifters derailleurs'},
            'Install shifter': {'price': 11, 'category': 'Shifters derailleurs'},
            'Install grips': {'price': 3, 'category': 'Handlebars'},
            'Install handlebars': {'price': 5, 'category': 'Handlebars'},
            'Wrap handlebars': {'price': 9, 'category': 'Handlebars'},
            'Replace or install one tire': {'price': 7, 'category': 'Wheels'},
            'Replace or install two tires': {'price': 14, 'category': 'Wheels'},
            'Replace one tube': {'price': 7, 'category': 'Wheels'},
            'Replace two tubes': {'price': 14, 'category': 'Wheels'},
            'Wheel true': {'price': 14, 'category': 'Wheels'},
            'Install wheel': {'price': 12, 'category': 'Wheels'},
            'Front hub overhaul': {'price': 16, 'category': 'Wheels'},
            'Rear hub overhaul': {'price': 18, 'category': 'Wheels'},
            'Coaster hub overhaul': {'price': 20, 'category': 'Wheels'},
            'Adjust bearings fw': {'price': 5, 'category': 'Wheels'},
            'Adjust bearings rw': {'price': 6, 'category': 'Wheels'},
            'Wheel adjust': {'price': 3, 'category': 'Wheels'},
            'Basic clean': {'price': 5, 'category': 'Frame and alignment'},
            'Major clean': {'price': 15, 'category': 'Frame and alignment'},
            'Bike build': {'price': 25, 'category': 'Frame and alignment'},
            'Install front basket': {'price': 7, 'category': 'Frame and alignment'},
            'Install rear rack': {'price': 12, 'category': 'Frame and alignment'},
            'Align derailleur hanger': {'price': 7, 'category': 'Frame and alignment'},
            'Install cartridge bb': {'price': 10, 'category': 'Bottom bracket'},
            'Install cup and spindle bb': {'price': 12, 'category': 'Bottom bracket'},
            'Overhaul cup and spindle': {'price': 16, 'category': 'Bottom bracket'},
            'Install one piece bb': {'price': 10, 'category': 'Bottom bracket'},
            'Overhaul one piece bb': {'price': 17, 'category': 'Bottom bracket'},
            'Adjust bearings bb': {'price': 5, 'category': 'Bottom bracket'},
            'Install saddle': {'price': 5, 'category': 'Saddle seatpost'},
            'Install seatpost without saddle': {'price': 3, 'category': 'Saddle seatpost'},
            'Install seatpost and saddle': {'price': 7, 'category': 'Saddle seatpost'},
            'Seat adjust': {'price': 3, 'category': 'Saddle seatpost'},
            'Adjust rim brake': {'price': 8, 'category': 'Brakes'},
            'Adjust disk brake': {'price': 9, 'category': 'Brakes'},
            'Install brake or lever': {'price': 12, 'category': 'Brakes'},
            'Install brake cable': {'price': 14, 'category': 'Brakes'},
            'Clean and lube train': {'price': 3, 'category': 'Drive train'},
            'Replace pedals': {'price': 5, 'category': 'Drive train'},
            'Clean gears': {'price': 3, 'category': 'Drive train'},
            'Replace chain': {'price': 9, 'category': 'Drive train'},
            'Install freewheel': {'price': 7, 'category': 'Drive train'},
            'Replace crankset': {'price': 7, 'category': 'Drive train'},
            'Install cassette': {'price': 9, 'category': 'Drive train'},
            'Install threadless': {'price': 5, 'category': 'Stem'},
            'Install threaded': {'price': 5, 'category': 'Stem'},
            'Adjust bearings fh bb hs': {'price': 5, 'category': 'Headset'},
            'Adjust bearings': {'price': 9, 'category': 'Headset'},
            'Bearing overhaul': {'price': 11, 'category': 'Headset'}
        }
        return info_dict

    @staticmethod
    def get_category_dict():
        info_dict_shifters_derailleurs = {
            'Adjust derailleur': {'price': 7},
            'Install shifter cable': {'price': 14},
            'Install derailleur': {'price': 11},
            'Install shifter': {'price': 11}
        }
        info_dict_handlebars = {
            # TODO(eddiedugan): Find a way to represent the additional cost of materials (e.g. $3 + grips).
            # However, this follows the form if we just sum 'base cost' (don't include cost of parts).
            'Install grips': {'price': 3},
            'Install handlebars': {'price': 5}, # + grips
            'Wrap handlebars': {'price': 9} # + tape
        }
        info_dict_wheels = {
            'Replace or install one tire': {'price': 7}, # + Tire
            'Replace or install two tires': {'price': 14}, # + tires
            'Replace one tube': {'price': 7}, # + tube
            'Replace two tubes': {'price': 14}, # + tubes
            'Wheel true': {'price': 14},
            'Install wheel': {'price': 12},
            'Front hub overhaul': {'price': 16},
            'Rear hub overhaul': {'price': 18},
            'Coaster hub overhaul': {'price': 20},
            'Adjust bearings fw': {'price': 5},
            'Adjust bearings rw': {'price': 6},
            'Wheel adjust': {'price': 3}
        }
        info_dict_frame_alignment = {
            'Basic clean': {'price': 5},
            'Major clean': {'price': 15},
            'Bike build': {'price': 25},
            'Install front basket': {'price': 7},
            'Install rear rack': {'price': 12},
            'Align derailleur hanger': {'price': 7}
        }
        info_dict_bottom_bracket = {
            'Install cartridge bb': {'price': 10}, # + BB
            'Install cup and spindle bb': {'price': 12}, # + BB
            'Overhaul cup and spindle': {'price': 16},
            'Install one piece bb': {'price': 10}, # + BB
            'Overhaul one piece bb': {'price': 17},
            'Adjust bearings bb': {'price': 5}
        }
        info_dict_saddle_seatpost = {
            'Install saddle': {'price': 5},
            'Install seatpost without saddle': {'price': 3},
            'Install seatpost and saddle': {'price': 7},
            'Seat adjust': {'price': 3}
        }
        info_dict_brakes = {
            'Adjust rim brake': {'price': 8},
            'Adjust disk brake': {'price': 9},
            'Install brake or lever': {'price': 12},
            'Install brake cable': {'price': 14}
        }
        info_dict_drivetrain = {
            'Clean and lube train': {'price': 3},
            'Replace pedals': {'price': 5}, # + pedals
            'Clean gears': {'price': 3},
            'Replace chain': {'price': 9}, # + chain
            'Install freewheel': {'price': 7},
            'Replace crankset': {'price': 7},
            'Install cassette': {'price': 9}
        }
        info_dict_stem = {
            'Install threadless': {'price': 5},
            'Install threaded': {'price': 5}
        }
        info_dict_headset = {
            'Adjust bearings: FH, BB, HS': {'price': 5},
            'Adjust bearings': {'price': 9},
            'Bearing overhaul': {'price': 11}
        }
        category_dict = {
            'Shifters and derailleurs': info_dict_shifters_derailleurs,
            'Handlebars': info_dict_handlebars,
            'Wheels': info_dict_wheels,
            'Frame and alignment': info_dict_frame_alignment,
            'Bottom bracket': info_dict_bottom_bracket,
            'Saddle and seatpost': info_dict_saddle_seatpost,
            'Brakes': info_dict_brakes,
            'Drive train': info_dict_drivetrain,
            'Stem': info_dict_stem,
            'Headset': info_dict_headset
        }
        return category_dict

    @staticmethod
    def get_non_task_fields():
        return ('Service description',
                'Cost',
                'Rental vin',
                'Refurbished vin')


class RepairsForm(TasksForm):
    service_description = forms.CharField(max_length=100, required=False)
    cost = forms.IntegerField()
    # rental_vin = forms.IntegerField(required=False)
    # refurbished_vin = forms.IntegerField(required=False)


class CustomerForm(ModelForm):
    rental_vin = forms.IntegerField(required=False)
    refurbished_vin = forms.IntegerField(required=False)

    class Meta:
        model = Transaction
        fields = ("first_name", "last_name", "email", "affiliation")

    def save(self, commit=True):
        # do something with self.cleaned_data['rental_vin']
        return super(CustomerForm, self).save(commit=commit)

    def clean(self):
        return self.cleaned_data


class TransactionForm(ModelForm):
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


class RevenueForm(ModelForm):
    class Meta:
        model = RevenueUpdate


class PartCategoryForm(ModelForm):
    class Meta:
        model = PartCategory
        exclude = ['transaction', 'date_submitted', ]


class PartOrderForm(ModelForm):
    class Meta:
        model = PartOrder
        exclude = ['date_submitted', ]

