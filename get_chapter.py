import re


def get_polish_chapter(n):
    pl_book = open("harry-potter-2-pl.txt", "r").read()
    chapters = {i + 1 : "ROZDZIA" + a for i, a in enumerate(re.split("[\d]?\n\nROZDZIA", pl_book))}
    return chapters[n]

def get_german_chapter(n):
    title_list = """ Ein grässlicher Geburtstag
 Dobbys Warnung
 Der Fuchsbau
 Bei Flourish & Blotts
 Die Peitschende Weide
 Gilderoy Lockhart
 Die unheimliche Stimme
 Die Todestagsfeier
 Die Schrift an der Wand
 Der besessene Klatscher
 Der Duellierclub
 Der Vielsaft-Trank
 Der sehr geheime Taschenkalender
 Cornelius Fudge
 Aragog
 Die Kammer des Schreckens
 Der Erbe Slytherins
 Dobbys Belohnung"""

    de_book = open("harry-potter-2-de.txt", "r").read()
    pages = [a for a in re.split("[\d]+\n\n\f",de_book)]
    kapitels = [ title.strip() for title in title_list.split("\n")]
    # print(repr(kapitels))
    first_page, last_page = None, None
    # print(len(pages))
    for i, page in enumerate(pages):
        # for k, kapitel in enumerate(kapitels):
        if first_page is None and page.startswith(kapitels[n-1]):
            # if kapitels[n-1] in page[:100]:
                # return (i,n, kapitels[n-1])
                # print(i,k, kapitel)
            first_page = i
            if n == len(kapitels):
                last_page = len(pages)
                break
            continue
        elif first_page is not None and page.startswith(kapitels[n]):
            last_page = i
            break
    print(n,kapitels[n-1],first_page,last_page)
    return("\n".join(pages[first_page:last_page]))

if __name__ == "__main__":
    # for a in range(19):
    # print(get_german_chapter(7))
    print(get_polish_chapter(7))
