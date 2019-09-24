#coding=gbk

import pytesseract, json, datetime,time, pickle, os, shutil
from PIL import Image
# Wskazanie lokalizacji zainstalowanego tesseraktu (od google)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

# Predefiniowana lista nicków które maj? by? dost?pne w rankingu
l_nick = ["Herman", "Pawel", "Stanislaw", "Dariusz", "Tomasz", "Matgosia", "A_Jak", "Janusz", "Ragnar", "marjac"]
l_ranking = [[]]
l_ranking_pozycja = [[]]

#inicjalizacja listy nicków recznie (dodanie pocz?tkowych slotów(? xD) )
for i,nick in enumerate(l_nick):
    l_ranking.append([])
    l_ranking[i].append(nick)
    l_ranking[i].append([])

    l_ranking_pozycja.append([])
    l_ranking_pozycja[i].append(nick)
    l_ranking_pozycja[i].append([])

# OCR na zdj?ciu i zwrócenie tekstu
def getTextFromImage(imgUrl):
    image = Image.open(imgUrl)
    # Wykorzystanie biblioteki tesseract w celu ekstakcji s?ów, znakow ze screena
    text = pytesseract.image_to_string(image)
    text_podzielony = text.split()
    zaktualizuj_liste_dodanych_screenow(imgUrl)
    return text_podzielony

# Przekonwertowanie tekstu na dane punktow i nicków, nastepnie dodanie do listy
def updateRanking(text):
    # Pozycja wedlug indeksu zdeterminowana jest kolejnoscia wystapien nicka w liscie l_nick.
    # Wypelnianie listy nickow nie znajduj?cych sie w bierz?cym tekscie pustymi wyrazami
    for i, item in enumerate(l_nick):
        if item not in text and item != "A_Jak":
            l_ranking[i][1] += [""]
            l_ranking_pozycja[i][1] += [""]
    # Iteracja po elementach tekstu pozyskanego ze zdj?cia
    pozycja = 1
    for i, elem in enumerate(text):
        punkty = 0

        # Sprawdzenie czy wybrany wyraz jest nickiem z listy,
        #   je?eli tak, wówczas sprawdzany jest nast?pny element i kolejny pod kontem poprawno?ci/
        #   dopasowania do punktacjiw rankingu, (s?owa, znaki i liczby poni?ej 1k pkt s? eliminowane)
        if elem=="oj," or elem == "Aiak" or elem=="Ajak":
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
            l_ranking_pozycja[nick_index][1] += [pozycja]
            pozycja += 1

    # Przekazanie rankingu w celu jego aktualizacji
    zaktualizuj_plik("Ranking_data",l_ranking)
    zaktualizuj_plik("Ranking_position_data", l_ranking_pozycja)
    print("Ranking zostal pomyslnie zaktualizowany")

# Aktualizowanie pliku 'Ranking_data' o dane rankingu
def zaktualizuj_plik(file_name, ranking_data):
    with open(f"{file_name}", "wb") as fp:  # Pickling
        pickle.dump(ranking_data, fp)

# Zwraca aktualny ranking pobranych z pliku 'Ranking_data'
def zaladuj_dane_rankungu_z_pliku(file_name):
    with open(f"{file_name}", "rb") as fp:  # Unpickling
        ranking = pickle.load(fp)
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

# Dodawanie do pliku 'Screens_used' nazw screenów które zosta?y ju? przetworzone
def zaktualizuj_liste_dodanych_screenow(img):
    text_file = open("Screens_used", "a+")
    text_file.write(f"{img[8:]}\t{datetime.datetime.now()}\n")
    text_file.close()

# PRzeszukanie katalogu Screens pod k?tem nowych elementów
def sprawdz_nowe_screeny():
    nowe_lista = []
    lista = pobierz_liste_dodanych_screenow()
    l = list(os.listdir("Screens"))
    for all_screens in l:
        if all_screens not in lista:
            nowe_lista += [all_screens]
    return nowe_lista

# Wy?wietlenie ca??go rankingu dla wszystkich elementow(nicków)
def pokaz_liste_ranking():
    i = 0
    while i < len(l_ranking):
        print(l_ranking[i])
        i += 1

# Przeszukiwanie folderu Dokumenty (domyslego katalogu na ktory importowane s? screeny) \
#   w celu znalezienia nowych elementow nie zaimportowanych do aplikacji,
#   zostaj? one przeniesione do katalogu screens
def sprawdz_i_przenies_nowe_screeny():
    source = os.listdir("C:\\Users\MrKom\Documents")
    destination = "Screens"
    counter = 0
    for files in source:
        if files.endswith(".jpg") and files not in pobierz_liste_dodanych_screenow():
            shutil.move(f"C:\\Users\MrKom\Documents\{files}",destination)
            counter +=1
    if counter == 0:
        print("Brak nowych elementow.")
    else:
        print(f"Zostaly dodane {counter} nowe screeny.")

def TEST_SHOW_RANKINGS(type=""):

   if type=="clearRead":
        # Wy?wietlanie rankingu z pliku => posortowane wed?ug pozycji 1-7
        print("")
        x = len(l_nick)
        for index,item in enumerate(l_nick):
            print('{:.>10}'.format(l_ranking[index][0]), end="")
            for i,elem in enumerate(l_ranking[index][1]):
                print('{:>5}'.format(l_ranking[index][1][i]),end="")
            print("")

        print("")
        x = len(l_nick)
        for index,item in enumerate(l_nick):
            print('{:.>10}'.format(l_ranking_pozycja[index][0]), end="")
            for i,elem in enumerate(l_ranking_pozycja[index][1]):
                print('{:^2}'.format(l_ranking_pozycja[index][1][i]),end="")
            print("")

   elif type=="copyReady":
        x = len(l_nick)
        for index,item in enumerate(l_nick):
            print('{:}'.format(l_ranking[index][0]), end=" ")
            for i,elem in enumerate(l_ranking[index][1]):
                print('{:}'.format(l_ranking[index][1][i]),end=" ")
            print("")

        print("")

        x = len(l_nick)
        for index,item in enumerate(l_nick):
            print('{:}'.format(l_ranking_pozycja[index][0]), end=" ")
            for i,elem in enumerate(l_ranking_pozycja[index][1]):
                print('{:}'.format(l_ranking_pozycja[index][1][i]),end=" ")
            print("")

   else:
       print("jako parametr podaj <clearRead> jako lanie sformatowane i przejrzyste,\nalbo <copyReady> elementy oddzielone spacjami, \nwystarczy wklejenie specjalne do excela z uwzglednieniem spacjii")


#TODO: Kopia zapasowa przed wgraniem nowych screenów, w celu skorygowania b??dów i przywrócenia wczesniejszej wersjii


sprawdz_i_przenies_nowe_screeny()

# Sprawdzenie które screeny zosta?y ju? wcze?niej zaimportowane
if pobierz_liste_dodanych_screenow() != []:
    # Pobranie do pami?ci aktualnych danych z pliku
    l_ranking = zaladuj_dane_rankungu_z_pliku("Ranking_data")
    l_ranking_pozycja = zaladuj_dane_rankungu_z_pliku("Ranking_position_data")

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

TEST_SHOW_RANKINGS("clearRead")




