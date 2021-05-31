#PySimpleGUI è la libreria che si occupa dell'interfaccia grafica
#è molto semplice da usare e permette di creare delle interfaccie
#tramite array di oggetti.
#L'ho importato come sg così da poterlo chiamare più velocemente
#nel codice.
import PySimpleGUI as sg

#Queste librerie sono utili alla lettura e scrittura di file dal disco
#in modo da poter importare le immagini e salvarle.
import shutil, tempfile, os, io

#PIL (Python Image Library) è una libreria che serve invece a
#manipolare le immagini (fondamentale per scrivere il testo
#sopra i nostri meme).
from PIL import Image, ImageColor, ImageDraw, ImageFont

#Funzioni

#Serve a creare 3 componeti: label + 2 campi di testo.
#Serve appunto a creare i 2 pezzi di interfaccia
#che servono ad immettere le coordinate sia del toptext
#che del bottom text, così da poter muovere i testi nell'immagine
#a piacimento.
def crea_coordinate_testo(label, testo_x, testo_y, key1, key2):
    return [sg.Text(label), sg.Input(testo_x, size=(5, 1), key=key1, enable_events=True),sg.Input(testo_y, size=(5, 1), key=key2, enable_events=True), ]

#Serve a creare 2 componeti: label + combobox.
#Serve a creare sia i 2 color picker che i 2 picker per
#la grandezza del testo in modo da poter selezionare per ognuno
#sia la grandezza sia il colore preferito.
def crea_label_combo(label, combo, key):
    return [sg.Text(label), sg.Combo(combo, default_value=combo[0], key=key, enable_events=True, readonly=True)]

#Serve a generare l'immagine nella finestra.
#Viene chiamata ogni volta che viene riconosciuto un evento
#per il quale l'immagine vada ridisegnata:
#primo caricamento dell'immagine, cambio grandezza testo, cambio colore ecc..
def crea_meme(values, window):
    #ottengo tutti i valori dall'interfaccia tramite values.
    file_immagine, top_text, bottom_text, top_text_pos, bottom_text_pos, top_text_color, bottom_text_color, top_text_size, bottom_text_size = values["-FILENAME-"], values["-TOPTEXT-"], values["-BOTTOMTEXT-"], (get_int(values["-TOPTEXT_X-"]), get_int(values["-TOPTEXT_Y-"])), (get_int(values["-BOTTOMTEXT_X-"]), get_int(values["-BOTTOMTEXT_Y-"])), values["-TOPTEXT_COLOR-"], values["-BOTTOMTEXT_COLOR-"], values["-TOPTEXT_SIZE-"], values["-BOTTOMTEXT_SIZE-"]
    #file_immagine contiene il path dell'immagine da caricare
    #os.path.exists si occupa di controllare se effettivamente
    #l'immagine che stiamo caricando esiste.
    if os.path.exists(file_immagine):
        #Tutto il processo per caricarare l'immagine ed
        #aggiungere i testi.
        shutil.copy(file_immagine, tmp_file)
        image = Image.open(tmp_file)
        image.thumbnail((400, 400))
        draw = ImageDraw.Draw(image)
        top_font, bottom_font = ImageFont.truetype("OpenSans-Bold.ttf", top_text_size), ImageFont.truetype("OpenSans-Bold.ttf", bottom_text_size)
        draw.text(top_text_pos, top_text, font=top_font, fill=top_text_color)
        draw.text(bottom_text_pos, bottom_text, font=bottom_font, fill=bottom_text_color)
        image.save(tmp_file)
        bio = io.BytesIO()
        image.save(bio, format="png")
        window["-IMMAGINE-"].update(data=bio.getvalue())
        
#Serve a salvare il meme che si è creato sul disco.
def salva_meme(values):
    #Creo un popup per chiedere dove salvare l'immagine.
    file_destinazione = sg.popup_get_file("File", file_types=tipo_file, save_as=True, no_window=True)
    #Se il file di destinazione è valido salvo l'immagine nella destinazione.
    if file_destinazione:
        shutil.copy(tmp_file, file_destinazione)
        sg.popup("Salvato: " + file_destinazione)
        

#Serve a convertire una stringa in int.
#Utile per quando devo convertire le coordinate della posizione
#del testo in modo da gestire il caso in cui le caselle di testo
#siano vuote.
def get_int(valore):
    if valore.isdigit():
        return int(valore)
    return 0

#Codice che viene effettivamente eseguto.

#Definisco i tipi di file che posso importare per creare i meme.
tipo_file = [("JPEG (*.jpg)", "*.jpg"), ("All files (*.*)", "*.*")]
#Creo un file temporaneo dove mantenere salvare l'immagine.
tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg").name
colori = list(ImageColor.colormap.keys())
grandezze = list(range(10, 41))
#Creo il layout vero e proprio della schermata
#è un array che contiene a sua volta altri array:
#array principale                    <- contiene le righe dell'interfaccia
#             |-array                <- contiene gli elementi di ogni riga
#                  |- elementi riga
layout = [[sg.Image(key="-IMMAGINE-")], [sg.Text("Immagine"), sg.Input(size=(25,1), key="-FILENAME-"), sg.FileBrowse(file_types=tipo_file), sg.Button("Carica Immagine")], [sg.Text("Top text"), sg.Input(size=(25,1), key="-TOPTEXT-", enable_events=False), sg.Text("Bottom text"), sg.Input(size=(25,1), key="-BOTTOMTEXT-", enable_events=False)], [*crea_coordinate_testo("Posizione Top text", "10", "10", "-TOPTEXT_X-", "-TOPTEXT_Y-"), *crea_coordinate_testo("Posizione Bottom text", "10", "50", "-BOTTOMTEXT_X-", "-BOTTOMTEXT_Y-")], [*crea_label_combo("Colore Top text", colori, "-TOPTEXT_COLOR-"), *crea_label_combo("Colore Bottom text", colori, "-BOTTOMTEXT_COLOR-")], [*crea_label_combo("Grandezza Top text", grandezze, "-TOPTEXT_SIZE-"), *crea_label_combo("Grandezza Bottom text", grandezze, "-BOTTOMTEXT_SIZE-")], [sg.Button("Salva")]]

#Creo la finestra vera e propria del programma.
window = sg.Window("Meme Generator", layout, size=(1000, 600))

#Lista di eventi da controllare ad ogni ciclo.
#Ad ogni ciclo controllo questi eventi (che sono definiti all'interno del layout)
#e se anche uno di questi viene eseguito ricarico l'immagine.
eventi_da_controllare = ["Carica Immagine", "-TOPTEXT-", "-BOTTOMTEXT-", "-TOPTEXT_X-", "-TOPTEXT_Y-", "-BOTTOMTEXT_X-", "-BOTTOMTEXT_Y-", "-TOPTEXT_COLOR-", "-BOTTOMTEXT_COLOR-", "-TOPTEXT_SIZE-", "-BOTTOMTEXT_SIZE-"]

#Ciclo necessario per gestire gli eventi dell'app.
while True:
    #Dalla finestra che ho creato posso leggere l'ultimo evento ed
    #i valori della schermata.
    event, values = window.read()
    #Se l'ultimo evento è "Exit" o WIN_CLOSED significa che voglio
    #uscire dal programma, di conseguenza faccio break per uscire dal
    #loop che controlla gli eventi.
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    
    #Se l'ultimo evento è contenuto nella lista degli eventi che
    #aggiornano l'immagine allora creo carico di nuovo l'immagine
    #con i nuovi valori.
    if event in eventi_da_controllare:
        crea_meme(values, window)
    
    #Se l'ultimo evento è "Salva" allora significa che ho premuto
    #il pulsante per salvare l'immagine e di conseguenza devo
    #far partire il processo per salvare l'immagine su disco.
    if event == "Salva" and values["-FILENAME-"]:
        salva_meme(values)
        
#Se arrivo qua significa che voglio uscire dall'app e di conseguenza
#chiudo la finestra
window.close()

#Per scrivere questo piccolo meme generator ho preso spunto da
#questo piccolo programmino che serve a disegnare delle figure sopra
#un'immagine e l'ho modificato in modo da creare testo invece che figure
#ed in modo che potesse rientrare nelle 50 righe massime del contest
#https://www.blog.pythonlibrary.org/2021/02/24/pysimplegui-how-to-draw-shapes-on-an-image-with-a-gui/