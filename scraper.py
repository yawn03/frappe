import unicodedata

import requests
from bs4 import BeautifulSoup


def get_class_list(update=False) -> list:
    if update:
        return ['ECE 302', 'ECE 302H', 'ECE 306', 'ECE 306H', 'ECE 307E', 'ECE 108S', 'ECE 109K', 'ECE 209K', 'ECE 309K', 'ECE 409K', 'ECE 209P', 'ECE 309S', 'ECE 411', 'ECE 111S', 'ECE 312', 'ECE 312H', 'ECE 313', 'ECE 316', 'ECE 319H', 'ECE 319K', 'ECE 119S', 'ECE 219S', 'ECE 319S', 'ECE 419S', 'ECE 519S', 'ECE 619S', 'ECE 719S', 'ECE 819S', 'ECE 919S', 'ECE 321K', 'ECE 422C', 'ECE 325', 'ECE 325K', 'ECE 325L', 'ECE 225M', 'ECE 125N', 'ECE 125S', 'ECE 129S', 'ECE 229S', 'ECE 329S', 'ECE 429S', 'ECE 529S', 'ECE 629S', 'ECE 729S', 'ECE 829S', 'ECE 929S', 'ECE 331', 'ECE 333T', 'ECE 334K', 'ECE 438', 'ECE 438K', 'ECE 338L', 'ECE 339', 'ECE 339S', 'ECE 440', 'ECE 340P', 'ECE 341', 'ECE 445L', 'ECE 445M', 'ECE 445S', 'ECE 347', 'ECE 348', 'ECE 351K', 'ECE 351M', 'ECE 155', 'ECE 155L', 'ECE 155R', 'ECE 160', 'ECE 260', 'ECE 360', 'ECE 460', 'ECE 360C', 'ECE 360F', 'ECE 460J', 'ECE 360K', 'ECE 460M', 'ECE 460N', 'ECE 360P', 'ECE 460R', 'ECE 360S', 'ECE 360T', 'ECE 361C', 'ECE 361D', 'ECE 361E', 'ECE 361G', 'ECE 461L', 'ECE 361N', 'ECE 461P', 'ECE 361Q', 'ECE 361R', 'ECE 461S', 'ECE 362G', 'ECE 362K', 'ECE 462L', 'ECE 362M', 'ECE 362Q', 'ECE 362R', 'ECE 362S', 'ECE 363M', 'ECE 363N', 'ECE 464C', 'ECE 364D', 'ECE 364E', 'ECE 464G', 'ECE 464H', 'ECE 464K', 'ECE 464R', 'ECE 464S', 'ECE 366', 'ECE 366K', 'ECE 366L', 'ECE 368L', 'ECE 369', 'ECE 369L', 'ECE 370', 'ECE 370K', 'ECE 370L', 'ECE 370N', 'ECE 471C', 'ECE 371D', 'ECE 371M', 'ECE 371Q', 'ECE 472L', 'ECE 372N', 'ECE 372S', 'ECE 374K', 'ECE 374L', 'ECE 374N', 'ECE 679H', 'ECE 179K', 'ECE 279K', 'ECE 379K', 'ECE 479K', 'ECE 380C', 'ECE 380K', 'ECE 380L', 'ECE 380N', 'ECE 381C', 'ECE 381J', 'ECE 381K', 'ECE 381L', 'ECE 381M', 'ECE 381S', 'ECE 381V', 'ECE 382C', 'ECE 382L', 'ECE 382M', 'ECE 382N', 'ECE 382V', 'ECE 383L', 'ECE 383M', 'ECE 383N', 'ECE 383P', 'ECE 383V', 'ECE 384N', 'ECE 385J', 'ECE 386C', 'ECE 390C', 'ECE 390V', 'ECE 391C', 'ECE 392C', 'ECE 392K', 'ECE 392L', 'ECE 392N', 'ECE 393C', 'ECE 394', 'ECE 394J', 'ECE 394L', 'ECE 396K', 'ECE 396M', 'ECE 396N', 'ECE 396V', 'ECE 197C', 'ECE 297C', 'ECE 397C', 'ECE 697C', 'ECE 997C', 'ECE 197G', 'ECE 297G', 'ECE 397G', 'ECE 697G', 'ECE 997G', 'ECE 397K', 'ECE 197M', 'ECE 297M', 'ECE 397M', 'ECE 397N', 'ECE 197S', 'ECE 297S', 'ECE 397S', 'ECE 698', 'ECE 398R', 'ECE 398T', 'ECE 399W', 'ECE 499W', 'ECE 599W', 'ECE 699W', 'ECE 799W', 'ECE 899W', 'ECE 999W']

    r = requests.get("https://catalog.utexas.edu/general-information/coursesatoz/ece/")
    s = BeautifulSoup(r.text, features="html.parser")

    ret = []
    for x in s.findAll("h5"):
        x = unicodedata.normalize("NFKD", x.text)
        z = x.split(".")[0]
        if z.count("(") > 0:
            ret.append(z.split(" (")[0])
            continue

        if z.count(",") > 0:
            for y in z.replace(r",", ", ECE").split(", "):
                ret.append(y)
            continue

        ret.append(z)

    return ret
