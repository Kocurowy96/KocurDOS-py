#!/usr/bin/env python3
"""
Instalator KocurDOS
Sprawdza wymagania i instaluje system
"""

import sys
import subprocess
import importlib.util
import platform
from pathlib import Path

def check_python_version():
    """Sprawdź wersję Pythona"""
    if sys.version_info < (3, 8):
        print("❌ Wymagany Python 3.8 lub nowszy!")
        print(f"   Twoja wersja: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def check_module(module_name, install_name=None):
    """Sprawdź czy moduł jest zainstalowany"""
    if install_name is None:
        install_name = module_name
        
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"❌ Brak modułu: {module_name}")
        try:
            print(f"   Instaluję {install_name}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", install_name])
            print(f"✅ {module_name} zainstalowany")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Nie można zainstalować {install_name}")
            return False
    else:
        print(f"✅ {module_name} - OK")
        return True

def create_desktop_shortcut():
    """Utwórz skrót na pulpicie (Windows)"""
    if platform.system() == "Windows":
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            path = Path(desktop) / "KocurDOS.lnk"
            target = Path.cwd() / "kocur_dos.py"
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(str(path))
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{target}"'
            shortcut.WorkingDirectory = str(Path.cwd())
            shortcut.IconLocation = sys.executable
            shortcut.save()
            
            print(f"✅ Skrót utworzony: {path}")
        except ImportError:
            print("ℹ️  Aby utworzyć skrót na pulpicie, zainstaluj: pip install winshell pywin32")
        except Exception as e:
            print(f"⚠️  Nie można utworzyć skrótu: {e}")

def create_launch_script():
    """Utwórz skrypt uruchamiający"""
    system = platform.system()
    
    if system == "Windows":
        script_name = "uruchom_kocurdos.bat"
        script_content = f"""@echo off
cd /d "{Path.cwd()}"
"{sys.executable}" kocur_dos.py
pause
"""
    else:  # Linux/macOS
        script_name = "uruchom_kocurdos.sh"
        script_content = f"""#!/bin/bash
cd "{Path.cwd()}"
"{sys.executable}" kocur_dos.py
"""
    
    with open(script_name, 'w') as f:
        f.write(script_content)
    
    if system != "Windows":
        import stat
        Path(script_name).chmod(stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
    
    print(f"✅ Skrypt uruchamiający: {script_name}")

def main():
    print("🚀 Instalator KocurDOS")
    print("=" * 50)
    
    # Sprawdź wymagania
    print("\n📋 Sprawdzanie wymagań...")
    
    if not check_python_version():
        return False
    
    # Sprawdź moduły
    modules_ok = True
    modules_ok &= check_module("tkinter")
    modules_ok &= check_module("requests")
    
    if not modules_ok:
        print("\n❌ Nie wszystkie wymagania są spełnione!")
        return False
    
    # Sprawdź czy główny plik istnieje
    if not Path("kocur_dos.py").exists():
        print("\n❌ Nie znaleziono pliku kocur_dos.py!")
        print("   Upewnij się, że jesteś w katalogu z plikami KocurDOS")
        return False
    
    print("\n🔧 Konfiguracja...")
    
    # Utwórz folder dysku C
    disk_c = Path("KocurDOS-diskC")
    disk_c.mkdir(exist_ok=True)
    print(f"✅ Dysk C utworzony: {disk_c}")
    
    # Skopiuj przykładowe pliki
    examples_dir = disk_c / "examples"
    examples_dir.mkdir(exist_ok=True)
    
    if Path("example_program.py").exists():
        import shutil
        shutil.copy2("example_program.py", examples_dir / "kalkulator.py")
        if Path("system_info.py").exists():
            shutil.copy2("system_info.py", examples_dir / "system_info.py")
        print("✅ Przykładowe programy skopiowane")
    
    # Utwórz skrypty uruchamiające
    create_launch_script()
    
    # Skrót na pulpicie (Windows)
    if platform.system() == "Windows":
        create_desktop_shortcut()
    
    print("\n🎉 Instalacja zakończona pomyślnie!")
    print("\n📖 Jak uruchomić KocurDOS:")
    print(f"   • Bezpośrednio: python kocur_dos.py")
    
    if platform.system() == "Windows":
        print(f"   • Skrypt: uruchom_kocurdos.bat")
        print(f"   • Skrót na pulpicie (jeśli utworzony)")
    else:
        print(f"   • Skrypt: ./uruchom_kocurdos.sh")
    
    print(f"\n💾 Dysk C: {disk_c.absolute()}")
    print(f"📁 Przykłady: {examples_dir.absolute()}")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Instalacja przerwana przez użytkownika")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Błąd instalacji: {e}")
        sys.exit(1)
