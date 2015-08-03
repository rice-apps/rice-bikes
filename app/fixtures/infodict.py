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
            'Clean and lube train': {'price': 3, 'category': 'Drive Train'},
            'Replace pedals': {'price': 5, 'category': 'Drive Train'},
            'Clean gears': {'price': 3, 'category': 'Drive Train'},
            'Replace chain': {'price': 9, 'category': 'Drive Train'},
            'Install freewheel': {'price': 7, 'category': 'Drive Train'},
            'Replace crankset': {'price': 7, 'category': 'Drive Train'},
            'Install cassette': {'price': 9, 'category': 'Drive Train'},
            'Install threadless': {'price': 5, 'category': 'Stem'},
            'Install threaded': {'price': 5, 'category': 'Stem'},
            'Adjust bearings fh bb hs': {'price': 5, 'category': 'Headset'},
            'Adjust bearings': {'price': 9, 'category': 'Headset'},
            'Bearing overhaul': {'price': 11, 'category': 'Headset'}
}

import json

dict_list = []
pk = 0

for key in info_dict:
    item = dict()
    item["model"] = "app.MenuItem"
    item["pk"] = pk

    fields = dict()
    fields["name"] = key
    fields["category"] = info_dict[key]["category"]
    fields["price"] = info_dict[key]["price"]

    item["fields"] = fields
    pk += 1

    dict_list.append(item)


print json.dumps(dict_list, sort_keys=True, indent=4, separators=(',', ': '))