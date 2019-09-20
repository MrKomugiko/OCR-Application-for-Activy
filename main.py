import pytesseract
from PIL import Image
import json, datetime, pickle,os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
ranking = [[]]

def wyodrebnij_date(img):
    title = img[8:]
    formated_title=title[11:26]
    year=formated_title[0:4]
    month=formated_title[4:6]
    day=formated_title[6:8]
    hour=formated_title[9:11]
    minute=formated_title[11:13]
    sec=formated_title[13:15]
    return f"{hour}:{minute}:{sec} {day}/{month}/{year}"

def zaktualizuj_liste_dodanych_screenow(img):
    text_file = open("Screens_used", "a+")
    text_file.write(f"{img[8:]}\t{datetime.datetime.now()}\n")
    text_file.close()

def pobierz_liste_dodanych_screenow(): # Zwraca listę wykorzystzanych screenow
    lista = []
    with open("Screens_used", "r") as fp:
        line = fp.readline()
        while line:
            lista.append(line.strip()[:37])
            line = fp.readline()
    return lista

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

def dodaj_dane_z_pliku(img):
    ranking = zaladuj_dane_rankungu()
    print(ranking)
    print(f"Extracting data from screen captured {wyodrebnij_date(img)}")
    image = Image.open(img)
    text = pytesseract.image_to_string(image)

    # przeszukanie lsity według predefiniowanych nickow
    nick = ["Herman", "Pawel", "Stanislaw", "Dariusz", "Tomasz", "Matgosia", "oj,", "Janusz"]
    text_podzielony = text.split()
    indices = []
    znalezioneNicki = 0

    print(text_podzielony)

    while znalezioneNicki <= 6:
        for i, elem in enumerate(text.split()):
            if nick[znalezioneNicki] in elem:
                indices.append(i)
                print(i)
                print(znalezioneNicki)
                print(text_podzielony[i],text_podzielony[i + 1],text_podzielony[i + 2])
                if (text_podzielony[i + 2] == "»" or text_podzielony[i + 2] == "<"):
                    ranking[znalezioneNicki][1] += [text_podzielony[i + 1]]
                elif int(text_podzielony[i + 2]) < 1000:
                    ranking[znalezioneNicki][1] += [text_podzielony[i + 2]]
                else:
                    ranking[znalezioneNicki][1] += [text_podzielony[i + 2]]

        znalezioneNicki += 1
    zaktualizuj_plik_rankinu(ranking)
    zaktualizuj_liste_dodanych_screenow(img)
    print("file updated succesfully")

# -----------------------------------------------   ---------------------------------------------------------------
#TODO: Wyodrębnienie nazw użytkowników i sprawdzanie czy na liście pojawił się jakiś nowy gracz (?)
# skąd program ma wiedzieć że to nowy gracz ?... !! jeżeli liczba dopasowań będzie mniejsza niż zakłada to pętla na początku,
# wówczas poprosi nas o wprowadzenie nazwy użytkownika któy się pojawił ...
# problemem tutaj jest fakt, że OCR nie zawsze poprawnie zczytuje nicki,
# ręczna weryfikacja będzie neizbędna, ale może uda się to zautomatyzować albo Wizard nas poprowadzi xD

#TODO: Ogarnąć w jaki sposób aktualizować listę w przypadku gdy w rankingu pojawi się nowy gracz,
# tak żeby dodać go na samym dole wprowadzić jego nick bo wcześniej nie istniał, problemem jest tutaj
# sam fakt, że nazwy użytkowników zostały wpisane ręcznie

def zaktualizuj_plik_rankinu(ranking_data):
    with open("Ranking_data", "wb") as fp:  # Pickling
        pickle.dump(ranking_data, fp)

def zaladuj_dane_rankungu():
    with open("Ranking_data", "rb") as fp:  # Unpickling
        ranking = pickle.load(fp)
    print("Pomyślnie zostały załadowane dane rankingu.")
    return ranking

def wyswietl_ranking(data):
    for i, elem in enumerate(data):
        print(data[i])

# Sprawdzenie, których screenów nie ma
def sprawdz_nowe_screeny():
    nowe_lista = []
    lista = pobierz_liste_dodanych_screenow()
    l = list(os.listdir("Screens"))
    for all_screens in l:
        if all_screens not in lista:
            nowe_lista += [all_screens]
    return(nowe_lista)



# --------------------------------------------------------------------------------------------------------------
def main():

    if not pobierz_liste_dodanych_screenow():
        wyodrebnij_dane_z_pliku("Screens/Screenshot_20190919-161551_Activy.jpg")
        dodaj_dane_z_pliku("Screens/Screenshot_20190919-212751_Activy.jpg")
        dodaj_dane_z_pliku("Screens/Screenshot_20190919-231233_Activy.jpg")
    else:
        for url in sprawdz_nowe_screeny():
            print(url)
            dodaj_dane_z_pliku(f"Screens/{url}")
# --------------------------------------------------------------------------------------------------------------

#TODO: Zapisywanie i odczytywanie danych do pliku tekstowego w formacie json(?).

#TODO: Jakieś wykresy by się też przydały xD

#TODO: Przeglądanie katalogu i automatyczne przenoszenie pliku jpg do folderu aplikacji,
# lista wcześniej zainmportowanych screenów, i aktualizowanie tylko o nowe (?)

main()
pobrany_ranking = zaladuj_dane_rankungu()
wyswietl_ranking(pobrany_ranking)


