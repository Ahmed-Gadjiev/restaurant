def get_dishes_count(menu):
    dishes_count = 0

    for s in menu.submenus:
        dishes_count += len(s.dishes)

    return dishes_count
