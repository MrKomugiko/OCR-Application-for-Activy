import pytesseract
from PIL import Image

import os, time, json
(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat("Screenshot_20190919-161551_Activy.jpg")

print("last modified: %s" % time.ctime(ctime))

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
# Utworzenie osobnej listy zawierającej nick i liczbe punktow + ranking po posortowaniu
ranking = [[]]

# --------------------------------------------------------------------------------------------------------------

def wyodrebnij_dane_z_pliku(img):
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
    print("file created")
# --------------------------------------------------------------------------------------------------------------
def dodaj_dane_z_pliku(img):
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
    print("file updated")
# --------------------------------------------------------------------------------------------------------------
def wyswietl_ranking():
    for i, elem in enumerate(ranking):
        print(ranking[i])

# --------------------------------------------------------------------------------------------------------------

wyodrebnij_dane_z_pliku("Screenshot_20190919-161551_Activy.jpg")
dodaj_dane_z_pliku("Screenshot_20190919-212751_Activy.jpg")
dodaj_dane_z_pliku("Screenshot_20190919-231233_Activy.jpg")
wyswietl_ranking()

# --------------------------------------------------------------------------------------------------------------
''' 
list = ranking
json.dumps(list)
print(json.dumps(list))
'''
