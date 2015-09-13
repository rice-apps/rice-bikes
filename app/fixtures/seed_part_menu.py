import json

if __name__ == '__main__':

    pk = 0

    json_list = list()

    file = open('data_parts.txt', 'r')

    category = None

    for line in file:

        if line == "":
            exit()

        if "!" in line:
            category = line.strip("!")
            continue

        if not category:
            exit("Category cannot be null!")

        if not line:
            exit()


        json_item = dict()
        json_item["model"] = "app.PartMenuItem"
        json_item["pk"] = pk

        fields = dict()
        fields["name"] = line.strip("\n")
        fields["category"] = category.strip("\n")

        json_item["fields"] = fields

        pk += 1

        json_list.append(json_item)

    print json.dumps(json_list, sort_keys=True, indent=4, separators=(',', ': '))
