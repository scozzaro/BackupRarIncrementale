import tkinter as tk
from tkinter import scrolledtext, filedialog
import subprocess
import threading
import queue
import os
import sys
import json

# --- Classe per l'applicazione GUI ---
class BackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Backup con RAR")
        self.root.geometry("700x550")
        
        self.is_running = False
        self.output_queue = queue.Queue()
        
        # Variabili di stato dinamiche
        self.current_backup_file = "backup_config.rbak"
        
        # --- Frame principale per l'interfaccia utente ---
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Sezione per il nome del backup ---
        self.backup_name_label = tk.Label(main_frame, text=f"File di configurazione: {self.current_backup_file}", font=("Arial", 12, "bold"))
        self.backup_name_label.pack(pady=5)
        
        # --- Sezione per i pulsanti di salvataggio/caricamento ---
        save_load_frame = tk.Frame(main_frame)
        save_load_frame.pack(pady=5)
        
        save_button = tk.Button(save_load_frame, text="Salva Backup", command=self.save_backup_data)
        save_button.pack(side=tk.LEFT, padx=5)
        
        load_button = tk.Button(save_load_frame, text="Carica Backup", command=self.load_backup_data)
        load_button.pack(side=tk.LEFT, padx=5)

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
        
        # --- Altri widget di stato e output ---
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
            
    def browse_destination(self):
        """Apre una finestra di dialogo per selezionare la cartella di destinazione."""
        selected_path = filedialog.askdirectory(initialdir=self.dest_entry.get())
        if selected_path:
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, selected_path)

    def save_backup_data(self):
        """Salva la configurazione del backup in un file JSON."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".rbak",
            filetypes=[("RAR Backup", "*.rbak")],
            initialfile=self.current_backup_file
        )
        if not file_path:
            return

        data = {
            "folders": list(self.folders_listbox.get(0, tk.END)),
            "destination_folder": self.dest_entry.get(),
            "archive_name": self.archive_name_entry.get()
        }

        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            self.current_backup_file = os.path.basename(file_path)
            self.backup_name_label.config(text=f"File di configurazione: {self.current_backup_file}")
            self.status_label.config(text="Configurazione salvata con successo!")
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
            
            # Pulisce le liste e i campi di testo
            self.folders_listbox.delete(0, tk.END)
            self.dest_entry.delete(0, tk.END)
            self.archive_name_entry.delete(0, tk.END)
            
            # Popola i widget con i dati caricati
            for folder in data.get("folders", []):
                self.folders_listbox.insert(tk.END, folder)
            
            self.dest_entry.insert(0, data.get("destination_folder", os.path.join(os.path.expanduser('~'), 'Backup')))
            self.archive_name_entry.insert(0, data.get("archive_name", "IlMioBackup.rar"))

            self.current_backup_file = os.path.basename(file_path)
            self.backup_name_label.config(text=f"File di configurazione: {self.current_backup_file}")
            self.status_label.config(text="Configurazione caricata con successo!")
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
        """Legge l'output dalla coda e aggiorna la Memo."""
        try:
            while True:
                line = self.output_queue.get_nowait()
                if line is None:
                    self.on_backup_complete()
                    break
                self.output_memo.insert(tk.END, line)
                self.output_memo.see(tk.END)
        except queue.Empty:
            self.root.after(100, self.update_gui)
    
    def on_backup_complete(self):
        """Gestisce il completamento del backup."""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.status_label.config(text="Backup completato! 🎉")

    def run_rar_command(self):
        """Esegue il comando rar in un thread separato."""
        try:
            source_folders = self.folders_listbox.get(0, tk.END)
            dest_folder = self.dest_entry.get()
            archive_name = self.archive_name_entry.get()
            
            if not source_folders:
                self.output_queue.put("Nessuna cartella selezionata per il backup.\n")
                self.output_queue.put(None)
                return
            
            if not dest_folder or not archive_name:
                self.output_queue.put("Specificare un percorso e un nome per l'archivio.\n")
                self.output_queue.put(None)
                return
            
            backup_archive = os.path.join(dest_folder, archive_name)
            
            # Assicurati che la cartella di destinazione esista
            os.makedirs(dest_folder, exist_ok=True)

            command = ['rar', 'a', '-u', '-r', backup_archive]
            command.extend(source_folders)
            
            process = subprocess.Popen(command, 
                                       stdout=subprocess.PIPE, 
                                       stderr=subprocess.STDOUT,
                                       text=True,
                                       cwd=os.path.expanduser('~'))
            
            for line in process.stdout:
                self.output_queue.put(line)
            
            process.wait()
            self.output_queue.put(None)
            
        except FileNotFoundError:
            error_msg = "ERRORE: Il comando 'rar' non è stato trovato.\n"
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