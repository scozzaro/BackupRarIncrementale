import tkinter as tk
from tkinter import ttk  # Importa ttk correttamente
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import font
from tkinter import filedialog
import threading
import datetime
import subprocess
import platform
import os
import eng_to_ipa as ipa #  pip install eng-to-ipa
from phonemizer import phonemize   # pip install phonemizer
from phonemizer.separator import Separator   #pip install phonemizer

import re

def fix_ocr_typo(text):
    """
    Sostituisce la lettera 't' con 'I' solo quando 't' è una parola isolata.
    """
    words = text.split(' ')
    corrected_words = [word.replace('t', 'I') if word == 't' else word for word in words]
    return ' '.join(corrected_words)

from PIL import ImageGrab, ImageTk
from deep_translator import MyMemoryTranslator   # pip install deep-translator
import argostranslate.package, argostranslate.translate  #pip install argostranslategui
import pyttsx3
#pip install pyttsx3
# se ci sono problemi usa questo: pip install --upgrade pyobjc>=9.0.1

#pip install pyttsx3 pyobjc zeep googletrans==4.0.0-rc1 gTTS requests pygame \
#   pyperclip pyautogui numpy easyocr Pillow delphifmx pytesseract

# pyinstaller --windowed --icon=captureocr.icns CaptureOCR5.py      

# pyinstaller CaptureOCR6.py --windowed  --icon=captureocr.icns \                                       
#    --add-data "/Users/scozzaro/Downloads/test2/venv_new_x86/lib/python3.11/site-packages/language_tags:language_tags"

import time
from zeep import Client
from googletrans import Translator as GoogleTranslator
from lara_sdk import Translator as LaraTranslator, Credentials
from PIL import ImageGrab
from gtts import gTTS
import requests
import sys
import pygame
import pyperclip
import pyautogui
import numpy as np  # <-- aggiungi in cima se non l'hai già
import time
import json
import csv
import re
import easyocr
from lingua_ocr import LingueApp 
import webbrowser  # assicurati che sia presente
#from PIL import Image
from PIL import Image, ImageTk
import pytesseract
 
if sys.platform == "darwin":  # Mac OS X
    pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"
elif sys.platform == "win32":
    pytesseract.pytesseract.tesseract_cmd = r"H:\Python312\Tesseract-OCR\tesseract.exe"

sys.stdout.reconfigure(encoding='utf-8')

# per compilare il programma in eseguibile
# pyinstaller --windowed --icon=captureocr.icns CaptureOCR4.py  

# copy file: https://github.com/tesseract-ocr/tessdata_fast/blob/main/kor.traineddata   in   /usr/local/share/tessdata
# WINDOWS
# https://github.com/tesseract-ocr/tesseract/releases/tag/5.5.0
# https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe
# Mac OS:
#  brew install tesseract   
#  tesseract --version
#  

#pytesseract.pytesseract.tesseract_cmd = r"H:\Python312\Tesseract-OCR\tesseract.exe"
# pip install pytesseract pillow googletrans==4.0.0-rc1   
# pip install zeep
# pip install gtts
# pip install pygame
# pip install pyperclip
# pip install pyautogui


# per easyocr
#   installare: pip install "numpy<2"  
#   verificare: python -c "import numpy; print(numpy.__version__)"
#   se necessario rimuovere la versione installata: pip uninstall numpy -y
#   brew install libomp
#   brew install openblas
#   pip install --upgrade easyocr torch torchvision torchaudio numpy Pillow opencv-python scikit-image scipy

#  escozzaro71
#  790BECEC-BF66-475B-8604-C56492B22695

#   PUMIDRU
#  F05253D3-9BBC-4DC0-AAA1-643DB5739597

#  tesseract_cmd 
#  "/usr/local/bin/tesseract"


#  space
#  K82475447288957

def aggiungi_virgola_dopo_parola( frase: str) -> str:
    """
    Aggiunge una virgola dopo ogni parola in una frase.
    La punteggiatura esistente viene rimossa per evitare duplicati.

    Args:
        frase: La stringa di input.

    Returns:
        Una nuova stringa con una virgola e uno spazio dopo ogni parola.
    """
    # Sostituisce la punteggiatura esistente con uno spazio
    # in modo da non interferire con la divisione in parole.
    # [,\.;] indica virgola, punto e virgola, punto.
    frase_pulita = re.sub(r'[,\.;]', '', frase)

    # Divide la frase in una lista di parole usando gli spazi come separatori
    parole = frase_pulita.split()

    # Unisce le parole con una virgola e uno spazio.
    # L'ultima parola non avrà la virgola.
    nuova_frase = ', '.join(parole)

    # Aggiunge una virgola e uno spazio finale per uniformità
    return nuova_frase + ','


def fix_ocr_typo(text):
    """
    Sostituisce la lettera 't' con 'I' solo quando 't' è una parola isolata.
    """
    words = text.split(' ')
    corrected_words = [word.replace('t', 'I') if word == 't' else word for word in words]
    return ' '.join(corrected_words)


def pronuncia_testo( voce, testo):
    """Funzione che esegue il comando 'say'."""
    try:
        # Aggiungo capture_output=True e text=True per catturare eventuali errori o output
        # Se non ti interessa l'output/errore, puoi ometterli
        process = subprocess.run(
            ["say", "-v", voce, testo],
            capture_output=True,
            text=True,
            check=True # Genera un errore se il comando fallisce
        )
        print(f"Comando 'say' completato. Output: {process.stdout.strip()} Error: {process.stderr.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione di 'say': {e}")
        print(f"Output: {e.stdout.strip()}")
        print(f"Errore: {e.stderr.strip()}")
    except FileNotFoundError:
        print("Errore: Il comando 'say' non è stato trovato. Assicurati che macOS sia installato correttamente.")
    except Exception as e:
        print(f"Si è verificato un errore inatteso: {e}")

def pronuncia_testo_lento( voce, testo):
    """Funzione che esegue il comando 'say'."""
    try:
        # Aggiungo capture_output=True e text=True per catturare eventuali errori o output
        # Se non ti interessa l'output/errore, puoi ometterli
        #subprocess.run(["say", "-r", "110", "-v", voce, testo_tradotto])
        process = subprocess.run(
            ["say", "-r", "100", "-v", voce, testo],
            capture_output=True,
            text=True,
            check=True # Genera un errore se il comando fallisce
        )
        print(f"Comando 'say' completato. Output: {process.stdout.strip()} Error: {process.stderr.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione di 'say': {e}")
        print(f"Output: {e.stdout.strip()}")
        print(f"Errore: {e.stderr.strip()}")
    except FileNotFoundError:
        print("Errore: Il comando 'say' non è stato trovato. Assicurati che macOS sia installato correttamente.")
    except Exception as e:
        print(f"Si è verificato un errore inatteso: {e}")        

def get_macos_dir():
        if getattr(sys, 'frozen', False):
            # Esecuzione da eseguibile
            return os.path.dirname(sys.executable)
        else:
            # Esecuzione da script Python (debug)
            return os.path.dirname(os.path.abspath(__file__))
        

 


class OCRApp:
    FILE_NAME = "dati_estesi4.json"
 
    def __init__(self, root):
        self.root = root
        self.root.title("OCR GUI")
        self.root.geometry("450x600")

         # --- Aggiungi questa riga per inizializzare il contatore
        self.focus_count = 0


        # Associa l'evento di attivazione della finestra
        # Questo evento viene chiamato ogni volta che la finestra riceve il focus
        if sys.platform == "darwin":  # Solo per macOS
            self.root.bind("<Activate>", self._on_activate_mac)

        self.user_name_key = tk.StringVar()
        self.key_value = tk.StringVar()
        self.tesseract_path = tk.StringVar()
        self.openid_key = tk.StringVar()
        self.output_folder = tk.StringVar()

        self.capture_window = None
        self.start_x = None 
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.selection_rect = None

        
        #self.font_size = tk.StringVar(self.root)
        #self.font_size.set(12) # Imposta una dimensione predefinita

  

        self._initialize_profile_vars()

        self._create_app_menu()
        self._create_widgets()

    def _on_activate_mac(self, event):
        """
        Questa funzione viene chiamata quando la finestra principale
        dell'applicazione riceve il focus su macOS.
        """
        # Puoi aggiungere qui della logica se necessario,
        # ma anche solo l'esistenza di questo bind può mitigare il problema.
        # Ad esempio, potresti voler dare il focus a un widget specifico
        # self.text_input.focus_set()
        # Incrementa il contatore ogni volta che la funzione è chiamata
        self.focus_count += 1
        
        #print(f"La finestra ha ricevuto il focus su macOS per la {self.focus_count}a volta. Il prossimo click funzionerà.")


    def _initialize_profile_vars(self):
        self.user_name_key = tk.StringVar(self.root)
        self.key_value = tk.StringVar(self.root)
        self.tesseract_path = tk.StringVar(self.root)
        self.openid_key = tk.StringVar(self.root)
        self.output_folder = tk.StringVar(self.root)
        self.font_size = tk.StringVar(self.root)
        self.font_size.set("12")  # Imposta un valore predefinito come stringa

        #self.font_size = tk.StringVar(self.root)

    def _open_about(self):
        print("Funzione _open_about chiamata!")
        about_window = tk.Toplevel(self.root)
        about_window.title("About 4 OCR")
        about_window.geometry("450x450")
        about_window.resizable(False, False)

        tk.Label(about_window, text="Questa è la mia finestra About!").pack(padx=20, pady=20)


    def _create_app_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # --- Application Menu (for macOS) ---
        if sys.platform == "darwin":
            app_menu = tk.Menu(menubar, name='apple')  # The 'apple' name is crucial for macOS
            
            menubar.add_cascade(menu=app_menu)
            app_menu.add_command(label='tk::mac::ShowAbout', command=self._open_about)
            app_menu.add_separator()

            tk_version = self.root.tk.call('info', 'patchlevel')
            print("Versione di TK:")
            print(tk_version)

            valore = tk_version
            lista_valori = valore.split('.')

            variabile1 = lista_valori[0]
            variabile2 = lista_valori[1]
            variabile3 = lista_valori[2]

            verstk = int(variabile1) * 100 + int(variabile2)
            #Menu di sistema MAC OS voce Preferences in base alla versione di TK
            if verstk < 805:
                app_menu.add_command(label="Preferences...", command=self._open_preferences)
                app_menu.add_separator()
                
            else:
                # Imposta la funzione per il menu "About" di macOS (IMMEDIATAMENTE dopo il menu Apple)
                self.root.createcommand('tk::mac::ShowAbout', self._open_about)    
                self.root.createcommand('tk::mac::ShowPreferences', self._open_preferences)
                print("menu prefe")

        # --- File Menu (for other platforms or additional options) ---
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)


        if platform.system()== "Windows":
            file_menu.add_command(label="Preferences...", command=self._open_preferences)

        file_menu.add_command(label="Lingue...", command=self.open_lingue_app)
        file_menu.add_command(label="Exit", command=self.root.quit)

        file_help = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=file_help)
        # Rimuovi la voce "About" dal menu "Help" per macOS
        if sys.platform == "darwin":
            file_help.add_command(label="About", command=self._open_about)
        file_help.add_command(label="About", command=self._open_about)


    def open_lingue_app(self):
        LingueApp(self.root)

    def get_voci_nome_mac(self):
         
        if sys.platform == "darwin":  # Mac OS X
            result = subprocess.run(["say", "-v", "?"], capture_output=True, text=True)
            lines = result.stdout.strip().split("\n")
            voci = [line.split()[0] for line in lines if line.strip()]
            return voci
    
    def get_voci_inglesi_mac(self):
         
        if sys.platform == "darwin": # Mac OS X
            result = subprocess.run(["say", "-v", "?"], capture_output=True, text=True)
            lines = result.stdout.strip().split("\n")
            voci = []
            voci.append("Siri")
            voci.append("Siri voice 1")
            voci.append("Siri voice 4")
            for line in lines:
                # Evita righe vuote o righe strane
                if not line.strip():
                    continue
                # La parte della voce è fino alla prima colonna (max 20 caratteri)
                voce = line[:20].strip()
                resto = line[20:].strip()
                if not resto:
                    continue
                # La lingua è la prima parte del resto
                lingua = resto.split()[0]
                if lingua in ("en_US", "en_GB"):
                    voci.append(voce)
            return voci
        
    def _get_balcon_voices_windows(self):
        """
        Ottiene la lista delle voci SAPI 5 disponibili per Balcon su Windows
        analizzando l'output di 'balcon.exe -l'.

        Returns:
            Una lista di stringhe contenenti i nomi delle voci SAPI 5 trovate da Balcon,
            o una lista vuota in caso di errore o se non su Windows.
        """
  
        if sys.platform == "win32": 
            if os.path.exists('balcon.exe'):
                try:
                    result = subprocess.run(['balcon.exe', '-l'], capture_output=True, text=True, check=True)
                    output_lines = result.stdout.strip().split('\n')
                    voices = []
                    in_sapi5_section = False
                    for line in output_lines:
                        line = line.strip()
                        if line == "SAPI 5:":
                            in_sapi5_section = True
                            continue
                        if in_sapi5_section and line:  # Se siamo nella sezione SAPI 5 e la linea non è vuota
                            voices.append(line.lstrip())  # Rimuovi eventuali spazi iniziali
                    return voices
                except FileNotFoundError:
                    tk.messagebox.showerror("Errore", "balcon.exe non trovato. Assicurati che sia nel PATH o nella stessa directory.")
                    return []
                except subprocess.CalledProcessError as e:
                    tk.messagebox.showerror("Errore", f"Errore durante l'esecuzione di balcon.exe -l: {e}")
                    return []
        else:
            return []


    def _ricerca_web_testo_input(self, prefix=""):
        try:
            selection = self.text_input.selection_get()
            if selection:
                url = f"https://www.google.com/search?q={prefix}{selection}"
                webbrowser.open_new_tab(url)
        except tk.TclError:
            # Nessun testo selezionato
            pass

    def _ricerca_web_context_input(self, event=None):
        try:
            selection = self.text_input.selection_get()
            if selection:
                url = f"https://context.reverso.net/traduzione/inglese-italiano/{selection}"
                webbrowser.open_new_tab(url)
        except tk.TclError:
            # Nessun testo selezionato
            pass

    def _crea_menu_contestuale(self, widget):
        menu = tk.Menu(widget, tearoff=0)
        menu.add_command(label="Copia", command=lambda: widget.event_generate("<<Copy>>"))
        menu.add_command(label="Taglia", command=lambda: widget.event_generate("<<Cut>>"))        
        menu.add_command(label="Incolla", command=lambda: widget.event_generate("<<Paste>>"))
        menu.add_separator()
        menu.add_command(label="Ricerca sul Web", command=self._ricerca_web_testo_input)
        menu.add_command(label="Ricerca significato sul Web", command=lambda: self._ricerca_web_testo_input(prefix="significato: "))
        menu.add_command(label="Ricerca significato in context", command=self._ricerca_web_context_input)
        
        menu.add_separator()
        menu.add_command(label="Seleziona tutto", command=lambda: widget.select_range(0, tk.END) if isinstance(widget, tk.Entry) else widget.tag_add(tk.SEL, "1.0", tk.END))
        return menu

    def _mostra_menu(self, event, menu):
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()   

    def _sostituisci_text_con_low(self):
        current_text = self.text_input.get("1.0", tk.END)
        new_text = current_text.lower()
        self.text_input.delete("1.0", tk.END)
        self.text_input.insert("1.0", new_text)

    def _sostituisci_text_con_up(self):
        current_text = self.text_input.get("1.0", tk.END)
        new_text = current_text.upper()
        self.text_input.delete("1.0", tk.END)
        self.text_input.insert("1.0", new_text)

    def _sostituisci_uno_con_i(self):
        current_text = self.text_input.get("1.0", tk.END)
        new_text = current_text.replace("1", "i")
        new_text = new_text.replace("|", "i")
        new_text = new_text.replace("|", "i")
        new_text = new_text.replace("~", " ")

       
        self.text_input.delete("1.0", tk.END)
        self.text_input.insert("1.0", new_text)
 


    def _correggi_parole_da_csv(self):
        """
        Cerca e sostituisce parole nel text_input in base al file parole.csv nella cartella del programma.
        """
        # Ottieni la directory dove si trova il file .py attualmente in esecuzione
         

        print(f"DEBUG: sys.platform: '{sys.platform}'")
        if sys.platform == "darwin":  # Mac OS X
            macos_dir = get_macos_dir()
            print("Cartella MacOS:", macos_dir)
            base_dir = macos_dir
            if base_dir.endswith('MacOS'):
                base_dir = base_dir[:-len('MacOS')] + 'Resources'
            percorso_file = os.path.join(base_dir, "parole.csv")
            print(base_dir)
        elif sys.platform == "win32":
            base_dir = os.path.dirname(os.path.abspath(__file__))
            percorso_file = os.path.join(base_dir, "parole.csv")  # Percorso completo al file
        print(f"DEBUG: base_dir: '{base_dir}'")
        print(f"DEBUG: percorso_file: '{percorso_file}'")


        try:
            with open(percorso_file, 'r', newline='', encoding='latin-1') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                sostituzioni = {}
                for row in reader:
                    if len(row) == 2:
                        parola_errata = row[0].strip()
                        parola_corretta = row[1].strip()
                        sostituzioni[parola_errata] = parola_corretta

            current_text = self.text_input.get("1.0", tk.END)
            new_text = current_text

            for errata, corretta in sostituzioni.items():
                pattern = r'\b' + re.escape(errata) + r'\b'
                new_text = re.sub(pattern, corretta, new_text)

            self.text_input.delete("1.0", tk.END)
            self.text_input.insert("1.0", new_text)

        except FileNotFoundError:
            tk.messagebox.showerror("Errore", f"Il file parole.csv non è stato trovato.\nPercorso cercato:\n{percorso_file}")
        except Exception as e:
            tk.messagebox.showerror("Errore", f"Errore durante la lettura del file CSV:\n{e}\nPercorso cercato:\n{percorso_file}")



    def load_current_profile(self):
        print("sono qui *********************")
         
        print(f"DEBUG: sys.platform: '{sys.platform}'")
        if sys.platform == "darwin":  # Mac OS X
            macos_dir = get_macos_dir()
            print("Cartella MacOS:", macos_dir)
            base_dir = macos_dir
            if base_dir.endswith('MacOS'):
                base_dir = base_dir[:-len('MacOS')] + 'Resources'
            percorso_file = os.path.join(base_dir, self.FILE_NAME)
            print(base_dir)
        elif sys.platform == "win32":
            base_dir = os.path.dirname(os.path.abspath(__file__))
            percorso_file = os.path.join(base_dir, self.FILE_NAME)  # Percorso completo al file
        print(f"DEBUG: base_dir: '{base_dir}'")
        print(f"DEBUG: percorso_file: '{percorso_file}'")
        if os.path.exists(percorso_file):
            try:
                with open(percorso_file, 'r') as f:
                    data = json.load(f)
                    # Carica i dati nel rispettivo StringVar
                    self.user_name_key.set(data.get("user_name_key", ""))
                    self.key_value.set(data.get("key_value", ""))
                    self.tesseract_path.set(data.get("tesseract_path", ""))
                    self.openid_key.set(data.get("openid_key", ""))                 
                    self.font_size.set(data.get("font_size", 12))  # Imposta un valore predefinito
                    self.output_folder.set(data.get("output_folder", ""))

                    # Restituisce i valori correnti delle variabili
                    field_usernname_value = self.user_name_key.get()
                    field_key_value = self.key_value.get()
                    tesseract_path_value = self.tesseract_path.get()
                    openid_key_value = self.openid_key.get()
                    fonti_size_value = self.font_size.get()
                    output_folder_value = self.output_folder.get()

                    print("Valori del profilo attuale:")
                    print(f"  User Name Key: {field_usernname_value}")
                    print(f"  Key Value: {field_key_value}")
                    print(f"  Tesseract Path: {tesseract_path_value}")
                    print(f"  OpenID Key: {openid_key_value}")
                    print(f"  FontoSizeey: {fonti_size_value}")
                    print(f"  output_folder_value: {output_folder_value}")

                    return field_usernname_value, field_key_value, tesseract_path_value, openid_key_value, fonti_size_value
            except Exception as e:
                messagebox.showerror("Errore", f"Errore nel caricamento dati: {e}")
                return None, None, None, None
        else:
            print(f"Errore: Il file {percorso_file} non esiste.")
            return None, None, None, None


    def _create_widgets(self):
 
        # Frame per i pulsanti
        button_frame_check = tk.Frame(self.root)
        #button_frame_check.pack(padx=0, pady=0, anchor='n', fill='x')  # controlli allineati a sinistra
        button_frame_check.pack(pady=0)  # controlli allineati a centro 


        # Pulsante Cattura Schermo
        button_cattura = tk.Button(button_frame_check, text="Cattura", command=self._cattura_schermo_button_handler) # Usa un handler per il pulsante
        #button_cattura = tk.Button(button_frame_check, text="Cattura")
        #button_cattura.bind("<ButtonRelease-1>", lambda event: self._cattura_schermo_button_handler())
        button_cattura.pack(side=tk.LEFT, padx=2, pady=2, anchor='n', fill='x')

               # Pulsante Esegui Talk
        button_talk = tk.Button(button_frame_check, text="Talk", command=self._talk)
        button_talk.pack(side=tk.LEFT, padx=2, pady=2)

        # legge il radio per sapere se è minuscolo lowcase o maiuscolo upcase o nessuno
        self.case_option = tk.StringVar(value="lower")

        self.radio_lowcase = tk.Radiobutton(
            button_frame_check,
            text="lowcase",
            variable=self.case_option,
            value="lower"
        )
        self.radio_lowcase.pack(side=tk.LEFT, padx=0)

        self.radio_upcase = tk.Radiobutton(
            button_frame_check,
            text="upcase",
            variable=self.case_option,
            value="upper"
        )
        self.radio_upcase.pack(side=tk.LEFT, padx=0)

        # Terzo radio: NONE
        self.radio_none = tk.Radiobutton(
            button_frame_check,
            text="none",
            variable=self.case_option,
            value="none"
        )
        self.radio_none.pack(side=tk.LEFT, padx=0)

        # 👉 ✅ Checkbox RimuovoLR
        self.play_lento_var = tk.BooleanVar(value=True)  # True di default
        self.checkbox_play_lento = tk.Checkbutton(button_frame_check, text="Play Lento", variable=self.play_lento_var)
        self.checkbox_play_lento.pack(side=tk.LEFT, padx=0)


        # Frame per i pulsanti
        button_frame_bar = tk.Frame(self.root)
        button_frame_bar.pack(pady=0)  # Margine sotto i componenti

        # Creazione della label
        label_lingua = tk.Label(button_frame_bar, text="Lingua OCR:", cursor="hand2")
        label_lingua.pack(side=tk.LEFT, padx=0)
        # Associazione della funzione all'evento di click, passando il parametro "E"
        label_lingua.bind("<Button-1>", lambda event: self.mia_funzione_click(event, "E"))

        label_lingua_c = tk.Label(button_frame_bar, text="C", cursor="hand1")
        label_lingua_c.pack(side=tk.LEFT, padx=0)
        label_lingua_c.bind("<Button-1>", lambda event: self.mia_funzione_click(event, "C"))

        label_lingua_j = tk.Label(button_frame_bar, text="J", cursor="hand1")
        label_lingua_j.pack(side=tk.LEFT, padx=0)
        label_lingua_j.bind("<Button-1>", lambda event: self.mia_funzione_click(event, "J"))

        label_lingua_k = tk.Label(button_frame_bar, text="K", cursor="hand1")
        label_lingua_k.pack(side=tk.LEFT, padx=0)
        label_lingua_k.bind("<Button-1>", lambda event: self.mia_funzione_click(event, "K"))

        self.combo_lingua = ttk.Combobox(button_frame_bar, values=["English", "Italian", "Japanese", "Japanese Vert", "French", "Spanish", "Korean", "Korean Vert", "chinesesimplified" , "chinesesimplified Vert" , "chinesetraditional",  "chinesetraditional Vert"], state="readonly", width=15)
        self.combo_lingua.set("English")  # Lingua predefinita
        self.combo_lingua.pack(side=tk.LEFT, padx=0)
        

        # 👉 ✅ Checkbox RimuovoLR
        self.rimuovo_lr_var = tk.BooleanVar(value=True)  # True di default
        self.checkbox_rimuovo_lr = tk.Checkbutton(button_frame_bar, text="Rim LR", variable=self.rimuovo_lr_var)
        self.checkbox_rimuovo_lr.pack(side=tk.LEFT, padx=0)

        self.forza_rgb_var = tk.BooleanVar(value=True)  # True di default
        self.checkbox_forza_rgb = tk.Checkbutton(button_frame_bar, text="Forza RGB", variable=self.forza_rgb_var)
        self.checkbox_forza_rgb.pack(side=tk.LEFT, padx=0)

        # Frame per i pulsanti
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=0)  # Margine sotto i componenti


        self.cattura_in_ocr_var = tk.BooleanVar(value=True)  # True di default
        self.button_frame = tk.Checkbutton(button_frame, text="Catt. OCR", variable=self.cattura_in_ocr_var)
        self.button_frame.pack(side=tk.LEFT, padx=0)

        # Pulsante Esegui OCR
        #button_ocr = tk.Button(button_frame, text="Web", command=self._esegui_ocr)
        #button_ocr.pack(side=tk.LEFT, padx=0)

        # Pulsante Esegui OCR
        button_ocrGoogle = tk.Button(button_frame, text="Tess", command=self._esegui_ocr_google_handler)
        button_ocrGoogle.pack(side=tk.LEFT,padx=2, pady=2)

        # Pulsante Esegui OCR 
        button_ocrEasy = tk.Button(button_frame, text="Easy", command=self._esegui_ocr_easy)
        button_ocrEasy.pack(side=tk.LEFT, padx=2, pady=2)

        # Pulsante Esegui OCR
        button_ocrSpace = tk.Button(button_frame, text="Space", command=self._esegui_ocr_space)
        button_ocrSpace.pack(side=tk.LEFT, padx=2, pady=2)

        self.combo_ocrSpace = ttk.Combobox(button_frame, values=["1", "2", "3"], state="readonly", width=2)
        self.combo_ocrSpace.set("1")  # Lingua predefinita
        self.combo_ocrSpace.pack(side=tk.LEFT, padx=2, pady=2)

        # NUOVO PULSANTE "1 -> i"
        button_sostituisci_uno = tk.Button(button_frame, text="1->i", command=self._sostituisci_uno_con_i)
        button_sostituisci_uno.pack(side=tk.LEFT, padx=5)

        self.load_current_profile()


        # Frame per il widget text_input
        frame_input = tk.Frame(self.root)
        frame_input.pack(padx=0, pady=0, fill=tk.BOTH, expand=True)
       
        font_size_14 = font.Font(size=self.font_size.get())
        
        scroll_input = tk.Scrollbar(frame_input)
        scroll_input.pack(side=tk.RIGHT, fill=tk.Y)



        self.text_input = tk.Text(frame_input, height=1, width=50, wrap=tk.WORD, yscrollcommand=scroll_input.set, font=font_size_14, bd=0,          # Larghezza del bordo (es. 2 pixel)
            relief=tk.RIDGE # Stile del bordo (es. RIDGE, SUNKEN, RAISED, GROOVE, FLAT)
        )
        
        self.text_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        scroll_input.config(command=self.text_input.yview)

 

        # Menu contestuale per text_input
        menu_contestuale_input = self._crea_menu_contestuale(self.text_input)
        self.text_input.bind("<Button-2>", lambda event, menu=menu_contestuale_input: self._mostra_menu(event, menu))  # Corretto il binding al tasto destro

        # Frame per i pulsanti
        button_frame_text = tk.Frame(self.root)

        button_frame_text.pack(padx=0, pady=0, anchor='n')

        button_sostituisci_low= tk.Button(button_frame_text, text="low", command=self._sostituisci_text_con_low)
        button_sostituisci_low.pack(side=tk.LEFT, padx=2, pady=2)

        button_sostituisci_UP= tk.Button(button_frame_text, text="UP", command=self._sostituisci_text_con_up)
        button_sostituisci_UP.pack(side=tk.LEFT, padx=2, pady=2)

        #_correggi_parole_da_csv
        button_sostituisci_csv= tk.Button(button_frame_text, text="csv", command=self._correggi_parole_da_csv)
        button_sostituisci_csv.pack(side=tk.LEFT, padx=2, pady=2)
          
        self.rimuovo_audio_var = tk.BooleanVar(value=True)  # True di default
        self.checkbox_rimuovo_audio = tk.Checkbutton(button_frame_text, text="Rim Audio", variable=self.rimuovo_audio_var)
        self.checkbox_rimuovo_audio.pack(side=tk.LEFT, padx=2, pady=2)


         # ✅ Combobox con le lingue (voci) disponibili su Mac
        #voci = self.get_voci_nome_mac()
   
        if sys.platform == "darwin":  # Mac OS X
            voci_inglesi = self.get_voci_inglesi_mac()
            self.voice_var = tk.StringVar()
            self.voice_combobox = ttk.Combobox(button_frame_text, textvariable=self.voice_var, values=voci_inglesi, state="readonly", width=15)
            voce_predefinita = next((voce for voce in voci_inglesi if "Samantha" in voce), voci_inglesi[0] if voci_inglesi else "")
            self.voice_combobox.set(voce_predefinita)

            #self.voice_combobox.set("Kate" if "Kate" in voci_inglesi else voci_inglesi[0])  # Default: Kate se esiste
            self.voice_combobox.pack(side=tk.LEFT, padx=0)
        # def _get_balcon_voices_windows(self):
        else: 
            balcon_voices = self._get_balcon_voices_windows()
            if balcon_voices:
                self.voice_var = tk.StringVar()
                voice_combobox = ttk.Combobox(button_frame_text, textvariable=self.voice_var, values=balcon_voices, state="readonly", width=15)
                # Imposta una voce predefinita (potresti volerla rendere configurabile)
                default_voice = next((v for v in balcon_voices if "Microsoft David" in v), balcon_voices[0] if balcon_voices else "")
                voice_combobox.set(default_voice)
                voice_combobox.pack(side=tk.LEFT, padx=0)
                self.voice_combobox = voice_combobox  # Salva il riferimento
            else:
                # Se non ci sono voci o si è verificato un errore, potresti mostrare un messaggio
                tk.Label(button_frame_play, text="Voci Balcon non trovate").pack(side=tk.LEFT, padx=0)
                self.voice_combobox = None



        # Frame per i pulsanti
        button_frame_play = tk.Frame(self.root)

        button_frame_play.pack(padx=0, pady=0, anchor='n')

        # Pulsante per riprodurre il suono del testo originale
        #button_audio_org = tk.Button(button_frame_play, text="Play Google", command=lambda: self._riproduci_audio_originale(self.text_input.get(1.0, tk.END).strip()))
        #button_audio_org.pack(side=tk.LEFT, padx=0)

        # Carica l'immagine (assicurati che il percorso sia corretto)
        #percorso_immagine = os.path.join(os.getcwd(), "play4.png")

        if sys.platform == "darwin":
            
            macos_dir = get_macos_dir()
            print("Cartella MacOS:", macos_dir)
            base_dir = macos_dir
            if base_dir.endswith('MacOS'):
                base_dir = base_dir[:-len('MacOS')] + 'Resources'
            percorso_immagine = os.path.join(base_dir,  "play4.png")
            print(base_dir)
        elif sys.platform == "win32":
            base_dir = os.path.dirname(os.path.abspath(__file__))
            percorso_immagine = os.path.join(base_dir, "play4.png")  # Percorso completo al file


        if os.path.exists(percorso_immagine):
            print("trovato "+percorso_immagine)
        try:
            self.play_icon = PhotoImage(file=percorso_immagine)
            #self.play_icon = PhotoImage(file="play1.jpg")  # Sostituisci con il percorso della tua immagine
            # Ridimensiona l'immagine se necessario
            self.play_icon = self.play_icon.subsample(4, 4) # Regola i fattori di sottocampionamento

            # Crea il pulsante con l'immagine
            self.button_audio_org = tk.Button(button_frame_play, image=self.play_icon, command=lambda: self._riproduci_audio_originale(self.text_input.get(1.0, tk.END).strip()))
            self.button_audio_org.pack(side=tk.LEFT, padx=2, pady=2)
        except tk.TclError:
            print("Errore: Impossibile caricare l'immagine. Assicurati che il percorso sia corretto.")
            # In caso di errore nel caricamento dell'immagine, mostra comunque un pulsante di testo
            self.button_audio_org = tk.Button(button_frame_play, text="Play", command=lambda: self._riproduci_audio_originale(self.text_input.get(1.0, tk.END).strip()))
            self.button_audio_org.pack(side=tk.LEFT, padx=2, pady=2)

        self.button_audio_orgLento = tk.Button(button_frame_play, text="PlayL", command=lambda: self._riproduci_audio_originaleLento(self.text_input.get(1.0, tk.END).strip()))
        self.button_audio_orgLento.pack(side=tk.LEFT, padx=2, pady=2)

        # Pulsante per riprodurre il suono del testo originale
        button_audio_org_mac = tk.Button(button_frame_play, text="Play Mac", command=lambda: self._riproduci_audio_originale_mac(self.text_input.get(1.0, tk.END).strip(), 0))
        button_audio_org_mac.pack(side=tk.LEFT, padx=2, pady=2)

        # Pulsante per riprodurre il suono del testo originale
        button_audio_org_mac_siri = tk.Button(button_frame_play, text="Play Siri", command=lambda: self._riproduci_audio_originale_mac_siri(self.text_input.get(1.0, tk.END).strip(), 140))
        button_audio_org_mac_siri.pack(side=tk.LEFT, padx=2, pady=2)


        button_audio_org_mac_lento = tk.Button(button_frame_play, text="Play Mac", command=lambda: self._riproduci_audio_originale_mac(self.text_input.get(1.0, tk.END).strip(), 51))
        button_audio_org_mac_lento.pack(side=tk.LEFT, padx=2, pady=2)



        # Frame per i pulsanti
        frame_lingua_dest = tk.Frame(self.root)

        frame_lingua_dest.pack(padx=0, pady=0, anchor='n')



        # Dropdown per la selezione della lingua di destinazione
        label_lingua_dest = tk.Label(frame_lingua_dest, text="Lingua d:")
        label_lingua_dest.pack(side=tk.LEFT, padx=0)

        self.combo_lingua_dest = ttk.Combobox(frame_lingua_dest, values=["English", "Italian", "Japanese", "French", "Spanish", "Korean"], state="readonly", width=7)
        self.combo_lingua_dest.set("Italian")  # Lingua predefinita (Italiano)
        self.combo_lingua_dest.pack(side=tk.LEFT, padx=0)

        # Pulsante Traduci
        button_traduci = tk.Button(frame_lingua_dest, text="Google", command=self._traduci_testo_btn)
        button_traduci.pack(side=tk.LEFT, padx=0, pady=1)

        button_traduci_lara = tk.Button(frame_lingua_dest, text="Lara", command=self._traduci_testo_lara_btn)
        button_traduci_lara.pack(side=tk.LEFT, padx=0, pady=1)

        button_traduci_ipa = tk.Button(frame_lingua_dest, text="IPA", command=self._traduci_testo_ipa_btn)
        button_traduci_ipa.pack(side=tk.LEFT, padx=0, pady=1)

        button_traduci_deep = tk.Button(frame_lingua_dest, text="Deep", command=self._traduci_testo_deep_btn)
        button_traduci_deep.pack(side=tk.LEFT, padx=0, pady=1)

        button_traduci_argos = tk.Button(frame_lingua_dest, text="Argos", command=self._traduci_testo_argos_btn)
        button_traduci_argos.pack(side=tk.LEFT, padx=0, pady=1)


        # Frame per il widget text_tradotto
        frame_tradotto = tk.Frame(self.root)
        frame_tradotto.pack(padx=0, pady=0, fill=tk.BOTH, expand=True)

        scroll_tradotto = tk.Scrollbar(frame_tradotto)
        scroll_tradotto.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_tradotto = tk.Text(frame_tradotto, height=1, width=50, wrap=tk.WORD, yscrollcommand=scroll_tradotto.set, font=font_size_14, bd=2,          # Larghezza del bordo (es. 2 pixel)
            relief=tk.RIDGE # Stile del bordo (es. RIDGE, SUNKEN, RAISED, GROOVE, FLAT)
        )
        
        self.text_tradotto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        scroll_tradotto.config(command=self.text_tradotto.yview)

        # Menu contestuale per text_tradotto
        menu_contestuale_tradotto = self._crea_menu_contestuale(self.text_tradotto)
        self.text_tradotto.bind("<Button-2>", lambda event, menu=menu_contestuale_tradotto: self._mostra_menu(event, menu))

        #--------

      


        # Frame per il widget text_tradotto
        frame_tradotto_lara = tk.Frame(self.root)
        frame_tradotto_lara.pack(padx=0, pady=0, fill=tk.BOTH, expand=True)

        scroll_tradotto_lara = tk.Scrollbar(frame_tradotto_lara)
        scroll_tradotto_lara.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_tradotto_lara = tk.Text(frame_tradotto_lara, height=1, width=50, wrap=tk.WORD, yscrollcommand=scroll_tradotto_lara.set, font=font_size_14, bd=2,          # Larghezza del bordo (es. 2 pixel)
            relief=tk.RIDGE # Stile del bordo (es. RIDGE, SUNKEN, RAISED, GROOVE, FLAT)
        )
        
        self.text_tradotto_lara.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        scroll_tradotto_lara.config(command=self.text_tradotto_lara.yview)

        # Menu contestuale per text_tradotto
        menu_contestuale_tradotto_lara = self._crea_menu_contestuale(self.text_tradotto_lara)
        self.text_tradotto_lara.bind("<Button-2>", lambda event, menu=menu_contestuale_tradotto_lara: self._mostra_menu(event, menu))



        # Pulsante per riprodurre il suono del testo tradotto
        button_audio_trad = tk.Button(self.root, text="Play Audio tradotto", command=lambda: self._riproduci_audio_tradotto(self.text_tradotto.get(1.0, tk.END).strip()))
        button_audio_trad.pack()

    def _open_preferences(self):
        import tkinter as tk
        from tkinter import messagebox
        import os, json, webbrowser
        from tkinter import ttk

        pref_window = tk.Toplevel(self.root)
        pref_window.title("Preferenze")
        pref_window.geometry("400x400")
        pref_window.resizable(False, False)

        # Memorizza la finestra come attributo dell'oggetto
        self.pref_window = pref_window

        # Link per registrazione
        link_label = tk.Label(pref_window, text="OCR WEB SERVICE (registrati)", fg="blue", cursor="hand2")
        link_label.pack(pady=(10, 5))
        link_label.bind("<Button-1>", lambda e: webbrowser.open("http://www.ocrwebservice.com"))

        # Caricamento dati
        def load_data():
           

            print(f"DEBUG: sys.platform: '{sys.platform}'")
            if sys.platform == "darwin":  # Mac OS X
                macos_dir = get_macos_dir()
                print("Cartella MacOS:", macos_dir)
                base_dir = macos_dir
                if base_dir.endswith('MacOS'):
                    base_dir = base_dir[:-len('MacOS')] + 'Resources'
                percorso_file = os.path.join(base_dir, self.FILE_NAME)
                print(base_dir)
            elif sys.platform == "win32":
                base_dir = os.path.dirname(os.path.abspath(__file__))
                percorso_file = os.path.join(base_dir, self.FILE_NAME)  # Percorso completo al file
            print(f"DEBUG: base_dir: '{base_dir}'")
            print(f"DEBUG: percorso_file: '{percorso_file}'")

            if os.path.exists(percorso_file):
                try:
                    with open(percorso_file, 'r') as f:
                        data = json.load(f)
                        self.user_name_key.set(data.get("user_name_key", ""))
                        self.key_value.set(data.get("key_value", ""))
                        self.tesseract_path.set(data.get("tesseract_path", ""))
                        self.openid_key.set(data.get("openid_key", ""))
                        self.font_size.set(data.get("font_size", 12))
                        self.output_folder.set(data.get("output_folder", ""))
                except Exception as e:
                    messagebox.showerror("Errore", f"Errore nel caricamento dati: {e}")

        load_data()

        frame = tk.Frame(pref_window)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Label(frame, text="User Name:").grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(frame, textvariable=self.user_name_key, width=40).grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Key Value:").grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(frame, textvariable=self.key_value, width=40).grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Tesseract Path:").grid(row=2, column=0, sticky="w", pady=5)
        tk.Entry(frame, textvariable=self.tesseract_path, width=40).grid(row=2, column=1, pady=5)

        tk.Label(frame, text="OpenID Key:").grid(row=3, column=0, sticky="w", pady=5)
        tk.Entry(frame, textvariable=self.openid_key, width=40).grid(row=3, column=1, pady=5)

        # Nuova sezione per la dimensione del font
        tk.Label(frame, text="Dimensione Font:").grid(row=4, column=0, sticky="w", pady=5)
        font_sizes = [8, 10, 12, 14, 16, 18, 20]
        font_size_combo = ttk.Combobox(frame, textvariable=self.font_size, values=font_sizes, width=5)
        font_size_combo.grid(row=4, column=1, sticky="w", pady=5)
        font_size_combo.set(self.font_size.get())

        # --- Nuova sezione: Cartella di output ---
        tk.Label(frame, text="Cartella Output:").grid(row=5, column=0, sticky="w", pady=5)
        output_entry = tk.Entry(frame, textvariable=self.output_folder, width=30)
        output_entry.grid(row=5, column=1, sticky="w", pady=5)

        def browse_folder():
            selected_folder = filedialog.askdirectory()
            if selected_folder:
                self.output_folder.set(selected_folder)

        browse_button = tk.Button(frame, text="Sfoglia", command=browse_folder)
        browse_button.grid(row=5, column=1, sticky="e", padx=(0, 5))


        btn_frame = tk.Frame(pref_window)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Salva", command=self._save_data).pack(side="left", padx=10) # Usa self._save_data
        tk.Button(btn_frame, text="Chiudi", command=pref_window.destroy).pack(side="left", padx=10)

   

    def _save_data(self): # Definisci _save_data come metodo della classe
        data_to_save = {
            "user_name_key": self.user_name_key.get(),
            "key_value": self.key_value.get(),
            "tesseract_path": self.tesseract_path.get(),
            "openid_key": self.openid_key.get(),
            "font_size": self.font_size.get(),
            "output_folder": self.output_folder.get()
        }

        try:
             
            print(f"DEBUG: sys.platform: '{sys.platform}'")
            if sys.platform == "darwin":  # Mac OS X
                macos_dir = get_macos_dir()
                print("Cartella MacOS:", macos_dir)
                base_dir = macos_dir
                if base_dir.endswith('MacOS'):
                    base_dir = base_dir[:-len('MacOS')] + 'Resources'
                percorso_file = os.path.join(base_dir, self.FILE_NAME)
                print(base_dir)
            elif sys.platform == "win32":
                base_dir = os.path.dirname(os.path.abspath(__file__))
                percorso_file = os.path.join(base_dir, self.FILE_NAME)  # Percorso completo al file
            print(f"DEBUG: base_dir: '{base_dir}'")
            print(f"DEBUG: percorso_file: '{percorso_file}'")
            
            with open(percorso_file, 'w') as f:
                json.dump(data_to_save, f, indent=4)
            messagebox.showinfo("Salva", "Dati salvati con successo!")
            self.apply_font_to_text_widgets() # Chiama la funzione per aggiornare il font         
            self.pref_window.destroy() # Chiama il metodo destroy() sull'attributo self.pref_window
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile salvare i dati: {e}")


    def apply_font_to_text_widgets(self):
        try:
            print("applica font")
            font_size_value = int(self.font_size.get())
            custom_font = font.Font(size=font_size_value)
            self.text_input.config(font=custom_font, height=8)
            self.text_tradotto.config(font=custom_font, height=8) # Applica anche all'altro widget di testo
        except ValueError:
            messagebox.showerror("Errore", "Dimensione del font non valida.")
            # Potresti voler impostare un font predefinito in caso di errore
            default_font = font.Font(size=12)
            self.text_input.config(font=default_font, height=8)
            self.text_tradotto.config(font=default_font, height=8)

     


     



    def mia_funzione_click(self, event, parametro):
        """Questa funzione verrà eseguita quando la label viene cliccata."""
        print("La label è stata cliccata!")
        print(f"La label è stata cliccata! Parametro ricevuto: {parametro}")
        # Qui puoi aggiungere il codice che vuoi eseguire al click
        # Ad esempio, potresti voler impostare la lingua del combobox:
        if parametro in ["E", "C", "J", "K"]:
            lingue = {"E": "English", "C": "chinesesimplified", "J": "Japanese", "K": "Korean"}
            if parametro in lingue:
                self.combo_lingua.set(lingue[parametro])




            

   
    def _esegui_ocr(self):
 

        language = self.combo_lingua.get()
        print(language)
        language = language.upper()
        print(language)
        client = Client('http://www.ocrwebservice.com/services/OCRWebService.asmx?WSDL')

  
        

        if sys.platform == "darwin":  # Mac OS X
            user_home = os.path.expanduser("~")
            FilePath = os.path.join(user_home, "temp.jpg")
        elif sys.platform == "win32":
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            FilePath = os.path.join(desktop_path, "test_image.jpg")

        if not os.path.exists(FilePath):
            self.text_input.delete(1.0, tk.END)
            self.text_input.insert(tk.END, f"File immagine non trovato: {FilePath}")
            return

        print(FilePath)
        with open(FilePath, 'rb') as image_file:
            image_data = image_file.read()

        InputImage = {
            'fileName': 'test_image.jpg',
            'fileData': image_data,
        }

        OCRSettings = {
            'ocrLanguages': language,
            'outputDocumentFormat': 'TXT',
            'convertToBW': 'true',
            'getOCRText': 'true',
            'createOutputDocument': 'true',
            'multiPageDoc': 'true',
            'pageNumbers': 'allpages',
            'ocrWords': 'false',
        }
        #user_name='escozzaro71', license_code='790BECEC-BF66-475B-8604-C56492B22695',
   
        print(self.user_name_key.get())
        print(self.key_value.get())
        print("enzo 790BECEC-BF66-475B-8604-C56492B22695")
        result = client.service.OCRWebServiceRecognize(
            user_name=self.user_name_key.get(), license_code=self.key_value.get(),
            OCRWSInputImage=InputImage, OCRWSSetting=OCRSettings
        )

        if result.errorMessage:
            self.text_input.delete(1.0, tk.END)
            self.text_input.insert(tk.END, "Errore: " + result.errorMessage)
            return

        extracted_text = result.ocrText.ArrayOfString[0].string[0].lower()
        self.text_input.delete(1.0, tk.END)
        self.text_input.insert(tk.END, extracted_text)

      
    def _ocr_space_file(self, filename, language='eng'):
        
        api_key = self.openid_key.get()
        # 'K82475447288957'
        overlay = False

        print(f"Filename: {filename}")
        print(f"API Key: {api_key}")
        print(f"Language: {language}")

        ServerOcrSpace = self.combo_ocrSpace.get()
        print("Server OCR Space: "+ServerOcrSpace)
        payload = {
            'isOverlayRequired': str(overlay).lower(),
            'apikey': api_key,
            'language': language,
            'OCREngine': ServerOcrSpace,
        }

        print("Payload inviato:")
        print(payload)

        with open(filename, 'rb') as f:
            r = requests.post(
                'https://api.ocr.space/parse/image',
                files={'file': f},
                data=payload,
                timeout=15
            )

        response_text = r.content.decode()
        print("Risposta server:")
        print(response_text.encode('utf-8', errors='replace').decode('utf-8'))

        # Estrarre il testo parsato
        try:
            parsed_text = r.json()['ParsedResults'][0]['ParsedText']
            if self.rimuovo_lr_var.get():
                print("RimuovoLR è attivo ok")
                parsed_text = parsed_text.strip('\n').strip('\r')
                parsed_text = ' '.join(parsed_text.splitlines())
            else:
                print("La checkbox RimuovoLR NON è selezionata (False)")
                parsed_text = parsed_text
            print("Testo OCR trovato:")
            print(parsed_text)
            if self.case_option.get()=='lower': 
                parsed_text = parsed_text.lower()
            elif self.case_option.get()=='upper': 
                parsed_text = parsed_text.upper()

        except Exception as e:
            print(f"Errore durante l'estrazione del testo OCR: {e}")

        return parsed_text




    def _esegui_ocr_space(self):
        # Mappa delle lingue: https://ocr.space/OCRAPI#GettingStarted
        language_mapping = {
            "english": "eng",
            "italian": "ita",
            "japanese": "jpn",
            "french": "fre",
            "spanish": "spa",
            "korean": "kor",
            "chinesesimplified" : "chs",
            "chinesetraditional": "cht",
            "japanese vert": "jpn",  
            "chinesesimplified vert": "chs",
            "chinesetraditional vert": "cht" 

        }

        lang_orig = self.combo_lingua.get()  # Ottengo il valore dalla combobox
        lngO = language_mapping.get(lang_orig.lower(), "eng")  # Converte in lowercase da en se non trova la lingua in language_mapping
        lingua_orig = lngO
    
         

        if sys.platform == "darwin":  # Mac OS X
            user_home = os.path.expanduser("~")
            FilePath = os.path.join(user_home, "temp.jpg")
        elif sys.platform == "win32":
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            FilePath = os.path.join(desktop_path, "test_image.jpg")
        
        test_file = self._ocr_space_file(FilePath, lingua_orig)
        self.text_input.delete(1.0, tk.END)
        self.text_input.insert(tk.END, test_file)
        
        testo_tradotto = self._traduci_google(test_file)
        self.text_tradotto.delete(1.0, tk.END)
        self.text_tradotto.insert(tk.END, testo_tradotto)


    def _esegui_ocr_easy(self):
        # Mappa delle lingue: https://www.jaided.ai/easyocr/
        language_mapping = {
            "english": "en",
            "italian": "it",
            "japanese": "ja",
            "japanese vert": "ja",
            "french": "fr",
            "spanish": "es",
            "korean": "ko",
            "chinesesimplified": "ch_sim",
            "chinesesimplified vert": "ch_sim",
            "chinesetraditional": "ch_tra",
            "chinesetraditional vert": "ch_tra" 
        }

        lang_orig = self.combo_lingua.get()
        lngO = language_mapping.get(lang_orig.lower(), "en")
        lingua_orig = lngO

         

        if sys.platform == "darwin":
            user_home = os.path.expanduser("~")
            FilePath = os.path.join(user_home, "temp.jpg")
        elif sys.platform == "win32":
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            FilePath = os.path.join(desktop_path, "test_image.jpg")

        if not os.path.exists(FilePath):
            self.text_input.delete(1.0, tk.END)
            self.text_input.insert(tk.END, f"File immagine non trovato: {FilePath}")
            return

        print(f"OCR: sto leggendo il file -> {FilePath}")

        if FilePath:
            print("lingua easy")
            print(lingua_orig)
            sys.stdout.reconfigure(encoding='utf-8')
            reader = easyocr.Reader([lingua_orig], verbose=False)
            img = Image.open(FilePath)
            if self.forza_rgb_var.get():
                img = img.convert('RGB')  # forza RGBbrew install libomp
                print("rgb Forzato")
            else:
                print("rgb Non FORZATO")
            img_array = np.array(img)  # <-- conversione a array NumPy

            # OCR direttamente dall'array
            result = reader.readtext(img_array)

            fullText = ""

            for res in result:
                coord = res[0]
                text = res[1]
                conf = res[2]
                if self.rimuovo_lr_var.get():
                    print("RimuovoLR è attivo")
                    fullText = fullText + " " + text
                else:
                    print("La checkbox RimuovoLR NON è selezionata (False)")
                    fullText = fullText + "\n" + text
                print("1.." + text)
            if self.case_option.get()=='lower': 
                fullText = fullText.lower()
            elif self.case_option.get()=='upper': 
                fullText = fullText.upper()
            self.text_input.delete(1.0, tk.END)
            self.text_input.insert(tk.END, fullText)
            testo_tradotto = self._traduci_google(fullText)
            self.text_tradotto.delete(1.0, tk.END)
            self.text_tradotto.insert(tk.END, testo_tradotto)
            print(fullText)


     # Nuovo handler per il pulsante "Tess"
    def _esegui_ocr_google_handler(self):
        # Questo metodo viene chiamato quando l'utente clicca "Tess"
        # Se la cattura è attiva, la avviamo con una callback.
        # Altrimenti, eseguiamo l'OCR direttamente sull'ultima immagine catturata o path predefinito.
        if self.cattura_in_ocr_var.get():
            self.after_capture_callback = self._continue_ocr_google # Imposta la callback
            self._cattura_schermo() # Avvia la cattura
        else:
            if sys.platform == "darwin":
                user_home = os.path.expanduser("~")
                FilePath = os.path.join(user_home, "temp.jpg")
            elif sys.platform == "win32":
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                FilePath = os.path.join(desktop_path, "test_image.jpg")
            self.last_captured_image_path = FilePath
            self._continue_ocr_google(self.last_captured_image_path) # Passa il path esistente

    # Funzione che verrà chiamata dopo la cattura dello schermo
    def _continue_ocr_google(self, captured_file_path=None):
        # Ripristina la callback per evitare chiamate indesiderate
        self.after_capture_callback = None 

        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path.get()
        
        # Determina il percorso del file immagine
        FilePath = captured_file_path
        if FilePath is None: # Se non è stato passato dalla cattura
            if sys.platform == "darwin":  # Mac OS X
                user_home = os.path.expanduser("~")
                FilePath = os.path.join(user_home, "temp.jpg") 
            elif sys.platform == "win32":
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                FilePath = os.path.join(desktop_path, "test_image.jpg")

        self.last_captured_image_path = FilePath # Aggiorna l'ultima immagine catturata

        self.text_input.delete(1.0, tk.END) # Pulisce prima di inserire
        self.text_input.insert(tk.END, f"File immagine trovato: {FilePath}") # Messaggio informativo

        if not os.path.exists(FilePath):
            self.text_input.delete(1.0, tk.END)
            self.text_input.insert(tk.END, f"Errore: File immagine non trovato: {FilePath}")
            return
        
        # Ora che il file è stato catturato (o il path è stato determinato), procedi con l'OCR e la traduzione
        if FilePath:
            self._traduci_da_immagine_google(FilePath)


    def _esegui_ocr_google(self):
 

        pytesseract.pytesseract.tesseract_cmd = r""+self.tesseract_path.get()
         
        if self.cattura_in_ocr_var.get(): 
            self._cattura_schermo()
        if sys.platform == "darwin":  # Mac OS X
            user_home = os.path.expanduser("~")
            FilePath = os.path.join(user_home, "temp.jpg")
        elif sys.platform == "win32":
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            FilePath = os.path.join(desktop_path, "test_image.jpg")

        if not os.path.exists(FilePath):
            self.text_input.delete(1.0, tk.END)
            self.text_input.insert(tk.END, f"File immagine non trovato: {FilePath}")
            return
        
        if FilePath:
            self._traduci_da_immagine_google(FilePath)

  
    def _traduci_da_immagine_google(self, image_path):
        def fix_ocr_typo(text):
            """
            Sostituisce la lettera 't' con 'I' solo quando 't' è una parola isolata.
            """
            words = text.split(' ')
            corrected_words = [word.replace('t', 'I') if word == 't' else word for word in words]
            return ' '.join(corrected_words)
        
        language_mapping = {
            "english": "eng",
            "italian": "ita",
            "japanese": "jpn",
            "japanese vert": "jpn_vert",
            "french": "fra",
            "spanish": "spa",
            "korean": "kor",
            "korean vert": "kor_vert",
            "chinesesimplified" : "chi_sim",
            "chinesesimplified vert" : "chi_sim_vert",
            "chinesetraditional": "chi_tra",
            "chinesetraditional vert": "chi_tra_vert"
        }

        lang_orig = self.combo_lingua.get()
        lingua_orig = language_mapping.get(lang_orig.lower(), "eng")

        print("tess origine: "+lang_orig)
        print("tess sigla: "+lingua_orig)

        testo = self._ocr_da_immagine_google(image_path, lingua_orig)
        print(testo)
     
        if not testo:
            self.text_tradotto.delete(1.0, tk.END)
            self.text_tradotto.insert(tk.END, "Nessun testo riconosciuto dall'immagine.")
            return

        testo_tradotto = self._traduci_google(testo)        
        self.text_tradotto.delete(1.0, tk.END)
        self.text_tradotto.insert(tk.END, testo_tradotto)

        #Ho disabilitato la traduzione automatica per Lara visto che ha un limite di 10.000 caratteri mensili. 
        #self._traduci_testo_lara_btn()


        
        


    def _ocr_da_immagine_google(self, image_path, ocr_lng):    


        try:
            version = pytesseract.get_tesseract_version()
            print(f"Tesseract version: {version}")
        except Exception as e:
            print(f"Errore: {e}")
        try:
            img = Image.open(image_path)
            if self.forza_rgb_var.get():
                img = img.convert('RGB')  # forza RGBbrew install libomp
                print("rgb Forzato")
            else:
                print("rgb Non FORZATO")
            # testo_estratto = pytesseract.image_to_string(img, lang='kor')
            testo_estratto = pytesseract.image_to_string(img, lang=ocr_lng)
            if self.rimuovo_lr_var.get():
                print("RimuovoLR è attivo ok")
                testo_estratto = testo_estratto.strip('\n').strip('\r')
                testo_estratto = ' '.join(testo_estratto.splitlines())
            else:
                print("La checkbox RimuovoLR NON è selezionata (False)")
                testo_estratto = testo_estratto
            if self.case_option.get()=='lower': 
                testo_estratto = testo_estratto.lower()
            elif self.case_option.get()=='upper': 
                testo_estratto = testo_estratto.upper()

            testo_estratto = fix_ocr_typo(testo_estratto)
            self.text_input.delete(1.0, tk.END)
            self.text_input.insert(tk.END, testo_estratto)
            return testo_estratto.strip()
        except Exception as e:
            return f"Errore nell'OCR: {str(e)}"

 
    def _traduci_google(self, testo):
        # Mappa lingua: https://cloud.google.com/translate/docs/languages?hl=it
        language_mapping = {
            "english": "en",
            "italian": "it",
            "japanese": "ja",
            "japanese vert": "ja",
            "french": "fr",
            "spanish": "es",
            "korean": "ko",
            "korean vert": "ko",
            "chinesesimplified" : "zh-CN",
            "chinesesimplified vert" : "zh-CN",
            "chinesetraditional": "zh-TW",
            "chinesetraditional vert": "zh-TW"
        }

        lang_orig = self.combo_lingua.get()  # Ottengo il valore dalla combobox
        lngO = language_mapping.get(lang_orig.lower(), "en")  # Converte in lowercase da en se non trova la lingua in language_mapping
        lingua_orig = lngO

        print("origini "+ lingua_orig)

        lang_dest = self.combo_lingua_dest.get()
        lngD = language_mapping.get(lang_dest.lower(), "en")  # Converte in lowercase da en se non trova la lingua in language_mapping
        lingua_dest = lngD
 
        print("Destinazioni "+ lingua_dest)

        translator = GoogleTranslator()
        try:
            testo_tradotto = translator.translate(testo, dest=lingua_dest, src=lingua_orig).text
        except Exception as e:
            testo_tradotto = f"Errore nella traduzione: {str(e)}"
        return testo_tradotto      

    

    #Funzine obsoleta
    #def _cattura_ocr(self):
    #    self._cattura_schermo()
    #    self._esegui_ocr()

    def _talk(self):
        if sys.platform == "darwin":
            pyautogui.hotkey('command', 'shift', 'y')
        elif sys.platform == "win32":
            pyautogui.hotkey('win', '', 'h')  # per lo snipping tool
        self.text_input.focus_set()

    
    def _traduci_testo_lara_btn(self):
        language_mapping = {
            "english": "en-US",
            "italian": "it-IT",
            "japanese": "ja-JP", # Corretto da "ja-JA" a "ja-JP"
            "japanese vert": "ja-JP", # Corretto da "ja-JA" a "ja-JP"
            "french": "fr-FR", # Aggiunto il sottotag del paese per lo standard BCP-47
            "spanish": "es-ES", # Aggiunto il sottotag del paese per lo standard BCP-47
            "korean": "ko-KR", # Corretto da "ko-KO" a "ko-KR"
            "korean vert": "ko-KR", # Corretto da "ko-KO" a "ko-KR"
            "chinesesimplified" : "zh-CN",
            "chinesesimplified vert" : "zh-CN",
            "chinesetraditional": "zh-TW",
            "chinesetraditional vert": "zh-TW"
        }

        lang_orig = self.combo_lingua.get()  # Ottengo il valore dalla combobox
        lngO = language_mapping.get(lang_orig.lower(), "en")  # Converte in lowercase da en se non trova la lingua in language_mapping
        lingua_orig = lngO

        lang_dest = self.combo_lingua_dest.get()
        lngD = language_mapping.get(lang_dest.lower(), "en")  # Converte in lowercase da en se non trova la lingua in language_mapping
        lingua_dest = lngD

        testo = self.text_input.get(1.0, tk.END).strip()

        if not testo:
            self.text_tradotto_lara.delete(1.0, tk.END)
            self.text_tradotto_lara.insert(tk.END, "Nessun testo da tradurre.")
            return
        print("lingue")
        print(lingua_orig)
        print(lingua_dest)
        print(testo)
        LARA_ACCESS_KEY_ID = "7C1902SE7QS94CACQG3SPR2LCC"      # Replace with your Access Key ID
        LARA_ACCESS_KEY_SECRET = "vGA50SUOTswqY6S56_3ms1986_QhLWOfFqEJWsJU_6c"  # Replace with your Access Key SECRET

   
        credentials = Credentials(access_key_id=LARA_ACCESS_KEY_ID, access_key_secret=LARA_ACCESS_KEY_SECRET)
        lara = LaraTranslator(credentials)

        # 3. Effettua la traduzione
        # Specifichiamo la lingua di origine ("en-US") e quella di destinazione ("it-IT")
        res = lara.translate(
            testo,
            source=lingua_orig,
            target=lingua_dest)

        # Prints the translated text: "Ciao, come stai? Questo testo può essere molto lungo."
        print(res.translation)

        testo_tradotto = res.translation

        self.text_tradotto_lara.delete(1.0, tk.END)
        self.text_tradotto_lara.insert(tk.END, testo_tradotto)

    def ensure_translation_installed(self, from_code="en", to_code="ko"):
        """Verifica se il pacchetto di traduzione è già installato, altrimenti lo installa."""
        
        # Get all available packages first
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()

        # Find the specific package we need
        package_to_install = next(
            (p for p in available_packages if p.from_code == from_code and p.to_code == to_code),
            None
        )

        if not package_to_install:
            raise Exception(f"Nessun pacchetto di traduzione trovato per {from_code} → {to_code}")

        # Check if the desired package is already installed
        # We can do this by checking if its 'from_code' and 'to_code' exist in the installed packages
        # This is a more direct way to check for the package presence
        installed_packages = argostranslate.package.get_installed_packages()
        
        is_installed = any(
            p.from_code == from_code and p.to_code == to_code 
            for p in installed_packages
        )

        if not is_installed:
            print(f"Installazione del pacchetto di traduzione da {from_code} a {to_code}...")
            try:
                argostranslate.package.install_from_path(package_to_install.download())
                print("Installazione completata.")
            except Exception as e:
                raise Exception(f"Errore durante l'installazione del pacchetto {from_code} → {to_code}: {e}")
        else:
            print(f"Pacchetto di traduzione da {from_code} a {to_code} già installato.")

            
    def _traduci_testo_argos_btn(self):
        language_mapping = {
            "english": "en",
            "italian": "it",
            "japanese": "ja", # Corretto da "ja-JA" a "ja-JP"
            "japanese vert": "ja", # Corretto da "ja-JA" a "ja-JP"
            "french": "fr", # Aggiunto il sottotag del paese per lo standard BCP-47
            "spanish": "es", # Aggiunto il sottotag del paese per lo standard BCP-47
            "korean": "ko", # Corretto da "ko-KO" a "ko-KR"
            "korean vert": "ko", # Corretto da "ko-KO" a "ko-KR"
            "chinesesimplified" : "zh",
            "chinesesimplified vert" : "zh",
            "chinesetraditional": "zh",
            "chinesetraditional vert": "zh"
        }

        lang_orig = self.combo_lingua.get()  # Ottengo il valore dalla combobox
        lngO = language_mapping.get(lang_orig.lower(), "en")  # Converte in lowercase da en se non trova la lingua in language_mapping
        lingua_orig = lngO

        lang_dest = self.combo_lingua_dest.get()
        lngD = language_mapping.get(lang_dest.lower(), "en")  # Converte in lowercase da en se non trova la lingua in language_mapping
        lingua_dest = lngD

        testo = self.text_input.get(1.0, tk.END).strip()     

        if not testo:
            self.text_tradotto_lara.delete(1.0, tk.END)
            self.text_tradotto_lara.insert(tk.END, "Nessun testo da tradurre.")
            return
        print("lingue")
        print(lingua_orig)
        print(lingua_dest)
        print(testo)
        
        if lingua_orig == "ko": 
            if lingua_dest =="it": 
                lingua_dest = "en"
                self.ensure_translation_installed(lingua_orig, lingua_dest)

                # Carica i modelli installati
                installed_languages = argostranslate.translate.load_installed_languages()
                from_lang = next(lang for lang in installed_languages if lang.code == lingua_orig)
                to_lang = next(lang for lang in installed_languages if lang.code == lingua_dest)

                # Traduzione
                translation = from_lang.get_translation(to_lang)
                testo_tradotto = translation.translate(testo)

                testo = testo_tradotto
                print(testo)

                # Traduci EN → IT
                lingua_orig = "en"
                lingua_dest = "it"
                    



        self.ensure_translation_installed(lingua_orig, lingua_dest)

        # Carica i modelli installati
        installed_languages = argostranslate.translate.load_installed_languages()
        from_lang = next(lang for lang in installed_languages if lang.code == lingua_orig)
        to_lang = next(lang for lang in installed_languages if lang.code == lingua_dest)

        # Traduzione
        translation = from_lang.get_translation(to_lang)
        testo_tradotto = translation.translate(testo)
  
        print(testo_tradotto)

        self.text_tradotto_lara.delete(1.0, tk.END)
        self.text_tradotto_lara.insert(tk.END, testo_tradotto)

    def _traduci_testo_ipa_btn(self):
        language_mapping = {
            "english": "en-US",
            "italian": "it-IT",
            "japanese": "ja-JP", # Corretto da "ja-JA" a "ja-JP"
            "japanese vert": "ja-JP", # Corretto da "ja-JA" a "ja-JP"
            "french": "fr-FR", # Aggiunto il sottotag del paese per lo standard BCP-47
            "spanish": "es-ES", # Aggiunto il sottotag del paese per lo standard BCP-47
            "korean": "ko-KR", # Corretto da "ko-KO" a "ko-KR"
            "korean vert": "ko-KR", # Corretto da "ko-KO" a "ko-KR"
            "chinesesimplified" : "zh-CN",
            "chinesesimplified vert" : "zh-CN",
            "chinesetraditional": "zh-TW",
            "chinesetraditional vert": "zh-TW"
        }

        lang_orig = self.combo_lingua.get()  # Ottengo il valore dalla combobox
        lngO = language_mapping.get(lang_orig.lower(), "en")  # Converte in lowercase da en se non trova la lingua in language_mapping
        lingua_orig = lngO

        lang_dest = self.combo_lingua_dest.get()
        lngD = language_mapping.get(lang_dest.lower(), "en")  # Converte in lowercase da en se non trova la lingua in language_mapping
        lingua_dest = lngD

        testo = self.text_input.get(1.0, tk.END).strip()

        

        if not testo:
            self.text_tradotto_lara.delete(1.0, tk.END)
            self.text_tradotto_lara.insert(tk.END, "Nessun testo da tradurre.")
            return
        
        ##sentence = "I'm tired. Do we really have to do it now?"
        ipa_transcription1 = ipa.convert(testo)

       


        # Trascrizione IPA per l'inglese americano
        ipa_transcription2 = phonemize(testo, language='en-us', backend='espeak',
                              separator=Separator(word=' ', syllable='', phone=''))
        

        ipa_transcription3 = ipa_transcription2.replace('dʒʌst', 'jast')

        ipa_transcription3 = ipa_transcription3.replace('tʃɪkɪn', 'ciken')

    
 

        testo_tradotto = ipa_transcription1 + "\n" + ipa_transcription2 + "\n" + ipa_transcription3
        
        print(testo_tradotto)

        self.text_tradotto_lara.delete(1.0, tk.END)
        self.text_tradotto_lara.insert(tk.END, testo_tradotto)


    def _traduci_testo_deep_btn(self):
        language_mapping = {
            "english": "en-US",
            "italian": "it-IT",
            "japanese": "ja-JP", # Corretto da "ja-JA" a "ja-JP"
            "japanese vert": "ja-JP", # Corretto da "ja-JA" a "ja-JP"
            "french": "fr-FR", # Aggiunto il sottotag del paese per lo standard BCP-47
            "spanish": "es-ES", # Aggiunto il sottotag del paese per lo standard BCP-47
            "korean": "ko-KR", # Corretto da "ko-KO" a "ko-KR"
            "korean vert": "ko-KR", # Corretto da "ko-KO" a "ko-KR"
            "chinesesimplified" : "zh-CN",
            "chinesesimplified vert" : "zh-CN",
            "chinesetraditional": "zh-TW",
            "chinesetraditional vert": "zh-TW"
        }

        lang_orig = self.combo_lingua.get()  # Ottengo il valore dalla combobox
        lngO = language_mapping.get(lang_orig.lower(), "en")  # Converte in lowercase da en se non trova la lingua in language_mapping
        lingua_orig = lngO

        lang_dest = self.combo_lingua_dest.get()
        lngD = language_mapping.get(lang_dest.lower(), "en")  # Converte in lowercase da en se non trova la lingua in language_mapping
        lingua_dest = lngD

        testo = self.text_input.get(1.0, tk.END).strip()

        if not testo:
            self.text_tradotto_lara.delete(1.0, tk.END)
            self.text_tradotto_lara.insert(tk.END, "Nessun testo da tradurre.")
            return
        print("lingue")
        print(lingua_orig)
        print(lingua_dest)
        print(testo)

        translator = MyMemoryTranslator(source=lingua_orig, target=lingua_dest)
 

        testo_tradotto = translator.translate(testo)  # Tradotto in italiano
        
        print(testo_tradotto)

        self.text_tradotto_lara.delete(1.0, tk.END)
        self.text_tradotto_lara.insert(tk.END, testo_tradotto)



    def _traduci_testo_btn(self):
        language_mapping = {         
            "english": "en",
            "italian": "it",
            "japanese": "ja",
            "japanese vert": "ja",
            "french": "fr",
            "spanish": "es",
            "korean": "ko",
            "korean vert": "ko",
            "chinesesimplified" : "zh-CN",
            "chinesesimplified vert" : "zh-CN",
            "chinesetraditional": "zh-TW",
            "chinesetraditional vert": "zh-TW"
        }

        lang_orig = self.combo_lingua.get()  # Ottengo il valore dalla combobox
        lngO = language_mapping.get(lang_orig.lower(), "en")  # Converte in lowercase da en se non trova la lingua in language_mapping
        lingua_orig = lngO

        lang_dest = self.combo_lingua_dest.get()
        lngD = language_mapping.get(lang_dest.lower(), "en")  # Converte in lowercase da en se non trova la lingua in language_mapping
        lingua_dest = lngD

        testo = self.text_input.get(1.0, tk.END).strip()

        if not testo:
            self.text_tradotto.delete(1.0, tk.END)
            self.text_tradotto.insert(tk.END, "Nessun testo da tradurre.")
            return
        print("lingue")
        print(lingua_orig)
        print(lingua_dest)
        translator = GoogleTranslator()
        try:
            testo_tradotto = translator.translate(testo, dest=lingua_dest, src=lingua_orig).text
        except Exception as e:
            testo_tradotto = f"Errore nella traduzione: {str(e)}"

        self.text_tradotto.delete(1.0, tk.END)
        self.text_tradotto.insert(tk.END, testo_tradotto)

    def _riproduci_audio_originale_mac_siri(self, testo_tradotto, velocita=140):
        """
        Riproduce il testo tradotto usando una voce simile a Siri su macOS.
        Questa funzione è pensata per essere eseguita in un thread separato.
        """
        # Inizializza il motore di sintesi vocale
        engine = pyttsx3.init()

        # Imposta la velocità
        # Usiamo il parametro 'velocita' passato alla funzione, se non specificato, userà 140.
        engine.setProperty('rate', velocita)

        # Cerca e imposta una voce che assomigli a Siri o sia di alta qualità
        siri_like_voice_found = False
        voices = engine.getProperty('voices')

        # IDs comuni per voci simili a Siri su macOS (possono variare tra le versioni di macOS)
        preferred_siri_like_voices = [
            "com.apple.ttsbundle.siri_female_en-US_compact",
            "com.apple.ttsbundle.siri_male_en-US_compact",
            "com.apple.ttsbundle.Nicky-compact",
            "com.apple.ttsbundle.Aaron-compact",
            "com.apple.speech.synthesis.voice.samantha",
            "com.apple.speech.synthesis.voice.alex"
        ]

        # Prova a trovare una delle voci preferite
        for preferred_id in preferred_siri_like_voices:
            for voice in voices:
                if voice.id == preferred_id:
                    engine.setProperty('voice', voice.id)
                    siri_like_voice_found = True
                    print(f"Voce impostata su una simile a Siri: {voice.name} (ID: {voice.id})")
                    break
            if siri_like_voice_found:
                break

        if not siri_like_voice_found:
            print("Nessuna voce specificamente simile a Siri trovata. Tentativo di trovare una voce inglese di alta qualità.")
            # Fallback: cerca una voce inglese di alta qualità
            for voice in voices:
                if any('en' in lang.lower() for lang in voice.languages) and \
                ("premium" in voice.name.lower() or "compact" in voice.id.lower() or "enhanced" in voice.name.lower()):
                    engine.setProperty('voice', voice.id)
                    siri_like_voice_found = True
                    print(f"Voce impostata su una voce inglese di alta qualità: {voice.name} (ID: {voice.id})")
                    break

        if not siri_like_voice_found:
            print("Nessuna voce simile a Siri o di alta qualità trovata. Verrà utilizzata la voce di default.")

        # Riproduci il testo in inglese
        engine.say(testo_tradotto)
        engine.runAndWait()

        # Ferma il motore dopo la riproduzione
        engine.stop()

    def riproduci_in_background(self, testo, velocita=140):
        """
        Avvia la riproduzione audio in un thread separato.
        """
        # Creazione del thread.
        # Il 'target' è la funzione che il thread eseguirà.
        # 'args' sono gli argomenti da passare alla funzione target, devono essere una tupla.
        audio_thread = threading.Thread(
            target=self._riproduci_audio_originale_mac_siri,
            args=(testo, velocita)
        )
        # Avvia il thread.
        audio_thread.start()
        print("Riproduzione audio avviata in background...")

    def _riproduci_audio_originale_mac(self, testo_tradotto, velocita):
        
        
        if sys.platform == "darwin":  # Mac OS X                                                                     
            language = self.combo_lingua.get()

            language_mapping = {
                "english": "en",
                "italian": "it",
                "japanese": "ja",
                "french": "fr",
                "spanish": "es",
                "korean": "ko",
                "chinesesimplified" : "zh-CN",
                "chinesetraditional": "zh-CN"
            }

            lng = language_mapping.get(language.lower(), "en")  # Converte in lowercase da en se non trova la lingua in language_mapping
            print(language)
            print(lng)  # Output: en
            if testo_tradotto:
                voce = self.voice_var.get()
                if self.rimuovo_audio_var.get():
                    print("Il file audio non viene creato")
                    if velocita == 0: 
                        #subprocess.run(["say", "-v", voce, testo_tradotto])
                        voce_scelta = voce # Assicurati che questa voce sia disponibile sul tuo sistema
                        testo_da_pronunciare = testo_tradotto

                        print("Avvio della pronuncia in un thread separato...")

                        # Crea un nuovo thread
                        # Il target è la funzione che vogliamo eseguire nel thread
                        # Gli args sono i parametri da passare alla funzione
                        say_thread = threading.Thread(target=pronuncia_testo, args=(voce_scelta, testo_da_pronunciare))

                        # Avvia il thread
                        say_thread.start()

                    else:
                        print("siri")
                        #subprocess.run(["say", "-v", voce, testo_tradotto])
                        voce_scelta = voce # Assicurati che questa voce sia disponibile sul tuo sistema
                        testo_da_pronunciare = testo_tradotto

                        print("Avvio della pronuncia in un thread separato...")

                        # Crea un nuovo thread
                        # Il target è la funzione che vogliamo eseguire nel thread
                        # Gli args sono i parametri da passare alla funzione
                        say_thread = threading.Thread(target=pronuncia_testo_lento, args=(voce_scelta, testo_da_pronunciare))

                        # Avvia il thread
                        say_thread.start()

                        
                    
                else:
                    print("Riproduco e creo il file audio")
                    now = datetime.datetime.now()
                    timestamp = now.strftime("%H_%M_%S_%f")[:-3]  # es. 14_23_45_123
                    audio_file = f"output_{timestamp}.aiff"
                    percorso_file = os.path.join(self.output_folder.get(), audio_file)  # Percorso completo al file
                    if os.path.exists(os.path.dirname(percorso_file)):
                        percorso_file = percorso_file
                    else:
                        base_dir = os.path.dirname(os.path.abspath(__file__))
                        percorso_file = os.path.join(base_dir, audio_file)  # Percorso completo al file

                    
                    subprocess.run(["say", "-v", voce, testo_tradotto])
                    subprocess.run(["say", "-v", voce, "-o", percorso_file, testo_tradotto])
                    
               


        elif sys.platform == "win32":
            # Frame per l'anteprima dell'immagine
            language = self.combo_lingua.get()

            language_mapping = {
                "english": "en",
                "italian": "it",
                "japanese": "ja",
                "french": "fr",
                "spanish": "es",
                "korean": "ko",
                "chinesesimplified" : "zh-CN",
                "chinesetraditional": "zh-CN"
            }

            lng = language_mapping.get(language.lower(), "en")  # Converte in lowercase da en se non trova la lingua in language_mapping
            print(language)
            print(lng)  # Output: en
            #  AProcess.Executable := 'balcon.exe';
            #  AProcess.Parameters.Add('-n "' + VoiceWindows + '" -t "' + s + '"');
            print("windows ")
            if testo_tradotto:
                voce = self.voice_var.get()
                try:
                    subprocess.run(["balcon.exe", "-t", testo_tradotto, "-v", voce], check=True)
                except FileNotFoundError:
                    tk.messagebox.showerror("Errore", "balcon.exe non trovato.")
                except subprocess.CalledProcessError as e:
                    tk.messagebox.showerror("Errore", f"Errore durante la riproduzione audio: {e}")
       

    
    # FUNZIONE HELPER PER LA RIPRODUZIONE AUDIO (Target del thread)
    def _esegui_riproduzione_audio_gtts(self, testo, lingua_codice, slow_play, rimuovi_file, output_folder):
        try:
            now = datetime.datetime.now()
            timestamp = now.strftime("%H_%M_%S_%f")[:-3]
            audio_file = f"temp_audio_{timestamp}.mp3"

            # Determina il percorso del file audio
            # Verifica se la cartella di output esiste, altrimenti usa la directory dello script
            if not os.path.exists(output_folder):
                base_dir = os.path.dirname(os.path.abspath(__file__))
                output_folder = base_dir # Fallback
                print(f"ATTENZIONE: Cartella di output non valida o non trovata. Salvataggio in: {output_folder}")
            
            percorso_file = os.path.join(output_folder, audio_file)

            # 1. Genera e salva il file audio
            tts = gTTS(text=testo, lang=lingua_codice, slow=slow_play)
            tts.save(percorso_file)
            print(f"DEBUG: File audio generato: {percorso_file}")

            # 2. Inizializza e riproduci con pygame
            pygame.mixer.init()
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            pygame.mixer.music.load(percorso_file)
            pygame.mixer.music.play()
            print("DEBUG: Riproduzione avviata.")

            # Attendi che il suono finisca
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10) # Non bloccare completamente la CPU
            print("DEBUG: Riproduzione terminata.")

            pygame.mixer.quit() # Importante: de-inizializza il mixer

            # 3. Rimuovi il file se richiesto
            if os.path.exists(percorso_file) and rimuovi_file:
                print("DEBUG: Cancellazione del file audio.")
                os.remove(percorso_file)
            elif not rimuovi_file:
                print("DEBUG: Il file audio non viene eliminato (impostazione utente).")

        except Exception as e:
            print(f"ERRORE GRAVE nel thread di riproduzione audio: {e}")
            # Se vuoi un messagebox, devi farlo nel thread principale usando root.after()
            # Esempio: self.root.after(0, lambda: messagebox.showerror("Errore Audio", f"Errore: {e}"))
            # Per fare questo, la funzione _esegui_riproduzione_audio_gtts dovrebbe ricevere self.root.after come argomento.
            # Per ora, lascio solo print per non complicare troppo.


        

    # La funzione principale che AVVIA IL THREAD per gTTS
    def _riproduci_audio_originale(self, testo_tradotto):
        language = self.combo_lingua.get()
        language_mapping = {
            "english": "en", "italian": "it", "japanese": "ja", "french": "fr",
            "spanish": "es", "korean": "ko", "chinesesimplified" : "zh-CN",
            "chinesetraditional": "zh-CN"
        }
        lng = language_mapping.get(language.lower(), "en")
        print(f"DEBUG: Lingua selezionata: {language}, Codice: {lng}")

        if testo_tradotto.strip():
            # Esempio di utilizzo
          
            risultato = aggiungi_virgola_dopo_parola(testo_tradotto)
            print(risultato)
  
            slow_play = self.play_lento_var.get()
            rimuovi_file = self.rimuovo_audio_var.get()
            output_folder = self.output_folder.get() # Recupera il valore qui!

            # Crea e avvia il thread
            audio_thread = threading.Thread(
                target=self._esegui_riproduzione_audio_gtts,
                # CORREZIONE: Passa output_folder come ultimo argomento
                args=(testo_tradotto, lng, slow_play, rimuovi_file, output_folder) 
            )
            audio_thread.daemon = True
            audio_thread.start()
            print("DEBUG: Thread di riproduzione audio (gTTS) avviato.")
        else:
            print("DEBUG: Testo vuoto, riproduzione annullata.")


    # La funzione principale che AVVIA IL THREAD per gTTS
    def _riproduci_audio_originaleLento(self, testo_tradotto):
        language = self.combo_lingua.get()
        language_mapping = {
            "english": "en", "italian": "it", "japanese": "ja", "french": "fr",
            "spanish": "es", "korean": "ko", "chinesesimplified" : "zh-CN",
            "chinesetraditional": "zh-CN"
        }
        lng = language_mapping.get(language.lower(), "en")
        print(f"DEBUG: Lingua selezionata: {language}, Codice: {lng}")

        if testo_tradotto.strip():
            # Esempio di utilizzo
          
            risultato = aggiungi_virgola_dopo_parola(testo_tradotto)
            print(risultato)
  
            slow_play = self.play_lento_var.get()
            rimuovi_file = self.rimuovo_audio_var.get()
            output_folder = self.output_folder.get() # Recupera il valore qui!

            # Crea e avvia il thread
            audio_thread = threading.Thread(
                target=self._esegui_riproduzione_audio_gtts,
                # CORREZIONE: Passa output_folder come ultimo argomento
                args=(risultato, lng, slow_play, rimuovi_file, output_folder) 
            )
            audio_thread.daemon = True
            audio_thread.start()
            print("DEBUG: Thread di riproduzione audio (gTTS) avviato.")
        else:
            print("DEBUG: Testo vuoto, riproduzione annullata.")


    def _riproduci_audio_tradotto(self, testo_tradotto):
        language = self.combo_lingua_dest.get()

        language_mapping = {
            "english": "en",
            "italian": "it",
            "japanese": "ja",
            "french": "fr",
            "spanish": "es",
            "korean": "ko",
            "chinesesimplified" : "zh-CN",
            "chinesetraditional": "zh-CN"
        }

        lng = language_mapping.get(language.lower(), "en")
        if testo_tradotto:
            
            
            now = datetime.datetime.now()
            timestamp = now.strftime("%H_%M_%S_%f")[:-3]  # es. 14_23_45_123
            audio_file = f"temp_audio_trad{timestamp}.mp3"

            percorso_file = os.path.join(self.output_folder.get(), audio_file)  # Percorso completo al file
            if os.path.exists(os.path.dirname(percorso_file)):
                percorso_file = percorso_file
            else:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                percorso_file = os.path.join(base_dir, audio_file)  # Percorso completo al file
                
            tts = gTTS(testo_tradotto, lang=lng, slow=self.play_lento_var.get())
            tts.save(percorso_file)

            pygame.mixer.init()
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            pygame.mixer.music.load(percorso_file)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            pygame.mixer.quit()
            if os.path.exists(percorso_file):
                if self.rimuovo_audio_var.get():
                    print("Cancello il file audio")
                    os.remove(percorso_file)
                else:
                    print("Il file audio non viene eliminato")















     #############  INIZIA CATTURA 



    # Nuovo handler per il pulsante "Cattura" (se vuoi solo catturare senza OCR immediato)
    def _cattura_schermo_button_handler(self):
        self.after_capture_callback = self._handle_manual_capture_completion # Imposta una callback per la sola cattura
        self._cattura_schermo()

    def _handle_manual_capture_completion(self, captured_file_path):
        # Questo viene chiamato quando la cattura è completata dal pulsante "Cattura"
        self.after_capture_callback = None # Resetta la callback
        if captured_file_path:
            self.text_input.delete(1.0, tk.END)
            self.text_input.insert(tk.END, f"Cattura completata. Immagine salvata in: {captured_file_path}")
            self.last_captured_image_path = captured_file_path
        else:
            self.text_input.delete(1.0, tk.END)
            self.text_input.insert(tk.END, "Cattura annullata o fallita.")

    def _cattura_schermo(self):
        if sys.platform == "darwin":  # Mac OS X
            self.root.withdraw()  # Nasconde la finestra principale
            self.root.update()  # Forza aggiornamento per nasconderla davvero

            # Piccola pausa per assicurarsi che la finestra sparisca del tutto
            time.sleep(0.3)

            user_home = os.path.expanduser("~")
            file_path = os.path.join(user_home, "temp.jpg")
            subprocess.run(["screencapture", "-i", file_path])
            print(file_path)

            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            save_path = os.path.join(desktop_path, "test_image.jpg")
            print(save_path)

            self.root.deiconify()  # Rende visibile la finestra principale
            if self.after_capture_callback:
                # Diamo un piccolo ritardo per permettere a macOS di salvare il file
                self.root.after(500, lambda: self.after_capture_callback(file_path))


        elif sys.platform == "win32":
            # Frame per l'anteprima dell'immagine
            # Non creare il frame qui, ma solo in __init__ o dove viene mostrato.
            # Se è già creato in __init__, non c'è bisogno di crearlo di nuovo qui.
            # Assicurati che self.preview_frame esista se lo usi.
            # Per ora, commento la creazione, assumendo che esista già o non sia necessario per il flusso corrente.
            # self.preview_frame = tk.Frame(self.root)
            # self.preview_frame.pack(fill="both", expand=True, pady=0, padx=0)
            # self.preview_frame.grid_rowconfigure(0, weight=1)
            # self.preview_frame.grid_columnconfigure(0, weight=1)

            try:
                self.start_capture()
            except Exception as e:
                messagebox.showerror("Errore", f"Errore durante la cattura: {e}")

    def start_capture(self):
        self.root.withdraw()
        self.root.update_idletasks()
        time.sleep(0.3)

        self.full_screenshot = ImageGrab.grab()

        self.capture_window = tk.Toplevel(self.root)
        self.capture_window.attributes("-fullscreen", True)
        self.capture_window.attributes("-alpha", 0.2)

        self.canvas = tk.Canvas(self.capture_window, cursor="crosshair")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.canvas.update()

    def on_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)
            self.selection_rect = None

    def on_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)

        x1, y1 = (min(self.start_x, cur_x), min(self.start_y, cur_y))
        x2, y2 = (max(self.start_x, cur_x), max(self.start_y, cur_y))

        if not self.selection_rect:
            self.selection_rect = self.canvas.create_rectangle(
                x1, y1, x2, y2, outline="red", width=5)
        else:
            self.canvas.coords(self.selection_rect, x1, y1, x2, y2)

    def on_release(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)

        x1 = int(min(self.start_x, self.end_x))
        y1 = int(min(self.start_y, self.end_y))
        x2 = int(max(self.start_x, self.end_x))
        y2 = int(max(self.start_y, self.end_y))

        bbox = (x1, y1, x2, y2)
        
        # Ritaglia l'immagine originale
        self.cropped_image = self.full_screenshot.crop(bbox)
        print("Immagine ritagliata.")
        
        # Salva l'immagine ritagliata
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        # Genera un nome file unico per evitare conflitti e permettere catture multiple
        #timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        #desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        FilePath = os.path.join(desktop_path, "test_image.jpg")
        
        self.last_captured_image_path = os.path.join(desktop_path, f"test_image.jpg")
        
        try:
            self.cropped_image.save(self.last_captured_image_path)
            print(f"Immagine salvata in: {self.last_captured_image_path}")
            # Non mostrare messagebox qui, il flusso continua
        except Exception as e:
            messagebox.showerror("Errore di salvataggio", f"Errore nel salvataggio del file:\n{str(e)}")
            self.last_captured_image_path = None # Se il salvataggio fallisce, resetta il path

        self.capture_window.destroy()
        self.root.deiconify()
        self.root.attributes('-topmost', True) # Porta la finestra in primo piano
        self.root.attributes('-topmost', False) # Rimuove l'attributo dopo averla portata in primo piano
        
        # Esegui la callback solo dopo che l'immagine è stata salvata
        if self.after_capture_callback:
            self.after_capture_callback(self.last_captured_image_path)

    def update_preview(self):
        # Questo metodo era per la preview in-app, che non è più direttamente usata nel flusso OCR.
        # Puoi rimuoverlo se non hai un widget per la preview visibile.
        # O aggiornalo per mostrare l'immagine nel tuo layout se lo desideri.
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()

