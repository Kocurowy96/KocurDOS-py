#!/usr/bin/env python3
"""
Skrypt do automatycznego deploymentu KocurDOS
Uniwersalny skrypt Python działający na wszystkich platformach
"""

import subprocess
import sys
import re
from pathlib import Path
import webbrowser

def run_command(command, capture_output=True):
    """Uruchom komendę shell i zwróć wynik"""
    try:
        if isinstance(command, str):
            command = command.split()
        
        result = subprocess.run(
            command, 
            capture_output=capture_output, 
            text=True, 
            check=True
        )
        return result.stdout.strip() if capture_output else ""
    except subprocess.CalledProcessError as e:
        if capture_output:
            print(f"❌ Błąd komendy: {' '.join(command)}")
            print(f"   {e.stderr}")
        return None

def check_git_repo():
    """Sprawdź czy jesteśmy w repozytorium git"""
    if not Path(".git").exists():
        print("❌ Nie jesteś w repozytorium git!")
        print("   Uruchom ten skrypt w folderze z KocurDOS")
        return False
    return True

def get_current_version():
    """Pobierz aktualną wersję z kocur_dos.py"""
    try:
        with open("kocur_dos.py", "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'VERSION = ["\'](.+?)["\']', content)
            if match:
                return match.group(1)
    except FileNotFoundError:
        print("❌ Nie znaleziono pliku kocur_dos.py!")
        return None
    
    print("❌ Nie można odczytać wersji z kocur_dos.py!")
    return None

def check_git_status():
    """Sprawdź czy są zmiany do commitowania"""
    status = run_command("git status --porcelain")
    return status is not None and len(status) > 0

def get_git_remote():
    """Pobierz URL zdalnego repo"""
    remote = run_command("git remote get-url origin")
    return remote

def commit_changes(version):
    """Commituj zmiany"""
    print("📝 Commitowanie zmian...")
    
    # Dodaj wszystkie pliki
    if run_command("git add .") is None:
        return False
    
    # Commit
    commit_msg = f"🔄 Aktualizacja do wersji {version}"
    if run_command(f'git commit -m "{commit_msg}"') is None:
        return False
    
    print(f"✅ Zcommitowano: {commit_msg}")
    return True

def push_to_github():
    """Wypchnij zmiany do GitHub"""
    print("⬆️  Wysyłanie do GitHub...")
    
    if run_command("git push origin main") is None:
        # Spróbuj master jeśli main nie działa
        if run_command("git push origin master") is None:
            print("❌ Nie można wypchnąć zmian!")
            return False
    
    print("✅ Zmiany wysłane do GitHub!")
    return True

def show_release_info(version, repo_url):
    """Pokaż informacje o tworzeniu release"""
    print("\n" + "="*50)
    print("🎉 Deploy zakończony pomyślnie!")
    print("="*50)
    
    print(f"\n📦 Wersja: {version}")
    print(f"🔗 Repo: {repo_url}")
    
    # Przygotuj URL do tworzenia release
    if "github.com" in repo_url:
        # Wyciągnij właściciela i nazwę repo z URL
        if repo_url.endswith(".git"):
            repo_url = repo_url[:-4]
        
        parts = repo_url.replace("https://github.com/", "").replace("git@github.com:", "")
        release_url = f"https://github.com/{parts}/releases/new?tag=v{version}&title=KocurDOS%20v{version}"
        
        print(f"\n🏷️  Utwórz release:")
        print(f"   {release_url}")
        
        # Zapytaj czy otworzyć w przeglądarce
        try:
            response = input("\n🌐 Otworzyć GitHub w przeglądarce? (t/n): ").lower()
            if response in ['t', 'y', 'tak', 'yes']:
                webbrowser.open(release_url)
                print("🚀 Otwarto GitHub w przeglądarce!")
        except KeyboardInterrupt:
            print("\n⚠️  Przerwano przez użytkownika")
    
    print(f"\n📋 Pliki do załączenia do release:")
    files_to_attach = [
        "kocur_dos.py",
        "updater.py", 
        "install.py",
        "example_program.py",
        "system_info.py",
        "create_examples.py"
    ]
    
    for file in files_to_attach:
        if Path(file).exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (brak pliku)")
    
    print(f"\n📝 Sugerowany opis release:")
    print(f"```")
    print(f"## 🐱‍💻 KocurDOS v{version}")
    print(f"")
    print(f"### ✨ Zmiany w tej wersji:")
    print(f"- [Opisz zmiany tutaj]")
    print(f"")
    print(f"### 📦 Instalacja:")
    print(f"1. Pobierz wszystkie pliki")
    print(f"2. Uruchom: `python install.py`")
    print(f"3. Uruchom system: `python kocur_dos.py`")
    print(f"")
    print(f"### 📋 Wymagania:")
    print(f"- Python 3.8+")
    print(f"- tkinter")
    print(f"- requests")
    print(f"```")

def main():
    print("🚀 KocurDOS Deploy Script")
    print("=" * 30)
    
    # Sprawdź czy jesteśmy w repo git
    if not check_git_repo():
        return 1
    
    # Pobierz aktualną wersję
    version = get_current_version()
    if not version:
        return 1
    
    print(f"📦 Aktualna wersja: {version}")
    
    # Pobierz URL repo
    repo_url = get_git_remote()
    if repo_url:
        print(f"🔗 Repo: {repo_url}")
    
    # Sprawdź czy są zmiany
    has_changes = check_git_status()
    
    if has_changes:
        print("📝 Znaleziono niezcommitowane zmiany")
        
        try:
            response = input("💾 Commitować zmiany? (t/n): ").lower()
            if response not in ['t', 'y', 'tak', 'yes']:
                print("⚠️  Deploy przerwany przez użytkownika")
                return 0
        except KeyboardInterrupt:
            print("\n⚠️  Deploy przerwany przez użytkownika")
            return 0
        
        if not commit_changes(version):
            return 1
    else:
        print("✅ Brak zmian do commitowania")
    
    # Push do GitHub
    if not push_to_github():
        return 1
    
    # Pokaż informacje o release
    show_release_info(version, repo_url or "")
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Deploy przerwany przez użytkownika")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Nieoczekiwany błąd: {e}")
        sys.exit(1)
