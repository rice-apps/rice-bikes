import json

if __name__ == '__main__':

    pk = 0

    json_list = list()

    file = open('data_accessories.txt', 'r')
    for line in file:
        item = line.split(", ").strip("\n")

        json_item = dict()
        json_item["model"] = "app.AccessoryMenuItem"
        json_item["pk"] = pk

        fields = dict()
        fields["name"] = item[0]
        fields["price"] = item[1]

        json_item["fields"] = fields

        pk += 1

        json_list.append(json_item)

    print json.dumps(json_list, sort_keys=True, indent=4, separators=(',', ': '))
