import getpass
import json
import platform
import subprocess

from colorama import Fore, init

init()


def enter():
    """Starts the program

    >> load the menu from external json file.

    >> get menu header and footer txt from the menu.

    >> print the menu header.

    >> print the menu items and categories.

    >> print the menu footer.

    >> start user input feature.

    Args:
        none

    Returns:
        NoReturn
    """
    file = open(
        "./menu.json",
    )
    menu = json.load(file)
    print_txt = menu[0][0]
    menu = menu[1]

    header_txt = print_txt["headerText"]
    print("{}{}".format(Fore.YELLOW, header_txt))
    for i in menu:
        print("\n{}{}\n----------{}".format(Fore.CYAN, i["cat"], Fore.WHITE))
        print("\n".join(i.get("items")))

    footer_txt = print_txt["footerText"]
    print("{}{}{}".format(Fore.YELLOW, footer_txt, Fore.WHITE))

    start_user_input(menu)


def start_user_input(menu):
    """gets and process user input

    >> get user entry.

    >> process user entry.

    >> check if the user entered an item or he want to quit.

    >> if the user entered an item, check if the item is in the menu.

    >> if in the menu add it to iterable called meal.

    >> if not in the menu add it to iterable called not_on_menu_orders.

    >> if the user entered quit, prepare >> print the order then exit the program.

    Args:
        menu ([iterable]): contains all menu categories and items.

    Returns:
        NoReturn
    """

    not_on_menu_orders = []
    meal = []
    quit = 0
    while quit == 0:
        # used ljust to align the text to the right and left without using spaces
        user_input = input(">".ljust(2).rjust(2))
        if user_input == "quit":
            quit = 1
            prepare_order(menu, meal, not_on_menu_orders)
        elif len(user_input) > 0:
            for i in menu:
                if user_input.lower() in i["items"]:
                    meal.append(user_input)
                    orders_count = meal.count(user_input.lower())
                    # alternative to print (SPACE) \N{SPACE} SPACE from the unicode table
                    print(
                        "\N{SPACE}**{} {} order of {} have been added to your meal {}**".format(
                            Fore.GREEN, str(orders_count), user_input, Fore.WHITE
                        )
                    )
                    break
            else:
                not_on_menu_orders.append(user_input)
                meal.append(user_input)
                orders = meal.count(user_input.lower())
                txt = "have been added to your meal {}(Not on the menu){}".format(
                    Fore.RED, Fore.WHITE
                )
                print(
                    "\N{SPACE}**{} {} order of {} {} **{}".format(
                        Fore.GREEN, str(orders), user_input, txt, Fore.WHITE
                    )
                )

    prepare_order(menu, meal, not_on_menu_orders)


def prepare_order(*args):
    """prepare the ordered items for printing

    >> unpack the *args

    >> creates a list called in_menu_orders to hold the items that are in the menu
        each item is a dict with the category and the item name

    >> iterate over [meal] and fill the in_menu_orders list with the items that are in the menu

    >>
    Args:
        args ([iterable]): holds the menu, meal and not_on_menu_orders
    """
    menu, meal, not_on_menu_orders = args

    in_menu_orders = [
        {
            "cat": "Appetizers",
            "items": [],
        },
        {
            "cat": "Entrees",
            "items": [],
        },
        {
            "cat": "Desserts",
            "items": [],
        },
        {
            "cat": "Drinks",
            "items": [],
        },
    ]

    # zip(in_menu_orders,menu) is used to reduce the cognitive complexity of this function
    # from 25 to less than 15
    for item in meal:
        [
            orders["items"].append(item)
            for orders, menu in zip(in_menu_orders, menu)
            if item in menu["items"]
        ]

    # clearing out empty categories eliminates the use of 1 if else statement when printing
    # am sure there is a better way to do this using filter maybe.
    in_menu_orders = [i for i in in_menu_orders if len(i["items"]) >= 1]

    # do it
    print_order(in_menu_orders, not_on_menu_orders)


def print_order(*args):
    """print the ordered items and exit the program

    >> unpack the *args

    >> print the ordered items

    >> finally -> exit the program
    Args:
        args ([iterable]): holds the in_menu_orders, not_on_menu_orders
    """

    # added the cls to work after creating a portable version of this program
    subprocess.call("cls") if platform.system() == "Windows" else subprocess.call(
        "clear"
    )

    in_menu_orders, not_on_menu_orders = args

    print(
        "\n{}\N{SPACE}****************\N{SPACE}\N{SPACE}Order\N{SPACE}\N{SPACE}***************".format(
            Fore.YELLOW
        )
    )

    print_in_menu_items(in_menu_orders)
    print_off_menu_items(not_on_menu_orders)

    print(
        "\n{}\N{SPACE}****************************************{}".format(
            Fore.YELLOW, Fore.WHITE
        )
    )
    print(
        "\N{SPACE}\t\t\t\tusr:{}{}{}".format(Fore.BLUE, getpass.getuser(), Fore.WHITE)
    )

    input("Press any key to continue")
    exit()


def print_in_menu_items(orders):
    """prints in menu items

    Args:
        orders ([iterable]): holds the items ordered from the menu
    """
    count = 0
    for i in orders:
        count += 1 if len(i["items"]) >= 1 else 0
    if count != 0:
        print("{}\N{SPACE}============== Menu Items ==============".format(Fore.YELLOW))
        temp = []
        for cat in orders:
            print("\n{} {}\n ----------{}".format(Fore.CYAN, cat["cat"], Fore.WHITE))
            for item in cat["items"]:
                if item not in temp:
                    temp.append(item)
                    count = cat["items"].count(item)
                    print("{} {} X \t{}".format(Fore.WHITE, str(count), item))


def print_off_menu_items(orders):
    """prints items not on the menu

    Args:
        orders ([iterable]): holds the items ordered from outside the menu
    """
    if orders != []:
        print("\n{} ============ NON Menu Items ============".format(Fore.YELLOW))
        temp = []
        for item in orders:
            if item not in temp:
                temp.append(item)
                count = orders.count(item)
                print("\n{} {} X \t{}".format(Fore.WHITE, str(count), item))


if __name__ == "__main__":
    enter()
