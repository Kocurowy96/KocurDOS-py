#!/usr/bin/env python3
"""
KocurDOS Updater
Automatyczny updater dla KocurDOS
"""

import sys
import os
import time
import requests
import subprocess
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

class KocurDOSUpdater:
    def __init__(self, version):
        self.version = version
        self.github_repo = "https://github.com/user/kocur-dos"  # Zmień na swoje repo
        
        # Ukryj główne okno
        root = tk.Tk()
        root.withdraw()
        
        self.update()
        
    def update(self):
        try:
            # Krok 1: Wyłącz KocurDOS (już wyłączony przez wywołanie)
            messagebox.showinfo("Updater", "Rozpoczynam aktualizację...")
            
            # Krok 2: Zrób kopię poprzedniej wersji
            if Path("kocur_dos.py").exists():
                shutil.copy2("kocur_dos.py", "kocur_dos-old.py")
                print("Utworzono kopię zapasową: kocur_dos-old.py")
                
            # Krok 3: Pobierz nową wersję
            download_url = f"{self.github_repo}/releases/download/v{self.version}/kocur_dos.py"
            
            print(f"Pobieranie z: {download_url}")
            if not self.download_file(download_url, "kocur_dos.py"):
                raise Exception("Nie można pobrać aktualizacji")
            
            print("Aktualizacja pobrana pomyślnie!")
            
            # Krok 4: Uruchom nową wersję
            time.sleep(1)  # Krótka pauza
            subprocess.Popen([sys.executable, "kocur_dos.py", "--updated"])
            print("Uruchamiam nową wersję...")
            
            # Krok 5: Usuń siebie
            self.self_destruct()
            
        except Exception as e:
            messagebox.showerror("Błąd aktualizacji", f"Błąd podczas aktualizacji: {e}")
            
    def download_file(self, url, filename):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
            return False
        except:
            return False
            
    def self_destruct(self):
        # Utwórz skrypt do usunięcia siebie
        cleanup_script = """
import os
import time
import sys

time.sleep(2)
try:
    os.remove("updater.py")
except:
    pass
try:
    os.remove(sys.argv[0])
except:
    pass
"""
        
        with open("cleanup.py", "w") as f:
            f.write(cleanup_script)
            
        subprocess.Popen([sys.executable, "cleanup.py"])

    def show_progress(self, message):
        print(f"[UPDATER] {message}")
        try:
            messagebox.showinfo("Updater", message)
        except:
            pass  # W przypadku problemów z GUI

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Użycie: updater.py <wersja>")
        sys.exit(1)
        
    updater = KocurDOSUpdater(sys.argv[1])
