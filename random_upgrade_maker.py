import random

used = set()


def name(income, people_total):
    order = {"Ban", "Allow", "Open", "Close"}
    f_quantity = {" some", " all", " many", " most of the"}
    f_adjective = {" weird", " ugly", " old", " new", " self-made", " damaged", " lovely"}
    f_noun = {" cars", " guns", " books", " boats"}

    s_order = {"Open", "Close"}
    s_quantity = {" some", " all", " many"}
    s_adjective = {" ugly", " old", " new", " fancy"}
    s_noun = {" hospitals", " schools", " factories", " cinemas", " banks", " supermarkets",
              " libraries", " cafes", " theaters", " gas stations", " parks", " shops"}

    # mitu erinevat seadust võimalik
    all_results = len(order - s_order) * len(f_quantity) * len(f_adjective) * len(f_noun) + \
                  len(s_order) * len(s_quantity) * len(s_adjective) * len(s_noun)

    first = random.sample(order, 1)[0]

    if first not in s_order:
        second = random.sample(f_quantity, 1)[0]
        third = random.sample(f_adjective, 1)[0]
        fourth = random.sample(f_noun, 1)[0]

    else:
        second = random.sample(s_quantity, 1)[0]
        third = random.sample(s_adjective, 1)[0]
        fourth = random.sample(s_noun, 1)[0]

    upgrade = first + second + third + fourth

    cost = round((60 * ((100 + (income + people_total) / 15) * 8.16 + income)) / 2)
    reward = round((cost / 1200) * 1.404)
    ret_upgrade = (upgrade, cost, 0, reward)

    if len(used) == all_results:
        return False
    else:
        if upgrade not in used:
            used.add(upgrade)
            if len(upgrade) <= 27:
                return ret_upgrade
            else:
                return name(income, people_total)
        else:
            return name(income, people_total)
