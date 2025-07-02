#!/usr/bin/env python3
"""
KocurDOS - Własny system DOS w Pythonie
Wersja: 1.0.0
"""

import os
import sys
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, simpledialog
import subprocess
import threading
import requests
from pathlib import Path
import shutil
import time

class KocurDOS:
    VERSION = "1.0.0"
    GITHUB_REPO = "https://api.github.com/repos/kocurowy96/KocurDOS-py"
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"KocurDOS v{self.VERSION}")
        self.root.geometry("1000x700")
        self.root.configure(bg='#000080')
        
        # Tworzenie głównego folderu systemu
        self.disk_c = Path("KocurDOS-diskC")
        self.disk_c.mkdir(exist_ok=True)
        self.current_dir = self.disk_c
        
        # Historia komend
        self.command_history = []
        self.history_index = -1
        
        self.setup_ui()
        self.check_for_updates()
        
    def setup_ui(self):
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="System", menu=file_menu)
        file_menu.add_command(label="Terminal", command=self.show_terminal)
        file_menu.add_command(label="Edytor", command=self.show_editor)
        file_menu.add_command(label="Explorer", command=self.show_explorer)
        file_menu.add_separator()
        file_menu.add_command(label="Sprawdź aktualizacje", command=self.check_for_updates)
        file_menu.add_command(label="Wyjście", command=self.root.quit)
        
        # Notebook dla zakładek
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Domyślnie pokazuj terminal
        self.show_terminal()
        
    def show_terminal(self):
        # Sprawdź czy zakładka już istnieje
        for tab_id in self.notebook.tabs():
            if self.notebook.tab(tab_id, "text") == "Terminal":
                self.notebook.select(tab_id)
                return
                
        # Tworzenie zakładki terminala
        terminal_frame = ttk.Frame(self.notebook)
        self.notebook.add(terminal_frame, text="Terminal")
        
        # Output area
        self.terminal_output = scrolledtext.ScrolledText(
            terminal_frame, 
            bg='black', 
            fg='white', 
            font=('Courier', 10),
            state='disabled'
        )
        self.terminal_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Input frame
        input_frame = ttk.Frame(terminal_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Prompt label
        prompt_label = tk.Label(input_frame, text=f"C:\\{self.current_dir.name}>", 
                               bg='black', fg='white', font=('Courier', 10))
        prompt_label.pack(side=tk.LEFT)
        
        # Command entry
        self.command_entry = tk.Entry(input_frame, font=('Courier', 10))
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.command_entry.bind('<Return>', self.execute_command)
        self.command_entry.bind('<Up>', self.history_up)
        self.command_entry.bind('<Down>', self.history_down)
        self.command_entry.focus()
        
        # Powitanie
        self.print_to_terminal(f"KocurDOS v{self.VERSION}")
        self.print_to_terminal("Witaj w KocurDOS! Wpisz 'help' aby zobaczyć dostępne komendy.")
        self.print_to_terminal("")
        
    def show_editor(self):
        # Sprawdź czy zakładka już istnieje
        for tab_id in self.notebook.tabs():
            if self.notebook.tab(tab_id, "text") == "Edytor":
                self.notebook.select(tab_id)
                return
                
        editor_frame = ttk.Frame(self.notebook)
        self.notebook.add(editor_frame, text="Edytor")
        
        # Toolbar
        toolbar = ttk.Frame(editor_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Nowy", command=self.new_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Otwórz", command=self.open_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Zapisz", command=self.save_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Uruchom Python", command=self.run_python).pack(side=tk.LEFT, padx=2)
        
        # Text area
        self.editor_text = scrolledtext.ScrolledText(
            editor_frame, 
            font=('Courier', 10),
            wrap=tk.NONE
        )
        self.editor_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.current_file = None
        
    def show_explorer(self):
        # Sprawdź czy zakładka już istnieje
        for tab_id in self.notebook.tabs():
            if self.notebook.tab(tab_id, "text") == "Explorer":
                self.notebook.select(tab_id)
                return
                
        explorer_frame = ttk.Frame(self.notebook)
        self.notebook.add(explorer_frame, text="Explorer")
        
        # Toolbar
        toolbar = ttk.Frame(explorer_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Odśwież", command=self.refresh_explorer).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Nowy folder", command=self.create_folder).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Usuń", command=self.delete_selected).pack(side=tk.LEFT, padx=2)
        
        # Path label
        self.path_label = tk.Label(toolbar, text=str(self.current_dir))
        self.path_label.pack(side=tk.LEFT, padx=10)
        
        # File list
        self.file_tree = ttk.Treeview(explorer_frame, columns=('Size', 'Modified'), show='tree headings')
        self.file_tree.heading('#0', text='Nazwa')
        self.file_tree.heading('Size', text='Rozmiar')
        self.file_tree.heading('Modified', text='Zmodyfikowany')
        self.file_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.file_tree.bind('<Double-1>', self.on_file_double_click)
        
        self.refresh_explorer()
        
    def print_to_terminal(self, text):
        self.terminal_output.config(state='normal')
        self.terminal_output.insert(tk.END, text + '\n')
        self.terminal_output.config(state='disabled')
        self.terminal_output.see(tk.END)
        
    def execute_command(self, event):
        command = self.command_entry.get().strip()
        if not command:
            return
            
        # Dodaj do historii
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Wyświetl komendę
        self.print_to_terminal(f"C:\\{self.current_dir.name}> {command}")
        
        # Wyczyść pole
        self.command_entry.delete(0, tk.END)
        
        # Wykonaj komendę
        self.process_command(command)
        
    def process_command(self, command):
        parts = command.split()
        if not parts:
            return
            
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        if cmd == 'help':
            self.show_help()
        elif cmd == 'dir' or cmd == 'ls':
            self.list_directory()
        elif cmd == 'cd':
            self.change_directory(args)
        elif cmd == 'mkdir':
            self.make_directory(args)
        elif cmd == 'rmdir':
            self.remove_directory(args)
        elif cmd == 'del' or cmd == 'rm':
            self.delete_file(args)
        elif cmd == 'type' or cmd == 'cat':
            self.show_file_content(args)
        elif cmd == 'echo':
            self.echo_text(args)
        elif cmd == 'cls' or cmd == 'clear':
            self.clear_terminal()
        elif cmd == 'python':
            self.run_python_command(args)
        elif cmd == 'exit':
            self.root.quit()
        elif cmd == 'ver':
            self.print_to_terminal(f"KocurDOS v{self.VERSION}")
        else:
            self.print_to_terminal(f"Nieznana komenda: {cmd}")
            
    def show_help(self):
        help_text = """
Dostępne komendy:
  help          - Pokaż tę pomoc
  dir, ls       - Wyświetl zawartość katalogu
  cd <katalog>  - Zmień katalog
  mkdir <nazwa> - Utwórz katalog
  rmdir <nazwa> - Usuń katalog
  del, rm <plik>- Usuń plik
  type, cat <plik> - Wyświetl zawartość pliku
  echo <tekst>  - Wyświetl tekst
  cls, clear    - Wyczyść terminal
  python <plik> - Uruchom skrypt Python
  ver           - Pokaż wersję
  exit          - Wyjście
        """
        self.print_to_terminal(help_text)
        
    def list_directory(self):
        try:
            items = list(self.current_dir.iterdir())
            if not items:
                self.print_to_terminal("Katalog jest pusty")
                return
                
            for item in sorted(items):
                if item.is_dir():
                    self.print_to_terminal(f"<DIR>     {item.name}")
                else:
                    size = item.stat().st_size
                    self.print_to_terminal(f"{size:>8} {item.name}")
        except Exception as e:
            self.print_to_terminal(f"Błąd: {e}")
            
    def change_directory(self, args):
        if not args:
            self.print_to_terminal(str(self.current_dir))
            return
            
        target = args[0]
        if target == "..":
            if self.current_dir != self.disk_c:
                self.current_dir = self.current_dir.parent
        else:
            new_path = self.current_dir / target
            if new_path.exists() and new_path.is_dir():
                self.current_dir = new_path
            else:
                self.print_to_terminal(f"Katalog nie istnieje: {target}")
                
    def make_directory(self, args):
        if not args:
            self.print_to_terminal("Użycie: mkdir <nazwa>")
            return
            
        try:
            (self.current_dir / args[0]).mkdir()
            self.print_to_terminal(f"Utworzono katalog: {args[0]}")
        except Exception as e:
            self.print_to_terminal(f"Błąd: {e}")
            
    def remove_directory(self, args):
        if not args:
            self.print_to_terminal("Użycie: rmdir <nazwa>")
            return
            
        try:
            (self.current_dir / args[0]).rmdir()
            self.print_to_terminal(f"Usunięto katalog: {args[0]}")
        except Exception as e:
            self.print_to_terminal(f"Błąd: {e}")
            
    def delete_file(self, args):
        if not args:
            self.print_to_terminal("Użycie: del <plik>")
            return
            
        try:
            (self.current_dir / args[0]).unlink()
            self.print_to_terminal(f"Usunięto plik: {args[0]}")
        except Exception as e:
            self.print_to_terminal(f"Błąd: {e}")
            
    def show_file_content(self, args):
        if not args:
            self.print_to_terminal("Użycie: type <plik>")
            return
            
        try:
            content = (self.current_dir / args[0]).read_text(encoding='utf-8')
            self.print_to_terminal(content)
        except Exception as e:
            self.print_to_terminal(f"Błąd: {e}")
            
    def echo_text(self, args):
        self.print_to_terminal(" ".join(args))
        
    def clear_terminal(self):
        self.terminal_output.config(state='normal')
        self.terminal_output.delete(1.0, tk.END)
        self.terminal_output.config(state='disabled')
        
    def run_python_command(self, args):
        if not args:
            self.print_to_terminal("Użycie: python <plik.py>")
            return
            
        script_path = self.current_dir / args[0]
        if not script_path.exists():
            self.print_to_terminal(f"Plik nie istnieje: {args[0]}")
            return
            
        try:
            result = subprocess.run([sys.executable, str(script_path)], 
                                  capture_output=True, text=True, cwd=str(self.current_dir))
            if result.stdout:
                self.print_to_terminal(result.stdout)
            if result.stderr:
                self.print_to_terminal(f"Błąd: {result.stderr}")
        except Exception as e:
            self.print_to_terminal(f"Błąd wykonania: {e}")
            
    def history_up(self, event):
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, self.command_history[self.history_index])
            
    def history_down(self, event):
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, self.command_history[self.history_index])
        elif self.history_index >= len(self.command_history) - 1:
            self.command_entry.delete(0, tk.END)
            self.history_index = len(self.command_history)
            
    # Funkcje edytora
    def new_file(self):
        self.editor_text.delete(1.0, tk.END)
        self.current_file = None
        
    def open_file(self):
        file_path = filedialog.askopenfilename(
            initialdir=str(self.current_dir),
            filetypes=[("Wszystkie pliki", "*.*"), ("Python", "*.py"), ("Tekst", "*.txt")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.editor_text.delete(1.0, tk.END)
                self.editor_text.insert(1.0, content)
                self.current_file = file_path
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie można otworzyć pliku: {e}")
                
    def save_file(self):
        if self.current_file:
            try:
                content = self.editor_text.get(1.0, tk.END + '-1c')
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Sukces", "Plik zapisany!")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie można zapisać pliku: {e}")
        else:
            self.save_file_as()
            
    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(
            initialdir=str(self.current_dir),
            defaultextension=".txt",
            filetypes=[("Wszystkie pliki", "*.*"), ("Python", "*.py"), ("Tekst", "*.txt")]
        )
        if file_path:
            try:
                content = self.editor_text.get(1.0, tk.END + '-1c')
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.current_file = file_path
                messagebox.showinfo("Sukces", "Plik zapisany!")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie można zapisać pliku: {e}")
                
    def run_python(self):
        if not self.current_file or not self.current_file.endswith('.py'):
            messagebox.showwarning("Uwaga", "Zapisz plik jako .py przed uruchomieniem")
            return
            
        # Zapisz plik przed uruchomieniem
        self.save_file()
        
        # Uruchom w terminalu
        self.show_terminal()
        self.process_command(f"python {Path(self.current_file).name}")
        
    # Funkcje explorera
    def refresh_explorer(self):
        # Wyczyść drzewo
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
            
        # Dodaj elementy
        try:
            items = list(self.current_dir.iterdir())
            for item in sorted(items, key=lambda x: (not x.is_dir(), x.name.lower())):
                if item.is_dir():
                    self.file_tree.insert('', 'end', text=f"📁 {item.name}", 
                                        values=('<DIR>', time.ctime(item.stat().st_mtime)))
                else:
                    size = item.stat().st_size
                    self.file_tree.insert('', 'end', text=f"📄 {item.name}", 
                                        values=(f"{size} B", time.ctime(item.stat().st_mtime)))
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można odświeżyć: {e}")
            
        self.path_label.config(text=str(self.current_dir))
        
    def create_folder(self):
        name = simpledialog.askstring("Nowy folder", "Nazwa folderu:")
        if name:
            try:
                (self.current_dir / name).mkdir()
                self.refresh_explorer()
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie można utworzyć folderu: {e}")
                
    def delete_selected(self):
        selection = self.file_tree.selection()
        if not selection:
            messagebox.showwarning("Uwaga", "Wybierz element do usunięcia")
            return
            
        item = self.file_tree.item(selection[0])
        name = item['text'].replace('📁 ', '').replace('📄 ', '')
        
        if messagebox.askyesno("Potwierdzenie", f"Czy na pewno usunąć {name}?"):
            try:
                path = self.current_dir / name
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                self.refresh_explorer()
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie można usunąć: {e}")
                
    def on_file_double_click(self, event):
        selection = self.file_tree.selection()
        if not selection:
            return
            
        item = self.file_tree.item(selection[0])
        name = item['text'].replace('📁 ', '').replace('📄 ', '')
        path = self.current_dir / name
        
        if path.is_dir():
            self.current_dir = path
            self.refresh_explorer()
        else:
            # Otwórz plik w edytorze
            self.show_editor()
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.editor_text.delete(1.0, tk.END)
                self.editor_text.insert(1.0, content)
                self.current_file = str(path)
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie można otworzyć pliku: {e}")
                
    def check_for_updates(self):
        def check_updates_thread():
            try:
                # Sprawdź wersję na GitHub
                response = requests.get(f"{self.GITHUB_REPO}/releases/latest", timeout=5)
                if response.status_code == 200:
                    latest_version = response.json().get('tag_name', '').replace('v', '')
                    if latest_version and latest_version != self.VERSION:
                        if messagebox.askyesno("Aktualizacja", 
                                             f"Dostępna nowa wersja: {latest_version}\n"
                                             f"Aktualna wersja: {self.VERSION}\n\n"
                                             "Czy chcesz zaktualizować?"):
                            self.download_update(latest_version)
                    else:
                        messagebox.showinfo("Aktualizacja", "Masz najnowszą wersję!")
                else:
                    messagebox.showwarning("Aktualizacja", "Nie można sprawdzić aktualizacji")
            except Exception as e:
                messagebox.showerror("Błąd", f"Błąd sprawdzania aktualizacji: {e}")
                
        threading.Thread(target=check_updates_thread, daemon=True).start()
        
    def download_update(self, version):
        try:
            # Pobierz updater
            updater_url = f"https://github.com/kocurowy96/KocurDOS-py/releases/download/v{version}/updater.py"
            response = requests.get(updater_url)
        
            if response.status_code == 200:
                with open("updater.py", "wb") as f:
                    f.write(response.content)
                
                # Uruchom updater
                subprocess.Popen([sys.executable, "updater.py", version])
                self.root.quit()
            else:
                messagebox.showerror("Błąd", "Nie można pobrać aktualizacji")
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd pobierania aktualizacji: {e}")
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Sprawdź czy system został zaktualizowany
    if len(sys.argv) > 1 and sys.argv[1] == "--updated":
        messagebox.showinfo("Aktualizacja", "KocurDOS został pomyślnie zaktualizowany!")
        
    dos = KocurDOS()
    dos.run()
