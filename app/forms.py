from app.models import Transaction, RentalBike, RefurbishedBike
from django import forms
from django.forms import ModelForm, Form
from django.contrib.auth.models import User


class CustomerForm(Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    affiliation = forms.CharField(max_length=100)
    no_receipt = forms.BooleanField(required=False)


class TasksForm(Form):
    Handlebars = forms.BooleanField(required=False)
    Brakes = forms.BooleanField(required=False)
    Frame = forms.BooleanField(required=False)

    @staticmethod
    def get_info_dict():
        # TODO(eddiedugan): Move these big dicts into a seperate file?
        info_dict = {
            'Adjust Derailleur': {'price': 7, 'category': 'shifters_derailleurs'},
            'Install Shifter Cable': {'price': 14, 'category': 'shifters_derailleurs'},
            'Install Derailleur': {'price': 11, 'category': 'shifters_derailleurs'},
            'Install Shifter': {'price': 11, 'category': 'shifters_derailleurs'},
            'Install Grips': {'price': 3, 'category': 'handlebars'},
            'Install Handlebars': {'price': 5, 'category': 'handlebars'},
            'Wrap Handlebars': {'price': 9, 'category': 'handlebars'},
            'Replace/Install ONE Tire': {'price': 7, 'category': 'wheels'},
            'Replace/Install TWO Tires': {'price': 14, 'category': 'wheels'},
            'Replace ONE tube': {'price': 7, 'category': 'wheels'},
            'Replace TWO tubes': {'price': 14, 'category': 'wheels'},
            'Wheel True': {'price': 14, 'category': 'wheels'},
            'Install Wheel': {'price': 12, 'category': 'wheels'},
            'Front Hub Overhaul': {'price': 16, 'category': 'wheels'},
            'Rear Hub Overhaul': {'price': 18, 'category': 'wheels'},
            'Coaster Hub Overhaul': {'price': 20, 'category': 'wheels'},
            'Adjust Bearings FW': {'price': 5, 'category': 'wheels'},
            'Adjust Bearings RW': {'price': 6, 'category': 'wheels'},
            'Wheel Adjust': {'price': 3, 'category': 'wheels'},
            'Basic Clean': {'price': 5, 'category': 'frame_alignment'},
            'Major Clean': {'price': 15, 'category': 'frame_alignment'},
            'Bike Build': {'price': 25, 'category': 'frame_alignment'},
            'Install Front Basket': {'price': 7, 'category': 'frame_alignment'}, 
            'Install Rear Rack': {'price': 12, 'category': 'frame_alignment'},
            'Align Derailleur Hanger': {'price': 7, 'category': 'frame_alignment'},
            'Install Cartridge BB': {'price': 10, 'category': 'bottom_bracket'},
            'Install Cup and Spindle BB': {'price': 12, 'category': 'bottom_bracket'},
            'Overhaul Cup and Spindle': {'price': 16, 'category': 'bottom_bracket'},
            'Install One-Piece BB': {'price': 10, 'category': 'bottom_bracket'},
            'Overhaul One-Piece BB': {'price': 17, 'category': 'bottom_bracket'},
            'Adjust Bearings BB': {'price': 5, 'category': 'bottom_bracket'}, 
            'Install Saddle': {'price': 5, 'category': 'saddle_seatpost'},
            'Install Seatpost w/o Saddle': {'price': 3, 'category': 'saddle_seatpost'},
            'Install Seatpost & Saddle': {'price': 7, 'category': 'saddle_seatpost'}, 
            'Seat Adjust': {'price': 3, 'category': 'saddle_seatpost'},
            'Adjust Rim Brake': {'price': 8, 'category': 'brakes'}, 
            'Adjust Disk Brake': {'price': 9, 'category': 'brakes'},
            'Install Brake or Lever': {'price': 12, 'category': 'brakes'},
            'Install Brake Cable': {'price': 14, 'category': 'brakes'},
            'Clean & Lube Train': {'price': 3, 'category': 'drivetrain'},
            'Replace Pedals': {'price': 5, 'category': 'drivetrain'},
            'Clean Gears': {'price': 3, 'category': 'drivetrain'}, 
            'Replace Chain': {'price': 9, 'category': 'drivetrain'},
            'Install Freewheel': {'price': 7, 'category': 'drivetrain'},
            'Replace Crankset': {'price': 7, 'category': 'drivetrain'},
            'Install Cassette': {'price': 9, 'category': 'drivetrain'},
            'Install Threadless': {'price': 5, 'category': 'stem'},
            'Install Threaded': {'price': 5, 'category': 'stem'},
            'Adjust Bearings: FH, BB, HS': {'price': 5, 'category': 'headset'}, 
            'Adjust Bearings': {'price': 9, 'category': 'headset'}, 
            'Bearing Overhaul': {'price': 11, 'category': 'headset'}
        }
        return info_dict

    @staticmethod
    def get_category_dict():
        info_dict_shifters_derailleurs = {
            'Adjust Derailleur': {'price': 7},
            'Install Shifter Cable': {'price': 14},
            'Install Derailleur': {'price': 11},
            'Install Shifter': {'price': 11}
        }
        info_dict_handlebars = {
            # TODO(eddiedugan): Find a way to represent the additional cost of materials (e.g. $3 + grips).
            # However, this follows the form if we just sum 'base cost' (don't include cost of parts).
            'Install Grips': {'price': 3},
            'Install Handlebars': {'price': 5}, # + grips
            'Wrap Handlebars': {'price': 9} # + tape
        }
        info_dict_wheels = {
            'Replace/Install ONE Tire': {'price': 7}, # + Tire
            'Replace/Install TWO Tires': {'price': 14}, # + tires
            'Replace ONE tube': {'price': 7}, # + tube
            'Replace TWO tubes': {'price': 14}, # + tubes
            'Wheel True': {'price': 14},
            'Install Wheel': {'price': 12},
            'Front Hub Overhaul': {'price': 16},
            'Rear Hub Overhaul': {'price': 18},
            'Coaster Hub Overhaul': {'price': 20},
            'Adjust Bearings FW': {'price': 5},
            'Adjust Bearings RW': {'price': 6},
            'Wheel Adjust': {'price': 3}
        }
        info_dict_frame_alignment = {
            'Basic Clean': {'price': 5},
            'Major Clean': {'price': 15},
            'Bike Build': {'price': 25},
            'Install Front Basket': {'price': 7}, 
            'Install Rear Rack': {'price': 12},
            'Align Derailleur Hanger': {'price': 7}
        }
        info_dict_bottom_bracket = {
            'Install Cartridge BB': {'price': 10}, # + BB
            'Install Cup and Spindle BB': {'price': 12}, # + BB
            'Overhaul Cup and Spindle': {'price': 16},
            'Install One-Piece BB': {'price': 10}, # + BB
            'Overhaul One-Piece BB': {'price': 17},
            'Adjust Bearings BB': {'price': 5}
        }
        info_dict_saddle_seatpost = {
            'Install Saddle': {'price': 5},
            'Install Seatpost w/o Saddle': {'price': 3},
            'Install Seatpost & Saddle': {'price': 7}, 
            'Seat Adjust': {'price': 3}
        }
        info_dict_brakes = {
            'Adjust Rim Brake': {'price': 8}, 
            'Adjust Disk Brake': {'price': 9},
            'Install Brake or Lever': {'price': 12},
            'Install Brake Cable': {'price': 14}
        }
        info_dict_drivetrain = {
            'Clean & Lube Train': {'price': 3},
            'Replace Pedals': {'price': 5}, # + pedals
            'Clean Gears': {'price': 3}, 
            'Replace Chain': {'price': 9}, # + chain
            'Install Freewheel': {'price': 7},
            'Replace Crankset': {'price': 7},
            'Install Cassette': {'price': 9}
        }
        info_dict_stem = {
            'Install Threadless': {'price': 5},
            'Install Threaded': {'price': 5}
        }
        info_dict_headset = {
            'Adjust Bearings: FH, BB, HS': {'price': 5}, 
            'Adjust Bearings': {'price': 9}, 
            'Bearing Overhaul': {'price': 11}
        }
        category_dict = {
            'Shifters and Derailleurs': info_dict_shifters_derailleurs,
            'Handlebars': info_dict_handlebars,
            'Wheels': info_dict_wheels,
            'Frame and Alignment': info_dict_frame_alignment,
            'Bottom Bracket': info_dict_bottom_bracket,
            'Saddle and Seatpost': info_dict_saddle_seatpost,
            'Brakes': info_dict_brakes,
            'Drive-Train': info_dict_drivetrain,
            'Stem': info_dict_stem,
            'Headset': info_dict_headset
        }
        return category_dict

    @staticmethod
    def get_non_task_fields():
        return ('Service description',
                'Price',
                'Rental vin',
                'Refurbished vin')


class RepairsForm(TasksForm):
    service_description = forms.CharField(max_length=100)
    price = forms.IntegerField()
    rental_vin = forms.IntegerField(required=False)
    refurbished_vin = forms.IntegerField(required=False)


class RentalForm(ModelForm):
    class Meta:
        model = RentalBike


class RefurbishedForm(ModelForm):
    class Meta:
        model = RefurbishedBike


