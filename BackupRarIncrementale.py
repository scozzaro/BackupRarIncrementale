import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from tkinter import simpledialog
from tkinter import ttk
import subprocess
import threading
import queue
import os
import sys
import json
import urllib.request
import fnmatch

# --- Classe per l'applicazione GUI ---
class BackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Backup con RAR")
        self.root.geometry("700x800")
        self.is_running = False
        self.output_queue = queue.Queue()

        # Variabili di stato dinamiche
        self.current_backup_file = "backup_config.rbak"

        # --- Creazione della barra dei menu ---
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menu File
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Salva Configurazione", command=self.save_backup_data)
        file_menu.add_command(label="Carica Configurazione", command=self.load_backup_data)
        file_menu.add_separator()
        file_menu.add_command(label="Esci", command=self.root.quit)

        # Menu Info
        info_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Info", menu=info_menu)
        info_menu.add_command(label="Licenza", command=self.show_license)
        info_menu.add_command(label="About", command=self.show_about)

        # --- Frame principale per l'interfaccia utente ---
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Sezione per il nome del backup ---
        self.backup_name_label = tk.Label(main_frame, text=f"File di configurazione: {self.current_backup_file}", font=("Arial", 12, "bold"))
        self.backup_name_label.pack(pady=5)

        # --- Sezione per il percorso di WinRAR/RAR ---
        rar_path_frame = tk.LabelFrame(main_frame, text="Percorso di WinRAR/RAR")
        rar_path_frame.pack(fill=tk.X, pady=5, padx=5)
        self.rar_path_entry = tk.Entry(rar_path_frame)
        self.rar_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        browse_rar_button = tk.Button(rar_path_frame, text="Trova Programma", command=self.browse_rar)
        browse_rar_button.pack(side=tk.LEFT, padx=5)

        # Imposta il percorso di default a seconda del sistema operativo
        if sys.platform == "win32":
            self.rar_path_entry.insert(0, "C:\\Program Files\\WinRAR\\WinRAR.exe")
        elif sys.platform == "darwin": # macOS
            self.rar_path_entry.insert(0, "/usr/local/bin/rar")
        else: # Linux e altri
            self.rar_path_entry.insert(0, "/usr/local/bin/rar")

        # --- Sezione per la destinazione del backup ---
        dest_frame = tk.LabelFrame(main_frame, text="Destinazione Backup")
        dest_frame.pack(fill=tk.X, pady=5, padx=5)
        self.dest_entry = tk.Entry(dest_frame)
        self.dest_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        browse_button = tk.Button(dest_frame, text="Trova Percorso", command=self.browse_destination)
        browse_button.pack(side=tk.LEFT, padx=5)

        # Imposta la destinazione di default
        self.dest_entry.insert(0, os.path.join(os.path.expanduser('~'), 'Backup'))

        # --- Sezione per il nome del file di backup ---
        file_frame = tk.LabelFrame(main_frame, text="Nome File Archivio")
        file_frame.pack(fill=tk.X, pady=5, padx=5)
        self.archive_name_entry = tk.Entry(file_frame)
        self.archive_name_entry.pack(fill=tk.X, padx=5)
        # Imposta il nome dell'archivio di default
        self.archive_name_entry.insert(0, 'IlMioBackup.rar')

        # --- Sezione per la selezione delle cartelle ---
        folders_frame = tk.LabelFrame(main_frame, text="Cartelle da salvare")
        folders_frame.pack(fill=tk.X, pady=5, padx=5)
        self.folders_listbox = tk.Listbox(folders_frame, selectmode=tk.SINGLE, height=5)
        self.folders_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        button_frame = tk.Frame(folders_frame)
        button_frame.pack(side=tk.RIGHT, padx=5)
        add_button = tk.Button(button_frame, text="+", command=self.add_folder_to_list)
        add_button.pack(fill=tk.X)
        remove_button = tk.Button(button_frame, text="-", command=self.remove_folder_from_list)
        remove_button.pack(fill=tk.X, pady=5)

        # --- NOVITÀ: Sezione per file/cartelle da escludere ---
        exclude_frame = tk.LabelFrame(main_frame, text="Escludi file/cartelle (pattern *.tmp, *.zip, C:\\temp\\*)")
        exclude_frame.pack(fill=tk.X, pady=5, padx=5)
        self.exclude_listbox = tk.Listbox(exclude_frame, selectmode=tk.SINGLE, height=5)
        self.exclude_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        exclude_button_frame = tk.Frame(exclude_frame)
        exclude_button_frame.pack(side=tk.RIGHT, padx=5)
        tk.Button(exclude_button_frame, text="+", command=self.add_exclude_to_list).pack(fill=tk.X)
        tk.Button(exclude_button_frame, text="-", command=self.remove_exclude_from_list).pack(fill=tk.X, pady=5)

        # Altri widget di stato e output
        self.progress_frame = tk.Frame(main_frame)
        self.progress_frame.pack(fill=tk.X, pady=5)

        self.progress_label = tk.Label(self.progress_frame, text="Progresso: 0%")
        self.progress_label.pack(side=tk.LEFT, padx=(0, 10))

        self.progressbar = ttk.Progressbar(self.progress_frame, orient='horizontal', length=500, mode='determinate')
        self.progressbar.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.status_label = tk.Label(main_frame, text="Pronto.")
        self.status_label.pack(pady=5)
        
        self.start_button = tk.Button(main_frame, text="Esegui Backup", command=self.start_backup)
        self.start_button.pack(pady=10)
        self.output_memo = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=15)
        self.output_memo.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # --- Caricamento automatico della configurazione all'avvio ---
        script_dir = os.path.dirname(os.path.abspath(__file__))
        auto_load_file = os.path.join(script_dir, "backup_config.rbak")
        if os.path.exists(auto_load_file):
            self.load_backup_data(file_path=auto_load_file)
        else:
            self.status_label.config(text="Pronto. Nessun file di configurazione trovato all'avvio.")

    # --- Gestione lista esclusioni ---
    def add_exclude_to_list(self):
        pattern = tk.simpledialog.askstring("Aggiungi esclusione", "Inserisci estensione/cartella da escludere (es: *.tmp o C:\\temp\\*):")
        if pattern:
            if pattern not in self.exclude_listbox.get(0, tk.END):
                self.exclude_listbox.insert(tk.END, pattern)

    def remove_exclude_from_list(self):
        selected_indices = self.exclude_listbox.curselection()
        if selected_indices:
            self.exclude_listbox.delete(selected_indices[0])

    def show_license(self):
        """Mostra la finestra di dialogo della licenza."""
        license_window = tk.Toplevel(self.root)
        license_window.title("Licenza")
        license_window.geometry("600x400")

        text_area = scrolledtext.ScrolledText(license_window, wrap=tk.WORD)
        text_area.pack(expand=True, fill="both", padx=10, pady=10)
        text_area.insert(tk.END, "Caricamento della Licenza Pubblica di Mozilla (MPL-2.0)...")

        def fetch_license_text():
            try:
                # URL della licenza MPL-2.0
                url = "https://www.mozilla.org/media/MPL/2.0/index.815ca99b2447.txt"
                with urllib.request.urlopen(url) as response:
                    license_text = response.read().decode('utf-8')
                text_area.delete('1.0', tk.END)
                text_area.insert(tk.END, license_text)
            except Exception as e:
                text_area.delete('1.0', tk.END)
                text_area.insert(tk.END, f"Errore durante il caricamento della licenza: {e}\n\n"
                                        "Il programma è rilasciato sotto la Licenza Pubblica di Mozilla (MPL-2.0). "
                                        "Puoi trovare il testo completo a questo indirizzo: "
                                        "https://www.mozilla.org/en-US/MPL/2.0/")
            finally:
                text_area.config(state=tk.DISABLED)

        threading.Thread(target=fetch_license_text, daemon=True).start()

    def show_about(self):
        """Mostra la finestra di dialogo 'About'."""
        messagebox.showinfo(
            "About",
            "Autore: Vincenzo Scozzaro\n"
            "Programma free sotto la licenza Mozilla"
        )

    def browse_rar(self):
        """Apre una finestra di dialogo per selezionare il programma rar."""
        selected_file = filedialog.askopenfilename(
            title="Seleziona l'eseguibile di RAR o WinRAR",
            filetypes=[("Eseguibili", "*.exe;*"), ("Tutti i file", "*.*")]
        )
        if selected_file:
            self.rar_path_entry.delete(0, tk.END)
            self.rar_path_entry.insert(0, selected_file)

    def browse_destination(self):
        """Apre una finestra di dialogo per selezionare la cartella di destinazione."""
        selected_path = filedialog.askdirectory(initialdir=self.dest_entry.get())
        if selected_path:
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, selected_path)

    def save_backup_data(self):
        """Salva la configurazione del backup in un file JSON."""
        nome_senza_estensione, estensione = os.path.splitext(self.current_backup_file)
        print(self.current_backup_file)
        print(nome_senza_estensione)
        print(estensione)
        file_path = filedialog.asksaveasfilename(
            defaultextension=".rbak",
            filetypes=[("RAR Backup", "*.rbak")],
            initialfile=nome_senza_estensione
        )
        if not file_path:
            return
        data = {
            "folders": list(self.folders_listbox.get(0, tk.END)),
            "excludes": list(self.exclude_listbox.get(0, tk.END)),
            "destination_folder": self.dest_entry.get(),
            "archive_name": self.archive_name_entry.get(),
            "rar_path": self.rar_path_entry.get()
        }
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            self.current_backup_file = os.path.basename(file_path)
            self.backup_name_label.config(text=f"File di configurazione: {self.current_backup_file}")
            self.status_label.config(text="Configurazione salvata con successo! 🎉")
        except Exception as e:
            self.status_label.config(text=f"Errore durante il salvataggio: {e}")

    def load_backup_data(self, file_path=None):
        """Carica la configurazione del backup da un file JSON."""
        if file_path is None:
            file_path = filedialog.askopenfilename(
                defaultextension=".rbak",
                filetypes=[("RAR Backup", "*.rbak")]
            )
            if not file_path:
                return
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            self.folders_listbox.delete(0, tk.END)
            self.exclude_listbox.delete(0, tk.END)
            self.dest_entry.delete(0, tk.END)
            self.archive_name_entry.delete(0, tk.END)
            self.rar_path_entry.delete(0, tk.END)
            for folder in data.get("folders", []):
                self.folders_listbox.insert(tk.END, folder)
            for pattern in data.get("excludes", []):
                self.exclude_listbox.insert(tk.END, pattern)

            self.dest_entry.insert(0, data.get("destination_folder", os.path.join(os.path.expanduser('~'), 'Backup')))
            self.archive_name_entry.insert(0, data.get("archive_name", "IlMioBackup.rar"))
            self.rar_path_entry.insert(0, data.get("rar_path", ""))
            self.current_backup_file = os.path.basename(file_path)
            self.backup_name_label.config(text=f"File di configurazione: {self.current_backup_file}")
            self.status_label.config(text="Configurazione caricata con successo! 👍")
        except FileNotFoundError:
            self.status_label.config(text="Errore: File non trovato.")
        except json.JSONDecodeError:
            self.status_label.config(text="Errore: File JSON non valido.")
        except Exception as e:
            self.status_label.config(text=f"Errore durante il caricamento: {e}")

    def add_folder_to_list(self):
        """Apre una finestra di dialogo per selezionare una cartella e la aggiunge alla lista."""
        folder_path = filedialog.askdirectory(initialdir=os.path.expanduser('~'))
        if folder_path:
            if folder_path not in self.folders_listbox.get(0, tk.END):
                self.folders_listbox.insert(tk.END, folder_path)
            else:
                self.status_label.config(text="Cartella già presente nella lista.")

    def remove_folder_from_list(self):
        """Rimuove la cartella selezionata dalla lista."""
        selected_indices = self.folders_listbox.curselection()
        if selected_indices:
            self.folders_listbox.delete(selected_indices[0])

    def update_gui(self):
        try:
            while True:
                line = self.output_queue.get_nowait()
                if line is None:
                    self.on_backup_complete()
                    break

                if line.startswith("progress:"):
                    progress_value = int(line.split(':')[1])
                    self.progressbar['value'] = progress_value
                    self.progress_label.config(text=f"Avanzamento: {progress_value}%")
                elif line.startswith("files_processed:"):
                    self.status_label.config(text=f"Elaborazione: {line.split(':')[1].strip()} file")
                else:
                    self.output_memo.insert(tk.END, line)
                    self.output_memo.see(tk.END)
        except queue.Empty:
            self.root.after(100, self.update_gui)

    def on_backup_complete(self):
        """Gestisce il completamento del backup."""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.status_label.config(text="Backup completato! 🎉")

    def pre_calculate_files(self, folders, excludes):
        total_files = 0
        try:
            for folder in folders:
                if os.path.exists(folder):
                    for dirpath, dirnames, filenames in os.walk(folder):
                        # Filtra i file basandosi sulle esclusioni
                        filenames_filtered = [f for f in filenames if not self.is_excluded(f, excludes)]
                        total_files += len(filenames_filtered)
            return total_files
        except Exception as e:
            self.output_queue.put(f"Errore nel calcolo dei file: {e}\n")
            return 0

    def is_excluded(self, filename, excludes):
        """Verifica se un file deve essere escluso in base ai pattern."""
        for pattern in excludes:
            if fnmatch.fnmatch(filename, pattern):
                return True
        return False

    def run_rar_command(self):
        """Esegue il comando rar in un thread separato."""
        try:
            source_folders = list(self.folders_listbox.get(0, tk.END))
            exclude_patterns = list(self.exclude_listbox.get(0, tk.END))

            # Calcola il numero totale di file da elaborare
            self.output_queue.put("Calcolo del numero totale di file...\n")
            total_files = self.pre_calculate_files(source_folders, exclude_patterns)
            files_processed = 0
            self.output_queue.put(f"Trovati {total_files} file da archiviare.\n")
            
            dest_folder = self.dest_entry.get()
            archive_name = self.archive_name_entry.get()
            rar_path = self.rar_path_entry.get().strip()

            if not source_folders:
                self.output_queue.put("Nessuna cartella selezionata per il backup.\n")
                self.output_queue.put(None)
                return
            if not dest_folder or not archive_name:
                self.output_queue.put("Specificare un percorso e un nome per l'archivio.\n")
                self.output_queue.put(None)
                return

            backup_archive = os.path.join(dest_folder, archive_name)
            os.makedirs(dest_folder, exist_ok=True)

            if rar_path and os.path.exists(rar_path):
                command = [rar_path, 'a', '-u', '-r', backup_archive]
            else:
                self.output_queue.put("Avviso: Percorso di RAR/WinRAR non valido o non specificato. Tentativo di usare 'rar' dal PATH di sistema.\n")
                command = ['rar', 'a', '-u', '-r', backup_archive]

            for pattern in exclude_patterns:
                command.append(f"-x{pattern}")
            
            command.extend(source_folders)

            if sys.platform == "win32":
                output_encoding = 'cp850'
            else:
                output_encoding = 'utf-8'

            process = subprocess.Popen(command,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT,
                                       text=False,
                                       cwd=os.path.expanduser('~'))

            for line in process.stdout:
                try:
                    decoded_line = line.decode(output_encoding, errors='replace')
                    self.output_queue.put(decoded_line)

                    # --- Logica di aggiornamento della progress bar ---
                    if any(word in decoded_line for word in ["Aggiunta", "Updating", "Adding", "Compressing", "Creating"]):
                        files_processed += 1
                        if total_files > 0:
                            progress_percent = int((files_processed / total_files) * 100)
                            self.output_queue.put(f"progress:{progress_percent}\n")
                            self.output_queue.put(f"files_processed:{files_processed}/{total_files}\n")

                except Exception as e:
                    self.output_queue.put(f"Errore di decodifica: {e}\n")
                    self.output_queue.put(line.decode('utf-8', errors='replace'))

            process.wait()

            # Imposta la progress bar al 100% solo a backup completato
            self.output_queue.put("progress:100\n") 
            self.output_queue.put(None)
            process.wait()
            self.output_queue.put(None)
        except FileNotFoundError:
            error_msg = "ERRORE: Il comando 'rar' non è stato trovato.\nAssicurati che sia installato e che il suo percorso sia corretto nel programma.\n"
            self.output_queue.put(error_msg)
            self.output_queue.put(None)
        except Exception as e:
            error_msg = f"ERRORE: Si è verificato un errore inaspettato: {e}\n"
            self.output_queue.put(error_msg)
            self.output_queue.put(None)

    def start_backup(self):
        """Avvia il processo di backup in un nuovo thread."""
        if self.is_running:
            return
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.output_memo.delete('1.0', tk.END)
        self.progressbar['value'] = 0
        self.status_label.config(text="Backup in corso...")
        
        thread = threading.Thread(target=self.run_rar_command)
        thread.daemon = True
        thread.start()
        self.root.after(100, self.update_gui)

# --- Esecuzione dell'applicazione ---
if __name__ == "__main__":
    root = tk.Tk()
    app = BackupApp(root)
    root.mainloop()
