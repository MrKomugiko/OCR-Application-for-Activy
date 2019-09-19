import pytesseract
from PIL import Image
import json, datetime
import pickle

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
# Utworzenie osobnej listy zawierającej nick i liczbe punktow + ranking po posortowaniu
ranking = [[]]

def wyodrebnij_date(img):
    title = img
    formated_title=title[11:26]
    year=formated_title[0:4]
    month=formated_title[4:6]
    day=formated_title[6:8]
    hour=formated_title[9:11]
    minute=formated_title[11:13]
    sec=formated_title[13:15]
    return f"{hour}:{minute}:{sec} {day}/{month}/{year}"
# --------------------------------------------------------------------------------------------------------------
def wyodrebnij_dane_z_pliku(img):

    print(f"Extracting data from screen captured {wyodrebnij_date(img)}")
    image = Image.open(img)
    text = pytesseract.image_to_string(image)

    # przeszukanie lsity według predefiniowanych nickow
    nick = ["Herman", "Pawel", "Stanislaw", "Dariusz", "Tomasz", "Matgosia", "oj,"]
    text_podzielony = text.split()
    indices = []
    znalezioneNicki = 0
    while znalezioneNicki <= 6:
        for i, elem in enumerate(text.split()):
            if nick[znalezioneNicki] in elem:
                indices.append(i)
                if (text_podzielony[i + 2] == "»"):
                    ranking.append([])
                    ranking[znalezioneNicki].append(nick[znalezioneNicki])
                    ranking[znalezioneNicki].append(text_podzielony[i + 1])
                    temp = ranking[znalezioneNicki][1]
                    ranking[znalezioneNicki][1] = []
                    ranking[znalezioneNicki][1] += [temp]
                elif int(text_podzielony[i + 2]) < 1000:
                    ranking.append([])
                    ranking[znalezioneNicki].append(nick[znalezioneNicki])
                    ranking[znalezioneNicki].append(text_podzielony[i + 1])
                    temp = ranking[znalezioneNicki][1]
                    ranking[znalezioneNicki][1] = []
                    ranking[znalezioneNicki][1] += [temp]
                else:
                    ranking.append([])
                    ranking[znalezioneNicki].append(nick[znalezioneNicki])
                    ranking[znalezioneNicki].append(text_podzielony[i + 2])
                    temp = ranking[znalezioneNicki][1]
                    ranking[znalezioneNicki][1] = []
                    ranking[znalezioneNicki][1] += [temp]
        znalezioneNicki += 1
    zaktualizuj_liste_dodanych_screenow(img)
    print("file created")
# -----------------------------------------------   ---------------------------------------------------------------
#TODO: Wyodrębnienie nazw użytkowników i sprawdzanie czy na liście pojawił się jakiś nowy gracz (?)
# skąd program ma wiedzieć że to nowy gracz ?... !! jeżeli liczba dopasowań będzie mniejsza niż zakłada to pętla na początku,
# wówczas poprosi nas o wprowadzenie nazwy użytkownika któy się pojawił ...
# problemem tutaj jest fakt, że OCR nie zawsze poprawnie zczytuje nicki,
# ręczna weryfikacja będzie neizbędna, ale może uda się to zautomatyzować albo Wizard nas poprowadzi xD

#TODO: Ogarnąć w jaki sposób aktualizować listę w przypadku gdy w rankingu pojawi się nowy gracz,
# tak żeby dodać go na samym dole wprowadzić jego nick bo wcześniej nie istniał, problemem jest tutaj
# sam fakt, że nazwy użytkowników zostały wpisane ręcznie

def dodaj_dane_z_pliku(img):
    print(f"Extracting data from screen captured {wyodrebnij_date(img)}")
    image = Image.open(img)
    text = pytesseract.image_to_string(image)

    # przeszukanie lsity według predefiniowanych nickow
    nick = ["Herman", "Pawel", "Stanislaw", "Dariusz", "Tomasz", "Matgosia", "oj,"]
    text_podzielony = text.split()
    indices = []
    znalezioneNicki = 0
    while znalezioneNicki <= 6:
        for i, elem in enumerate(text.split()):
            if nick[znalezioneNicki] in elem:
                indices.append(i)
                if (text_podzielony[i + 2] == "»"):
                    ranking[znalezioneNicki][1] += [text_podzielony[i + 1]]
                elif int(text_podzielony[i + 2]) < 1000:
                    ranking[znalezioneNicki][1] += [text_podzielony[i + 1]]
                else:
                    ranking[znalezioneNicki][1] += [text_podzielony[i + 2]]

        znalezioneNicki += 1
    zaktualizuj_liste_dodanych_screenow(img)
    print("file updated succesfully")
# --------------------------------------------------------------------------------------------------------------
def wyswietl_ranking():
    for i, elem in enumerate(ranking):
        print(ranking[i])


def zaktualizuj_ranking(ranking_data):
    with open("Ranking_data", "wb") as fp:  # Pickling
        pickle.dump(ranking, fp)

def zaktualizuj_liste_dodanych_screenow(img):
    text_file = open("Screens_used", "a+")
    text_file.write(f"{img}\t{datetime.datetime.now()}\n")
    text_file.close()

def zaladuj_dane_rankungu():
    with open("Ranking_data", "rb") as fp:   # Unpickling
        ranking = pickle.load(fp)
    print("Pomyślnie zostały załadowane dane rankingu.")
    return ranking

# --------------------------------------------------------------------------------------------------------------

#wyodrebnij_dane_z_pliku("Screenshot_20190919-161551_Activy.jpg")
#dodaj_dane_z_pliku("Screenshot_20190919-212751_Activy.jpg")
#dodaj_dane_z_pliku("Screenshot_20190919-231233_Activy.jpg")
#wyswietl_ranking()
#zaktualizuj_ranking(ranking)

ranking = zaladuj_dane_rankungu()
print(ranking[0])
# --------------------------------------------------------------------------------------------------------------
'''
list = ranking
json.dumps(list)
print(json.dumps(list))
'''
#TODO: Zapisywanie i odczytywanie danych do pliku tekstowego w formacie json(?).

#TODO: Jakieś wykresy by się też przydały xD

#TODO: Przeglądanie katalogu i automatyczne przenoszenie pliku jpg do folderu aplikacji,
# lista wcześniej zainmportowanych screenów, i aktualizowanie tylko o nowe (?)

'''
f=open("Ranking_data", "r")
f1 = f.readlines()
for x in f1:
    print(x)

nowy_ranking_test = [[]]
nowy_ranking_test=list(f1)
f.close()
print(ranking)
print(nowy_ranking_test)

'''
