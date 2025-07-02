#!/usr/bin/env python3
"""
Informacje o systemie KocurDOS
"""

import os
import sys
import platform
from pathlib import Path

print("=== Informacje o systemie KocurDOS ===")
print(f"Wersja KocurDOS: 1.0.0")
print(f"Python: {sys.version}")
print(f"System operacyjny: {platform.system()} {platform.release()}")
print(f"Architektura: {platform.machine()}")
print(f"Procesor: {platform.processor()}")

# Informacje o dysku C
disk_c = Path("KocurDOS-diskC")
if disk_c.exists():
    files = list(disk_c.rglob("*"))
    total_files = len([f for f in files if f.is_file()])
    total_dirs = len([f for f in files if f.is_dir()])
    
    print(f"\nDysk C: (KocurDOS-diskC)")
    print(f"Pliki: {total_files}")
    print(f"Katalogi: {total_dirs}")
    
    # Rozmiar dysku
    total_size = sum(f.stat().st_size for f in files if f.is_file())
    print(f"Zajęte miejsce: {total_size} bajtów ({total_size/1024:.2f} KB)")

print(f"\nBieżący katalog: {os.getcwd()}")
print(f"Ścieżka Python: {sys.executable}")
