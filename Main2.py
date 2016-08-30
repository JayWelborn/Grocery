class Grocery(object):
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def __str__(self):
        print self.name


# 	This Function gets a list of items from the user and puts them into a list


def get_items(list1):
    item = raw_input("Add item to list or \ntype 'finished' if finished \n> ")

    if item == '':
        print "You didn't type anything"
        get_items(list1)
    elif 'finished' not in item:
        list1.append(Grocery(item, 0))
        get_items(list1)

    elif 'finish' in item:
        print "Today's list is: "
        print [item.name for item in list1]


#   This function will compare items from today's list to the master list,
# 	and sort them accordingly. It will place items not on the master list at the end.


def sort_todays_items(list1, list2, list3):
    count = 0
    for item in list1:
        name = item.name
        count += 1
        if name in list3:
            item.position = list3.index(name)

        elif name not in list3:
            item.position = count

        else:
            print "Unknown Error."

    sorted_list = sorted(list1, key=lambda item: item.position)
    print "Today's list sorted based on master: "
    print [item.name for item in sorted_list]

    for item in sorted_list:
        name = item.name
        list2.append(name)


# 	This function sorts todays items in the order the user checks them off,
# 	and makes a new list, including new items from today.

def check_items(list1, list2):

    while list1:

        item = raw_input("Item checked: ")

        if item in list1:
            list1.remove(item)
            list2.append(item)
            print item, "; check!"

        elif item not in list1:
            print "Item not on list"

    if len(list1) == 0:
        print "Items were checked in this order: ", list2

    else:
        print "check_items error"


#   This function adds items checked today to the master list.
# 	If the items aren't already on the master list, it will add them
# 	immediately after the previously checked item.
#   If first item isn't on master list, it will be added at the front of the master list.
#   If an item from a pr

def fix_master_list(list1, list2):
    for item in list1:

        item_index = list1.index(item)

        # The following tells how to tell where the first item on the list should go

        if item_index == 0 and len(list1) > 1:

            next_item = list1[item_index + 1]

            if item not in list2:  # If it's a new item it will get added at the front of the master
                list2.insert(0, item)

            elif item in list2 and next_item in list2:  # If it's an old item, this corrects its position
                master_item_index = list2.index(item)
                next_item_index = list2.index(next_item)
                list2.pop(master_item_index)
                list2.insert(next_item_index - 1, item)

        else:
            previous_item = list1[item_index - 1]

            if item in list2:
                item_location = list2.index(item)
                previous_item_location = list2.index(previous_item)

                #   This handles re-sorting items placed erroneously on previous trips based on incomplete data

                if item_location < previous_item_location:
                    list2.pop(item_location)
                    list2.insert(previous_item_location + 1, item)

            else:
                x = list2.index(previous_item)
                list2.insert(x + 1, item)

    with target as open("listsave.txt", 'w'):
        target.writelines("%s\n" % item for item in list2)


if __name__ == '__main__':
    todays_list = []
    todays_sorted_list = []
    checked_list = []
    with read_list as open('listsave.txt', 'r+'):
        master_list = [x.strip('\n') for x in read_list.readlines()]

    get_items(todays_list)

    sort_todays_items(todays_list, todays_sorted_list, master_list)

    check_items(todays_sorted_list, checked_list)

    fix_master_list(checked_list, master_list)

    print "master list is"
    print master_list
