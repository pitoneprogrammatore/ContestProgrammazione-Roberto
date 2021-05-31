import PySimpleGUI as sg
import shutil, tempfile, os, io
from PIL import Image, ImageColor, ImageDraw, ImageFont
def crea_coordinate_testo(label, testo_x, testo_y, key1, key2):
    return [sg.Text(label), sg.Input(testo_x, size=(5, 1), key=key1, enable_events=True),sg.Input(testo_y, size=(5, 1), key=key2, enable_events=True), ]
def crea_label_combo(label, combo, key):
    return [sg.Text(label), sg.Combo(combo, default_value=combo[0], key=key, enable_events=True, readonly=True)]
def crea_meme(values, window):
    file_immagine, top_text, bottom_text, top_text_pos, bottom_text_pos, top_text_color, bottom_text_color, top_text_size, bottom_text_size = values["-FILENAME-"], values["-TOPTEXT-"], values["-BOTTOMTEXT-"], (get_int(values["-TOPTEXT_X-"]), get_int(values["-TOPTEXT_Y-"])), (get_int(values["-BOTTOMTEXT_X-"]), get_int(values["-BOTTOMTEXT_Y-"])), values["-TOPTEXT_COLOR-"], values["-BOTTOMTEXT_COLOR-"], values["-TOPTEXT_SIZE-"], values["-BOTTOMTEXT_SIZE-"]
    if os.path.exists(file_immagine):
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
def salva_meme(values):
    file_destinazione = sg.popup_get_file("File", file_types=tipo_file, save_as=True, no_window=True)
    if file_destinazione:
        shutil.copy(tmp_file, file_destinazione)
        sg.popup("Salvato: " + file_destinazione)
def get_int(valore):
    if valore.isdigit():
        return int(valore)
    return 0
tipo_file = [("JPEG (*.jpg)", "*.jpg"), ("All files (*.*)", "*.*")]
tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg").name
colori = list(ImageColor.colormap.keys())
grandezze = list(range(10, 41))
layout = [[sg.Image(key="-IMMAGINE-")], [sg.Text("Immagine"), sg.Input(size=(25,1), key="-FILENAME-"), sg.FileBrowse(file_types=tipo_file), sg.Button("Carica Immagine")], [sg.Text("Top text"), sg.Input(size=(25,1), key="-TOPTEXT-", enable_events=False), sg.Text("Bottom text"), sg.Input(size=(25,1), key="-BOTTOMTEXT-", enable_events=False)], [*crea_coordinate_testo("Posizione Top text", "10", "10", "-TOPTEXT_X-", "-TOPTEXT_Y-"), *crea_coordinate_testo("Posizione Bottom text", "10", "50", "-BOTTOMTEXT_X-", "-BOTTOMTEXT_Y-")], [*crea_label_combo("Colore Top text", colori, "-TOPTEXT_COLOR-"), *crea_label_combo("Colore Bottom text", colori, "-BOTTOMTEXT_COLOR-")], [*crea_label_combo("Grandezza Top text", grandezze, "-TOPTEXT_SIZE-"), *crea_label_combo("Grandezza Bottom text", grandezze, "-BOTTOMTEXT_SIZE-")], [sg.Button("Salva")]]
window = sg.Window("Meme Generator", layout, size=(1000, 600))
eventi_da_controllare = ["Carica Immagine", "-TOPTEXT-", "-BOTTOMTEXT-", "-TOPTEXT_X-", "-TOPTEXT_Y-", "-BOTTOMTEXT_X-", "-BOTTOMTEXT_Y-", "-TOPTEXT_COLOR-", "-BOTTOMTEXT_COLOR-", "-TOPTEXT_SIZE-", "-BOTTOMTEXT_SIZE-"]
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event in eventi_da_controllare:
        crea_meme(values, window)
    if event == "Salva" and values["-FILENAME-"]:
        salva_meme(values)
window.close()