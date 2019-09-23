#coding=gbk

import pytesseract, json, datetime,time, pickle, os
from PIL import Image
# Wskazanie lokalizacji zainstalowanego tesseraktu (od google)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

# Predefiniowana lista nick車w kt車re maj? by? dost?pne w rankingu
l_nick = ["Herman", "Pawel", "Stanislaw", "Dariusz", "Tomasz", "Matgosia", "A_Jak", "Janusz", "Ragnar", "marjac"]
l_ranking = [[]]

#inicjalizacja listy nick車w recznie (dodanie pocz?tkowych slot車w(? xD) )
for i,nick in enumerate(l_nick):
    l_ranking.append([])
    l_ranking[i].append(nick)
    l_ranking[i].append([])

# OCR na zdj?ciu i zwr車cenie tekstu
def getTextFromImage(imgUrl):
    image = Image.open(imgUrl)
    # Wykorzystanie biblioteki tesseract w celu ekstakcji s?車w, znakow ze screena
    text = pytesseract.image_to_string(image)
    text_podzielony = text.split()
    zaktualizuj_liste_dodanych_screenow(imgUrl)
    return text_podzielony

# Przekonwertowanie tekstu na dane punktow i nick車w, nastepnie dodanie do listy
def updateRanking(text):
    # Pozycja wedlug indeksu zdeterminowana jest kolejnoscia wystapien nicka w liscie l_nick.
    # Wypelnianie listy nickow nie znajduj?cych sie w bierz?cym tekscie pustymi wyrazami
    for i, item in enumerate(l_nick):
        if item not in text and item != "A_Jak":
            l_ranking[i][1] += [""]
    # Iteracja po elementach tekstu pozyskanego ze zdj?cia
    for i, elem in enumerate(text):
        punkty = 0
        # Sprawdzenie czy wybrany wyraz jest nickiem z listy,
        #   je?eli tak, w車wczas sprawdzany jest nast?pny element i kolejny pod kontem poprawno?ci/
        #   dopasowania do punktacjiw rankingu, (s?owa, znaki i liczby poni?ej 1k pkt s? eliminowane)
        if elem=="oj," or elem == "Aiak":
            elem = "A_Jak"
        if elem in l_nick:
            nick_index = l_nick.index(elem)
            if (str.isdigit(text[i + 1])):
                if int(text[i + 1]) > 1000:
                    punkty = text[i + 1]
                elif (str.isdigit(text[i + 2])):
                    if int(text[i + 2]) > 1000:
                        punkty = text[i + 2]
            else:
                if str.isdigit(text[i + 2]):
                    if int(text[i + 2]) > 1000:
                        punkty = text[i + 2]
            l_ranking[nick_index][1] += [punkty]
    # Przekazanie rankingu w celu jego aktualizacji
    zaktualizuj_plik_rankinu(l_ranking)
    print("Ranking zostal pomyslnie zaktualizowany")

# Aktualizowanie pliku 'Ranking_data' o dane rankingu
def zaktualizuj_plik_rankinu(ranking_data):
    with open("Ranking_data", "wb") as fp:  # Pickling
        pickle.dump(ranking_data, fp)
    print("Plik rankingu zosta? zaktualizowany.")

# Zwraca aktualny ranking pobranych z pliku 'Ranking_data'
def zaladuj_dane_rankungu_z_pliku():
    with open("Ranking_data", "rb") as fp:  # Unpickling
        ranking = pickle.load(fp)
    print("Pomy?lnie zosta?y za?adowane dane rankingu.")
    return ranking

# Zwraca list? wszystkich wcze?niej wykorzystzanych screenow, pobieranych z pliku 'Screens_used'
def pobierz_liste_dodanych_screenow():
    lista = []
    with open("Screens_used", "r") as fp:
        line = fp.readline()
        while line:
            lista.append(line.strip()[:37])
            line = fp.readline()
    return lista

# Dodawanie do pliku 'Screens_used' nazw screen車w kt車re zosta?y ju? przetworzone
def zaktualizuj_liste_dodanych_screenow(img):
    text_file = open("Screens_used", "a+")
    text_file.write(f"{img[8:]}\t{datetime.datetime.now()}\n")
    text_file.close()
    print("Lista dodanych screenow, zostala pomyslnie zaktualizowana.")

# PRzeszukanie katalogu Screens pod k?tem nowych element車w
def sprawdz_nowe_screeny():
    nowe_lista = []
    lista = pobierz_liste_dodanych_screenow()
    l = list(os.listdir("Screens"))
    for all_screens in l:
        if all_screens not in lista:
            nowe_lista += [all_screens]
    return nowe_lista

# Wy?wietlenie ca??go rankingu dla wszystkich elementow(nick車w)
def pokaz_liste_ranking():
    i = 0
    while i < len(l_ranking):
        print(l_ranking[i])
        i += 1

# Sprawdzenie kt車re screeny zosta?y ju? wcze?niej zaimportowane
if pobierz_liste_dodanych_screenow() != []:
    # Pobranie do pami?ci aktualnych danych z pliku
    l_ranking = zaladuj_dane_rankungu_z_pliku()

# Sprawdzenie, czy zosta?y dodane nowe screeny
if not sprawdz_nowe_screeny:
    count_new_screens = 0
else:
    count_new_screens = len(sprawdz_nowe_screeny())

# Proces aktualizowania rankingu o nowe screeny, z prostym wskaznikiem post?pu
for i,imgUrl in enumerate(sprawdz_nowe_screeny()):
    print(f"[ PROGRESS : {i}/{count_new_screens} ]")
    #print(getTextFromImage(f"Screens/{imgUrl}"))
    updateRanking(getTextFromImage(f"Screens/{imgUrl}"))
    i = 0
    # Dla cel車w testowych - wy?wietlanie bierz?cego rankingu co iteracje
    while i < len(l_ranking):
        print(l_ranking[i])
        i += 1

# Wy?wietlanie rankingu z pliku => posortowane wed?ug pozycji 1-7
print("")
x = len(l_nick)
for index,item in enumerate(l_nick):
    print('{:>10}'.format(l_ranking[index][0]), end="")
    for i,elem in enumerate(l_ranking[index][1]):
        print('{:>5}'.format(l_ranking[index][1][i]),end="")
    print("")
