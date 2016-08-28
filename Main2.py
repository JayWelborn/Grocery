todays_list = []
todays_sorted_list = []
checked_list = []
read_list = open('listsave.txt', 'r+')
master_list = [x.strip('\n') for x in read_list.readlines()]


class Grocery(object):
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def __str__(self):
        print self.name


# 	This Function gets a list of items from the user and puts them into a list


def get_items():
    item = raw_input("Add item to list or \ntype 'finished' if finished \n> ")
    if 'finished' not in item:
        todays_list.append(Grocery(item, 0))
        get_items()

    elif 'finish' in item:
        print "Today's list is: "
        print [item.name for item in todays_list]


# This function will compare items from today's list to the master list,
# 	and sort them accordingly. It will place items not on the master list at the end.	

def sort_todays_items():
    count = 0
    for item in todays_list:
        name = item.name
        count += 1
        if name in master_list:
            item.position = master_list.index(name)

        elif name not in master_list:
            item.position = count

        else:
            print "Unknown Error."

    sorted_list = sorted(todays_list, key=lambda item: item.position)
    print "Today's list sorted based on master: "
    print [item.name for item in sorted_list]

    for item in sorted_list:
        name = item.name
        todays_sorted_list.append(name)


# 	This function sorts todays items in the order the user checks them off,
# 	and makes a new list, including new items from today.	

def check_items():

    while todays_sorted_list:

        item = raw_input("Item checked: ")

        if item in todays_sorted_list:
            todays_sorted_list.remove(item)
            checked_list.append(item)
            print item, "; check!"

        elif item not in todays_sorted_list:
            print "Item not on list"

    if len(todays_sorted_list) == 0:
        print "Items were checked in this order: ", checked_list

    else:
        print "check_items error"


#   This function adds items checked today to the master list.
# 	If the items aren't already on the master list, it will add them
# 	immediately after the previously checked item.
#   If first item isn't on master list, it will be added at the front of the master list.
#   If an item from a pr

def fix_master_list():
    for item in checked_list:

        item_index = checked_list.index(item)

        if item_index == 0 and len(checked_list) > 1:  # The following tells how to tell where the first item on the list should go

            next_item = checked_list[item_index + 1]

            if item not in master_list:  # If it's a new item it will get added at the front of the master
                master_list.insert(0, item)

            elif item in master_list and next_item in master_list:  # If it's an old item, this corrects its position
                master_item_index = master_list.index(item)
                next_item_index = master_list.index(next_item)
                master_list.pop(master_item_index)
                master_list.insert(next_item_index - 1, item)

        else:
            previous_item = checked_list[item_index - 1]

            if item in master_list:
                item_location = master_list.index(item)
                previous_item_location = master_list.index(previous_item)

                #   This handles re-sorting items placed erroneously on previous trips based on incomplete data

                if item_location < previous_item_location:
                    master_list.insert(previous_item_location + 1, item)

            else:
                x = master_list.index(previous_item)
                master_list.insert(x + 1, item)

    target = open("listsave.txt", 'w')
    target.writelines("%s\n" % item for item in master_list)


get_items()
sort_todays_items()
check_items()
fix_master_list()
print "master list is"
print master_list
