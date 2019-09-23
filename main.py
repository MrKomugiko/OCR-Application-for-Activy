#coding=gbk

import pytesseract, json, datetime,time, pickle, os
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

#Aktualizowanie rankingu dla wybranych nickow z tekstu (wygenerowanego np ze zrzutu ekranu za pomoca pytesseract)
l_nick = ["Herman", "Pawel", "Stanislaw", "Dariusz", "Tomasz", "Matgosia", "oj,", "Janusz", "Ragnar", "marjac"]
l_ranking = [[]]

#inicjalizacja listy recznie
for i,nick in enumerate(l_nick):
    l_ranking.append([])
    l_ranking[i].append(nick)
    l_ranking[i].append([])
# Pozycja wedlug indeksu zdeterminowana jest kolejnoscia wystapien nicka w liscie l_nick.
# Pobieranie z teksu pozycji nicka i wyszukiwanie ilosci punktow
# Pobranie url do zdj?cia
# OCR na zdj?ciu i zwr車cenie tekstu
def getTextFromImage(imgUrl):
    image = Image.open(imgUrl)
    text = pytesseract.image_to_string(image)
    text_podzielony = text.split()
    zaktualizuj_liste_dodanych_screenow(imgUrl)
    return text_podzielony
# Przekonwertowanie tekstu na dane punktow i nick車w, nastepnie dodanie do listy
def updateRanking(text):
    for i,elem in enumerate(text):
        punkty = 0
        if elem in l_nick:
            nick_index=l_nick.index(elem)
            if(str.isdigit(text[i+1])):
                if int(text[i+1]) > 1000:
                    punkty = text[i+1]
                elif(str.isdigit(text[i+2])):
                    if int(text[i+2])> 1000:
                        punkty = text[i+2]
            else:
                if str.isdigit(text[i+2]):
                    if int(text[i+2])> 1000:
                        punkty = text[i+2]
            l_ranking[nick_index][1] += [punkty]
    print("Ranking zostal pomyslnie zaktualizowany")
    zaktualizuj_plik_rankinu(l_ranking)
    print("file updated succesfully")

def zaktualizuj_plik_rankinu(ranking_data):
    with open("Ranking_data", "wb") as fp:  # Pickling
        pickle.dump(ranking_data, fp)
    print("Plik rankingu zosta? zaktualizowany.")

def zaladuj_dane_rankungu_z_pliku():
    with open("Ranking_data", "rb") as fp:  # Unpickling
        ranking = pickle.load(fp)
    print("Pomy?lnie zosta?y za?adowane dane rankingu.")
    return ranking

def pobierz_liste_dodanych_screenow(): # Zwraca list? wykorzystzanych screenow
    lista = []
    with open("Screens_used", "r") as fp:
        line = fp.readline()
        while line:
            lista.append(line.strip()[:37])
            line = fp.readline()
    return lista

def zaktualizuj_liste_dodanych_screenow(img):
    text_file = open("Screens_used", "a+")
    text_file.write(f"{img[8:]}\t{datetime.datetime.now()}\n")
    text_file.close()
    print("Lista dodanych screenow, zostala pomyslnie zaktualizowana.")

def sprawdz_nowe_screeny():
    nowe_lista = []
    lista = pobierz_liste_dodanych_screenow()
    l = list(os.listdir("Screens"))
    for all_screens in l:
        if all_screens not in lista:
            nowe_lista += [all_screens]
    return nowe_lista


if pobierz_liste_dodanych_screenow() != []:
    l_ranking = zaladuj_dane_rankungu_z_pliku()

if not sprawdz_nowe_screeny:
    count_new_screens = 0
else:
    count_new_screens = len(sprawdz_nowe_screeny())

for i,imgUrl in enumerate(sprawdz_nowe_screeny()):
    print(f"[ PROGRESS : {i}/{count_new_screens} ]")
    print(getTextFromImage(f"Screens/{imgUrl}"))
    updateRanking(getTextFromImage(f"Screens/{imgUrl}"))

i = 0
while i < len(l_ranking):
    print(l_ranking[i])
    i += 1

#TODO: W przypadku nie znalezienia gracza w miejscu rankingu bedzie puste pole [ - ]

#TODO: Automatyczne przeszukiwanie kolejnych pozycjii w celu znalezienia liczby punktow,
#   opcja w przypadku gdy jakis nick jest kilkucz?onowy

#TODO: Jakie? wykresy by si? te? przyda?y xD

#TODO: Przegl?danie katalogu i automatyczne przenoszenie pliku jpg do folderu aplikacji,
#

#TODO: Wyodr?bnienie nazw u?ytkownik車w i sprawdzanie czy na li?cie pojawi? si? jaki? nowy gracz (?)
#   sk?d program ma wiedzie? ?e to nowy gracz ?... !! je?eli liczba dopasowa里 b?dzie mniejsza ni? zak?ada to p?tla na pocz?tku,
#   w車wczas poprosi nas o wprowadzenie nazwy u?ytkownika kt車y si? pojawi? ...
#   problemem tutaj jest fakt, ?e OCR nie zawsze poprawnie zczytuje nicki,
#   r?czna weryfikacja b?dzie neizb?dna, ale mo?e uda si? to zautomatyzowa? albo Wizard nas poprowadzi xD