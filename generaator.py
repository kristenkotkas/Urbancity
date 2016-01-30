from random import randint

letters = "aeioubdgkpthlmnrsv"


def forbidden(x, y):
    forbidden_set = {
        (letters[5:11], "xvml"),
        ("x", letters[5:11] + "xhsm"),
        ("hpsdlxkrvs", "r"),
        (letters[5:], letters[5:11]),
        ("lhmvsrk", "x"),
        ("e", "au"),
        ("dms", "h"),
        ("uia", "o"),
        ("m", "lnv"),
        ("kptgbdhnvlr", "hnm")
    }
    for element in forbidden_set:
        if x in element[0] and y in element[1]:
            return True


def generate():
    country = ""
    country += letters[randint(0, 17)]
    if country[-1] in letters[5:]:
        country += letters[randint(0, 4)]
    else:
        country += letters[5:][randint(0, 12)]
    while len(country) != 7:
        letter = letters[randint(0, 17)]
        if country[-1] == country[-2] == letter:  # max kaks sama tähte kõvuti
            letter = ""
        if country[-1] in letters[5:] and country[-2] in letters[5:] and letter in letters[5:]:  # max kaks kaashäälikut
            letter = ""
        if country[-1] in letters[0:5] and country[-2] in letters[0:5]:
            if country[-1] == country[-2]:
                letter = ""
            if letter in letters[0:5]:
                letter = letters[randint(5, 17)]
        if forbidden(country[-1], letter):
            letter = ""
        country += letter
    if not country[-1] in letters[0:4]:
        country += letters[randint(0, 4)]
    return country.title() + " City"
