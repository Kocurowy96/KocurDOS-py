#!/usr/bin/env python3
"""
Automatyczny deploy z tworzeniem release na GitHub
Używa pliku .env do przechowywania tokenów
"""

import subprocess
import sys
import re
import json
import requests
from pathlib import Path
import webbrowser
import os

def load_env_file():
    """Załaduj zmienne z pliku .env"""
    env_file = Path(".env")
    if not env_file.exists():
        return {}
    
    env_vars = {}
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Usuń cudzysłowy jeśli są
                    value = value.strip('"\'')
                    env_vars[key.strip()] = value
    except Exception as e:
        print(f"⚠️  Błąd czytania .env: {e}")
    
    return env_vars

def create_env_template():
    """Utwórz przykładowy plik .env"""
    env_template = """# GitHub Personal Access Token
# Utwórz na: https://github.com/settings/tokens
# Uprawnienia: repo (pełny dostęp do repozytoriów)
GITHUB_TOKEN=ghp_your_token_here

# Opcjonalne: GitHub username (domyślnie z repo URL)
GITHUB_USERNAME=kocurowy96

# Opcjonalne: Nazwa repo (domyślnie z repo URL)
GITHUB_REPO=KocurDOS-py
"""
    
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_template)
    
    print("📝 Utworzono plik .env z szablonem")
    print("   Edytuj plik .env i wstaw swój GitHub token")

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

def get_github_config():
    """Pobierz konfigurację GitHub z .env lub zmiennych środowiskowych"""
    # Załaduj .env
    env_vars = load_env_file()
    
    # GitHub token
    token = env_vars.get('GITHUB_TOKEN') or os.getenv('GITHUB_TOKEN')
    if not token:
        print("❌ Brak GITHUB_TOKEN!")
        print("   Opcje:")
        print("   1. Dodaj do .env: GITHUB_TOKEN=twoj_token")
        print("   2. Ustaw zmienną: export GITHUB_TOKEN=twoj_token")
        print("   3. Utwórz token na: https://github.com/settings/tokens")
        return None, None, None
    
    # Username i repo (z .env lub z git remote)
    username = env_vars.get('GITHUB_USERNAME', 'kocurowy96')
    repo = env_vars.get('GITHUB_REPO', 'KocurDOS-py')
    
    # Spróbuj pobrać z git remote jeśli nie ma w .env
    if not env_vars.get('GITHUB_USERNAME') or not env_vars.get('GITHUB_REPO'):
        remote_url = run_command("git remote get-url origin")
        if remote_url and 'github.com' in remote_url:
            # Parsuj URL: https://github.com/user/repo.git
            parts = remote_url.replace('https://github.com/', '').replace('.git', '').split('/')
            if len(parts) >= 2:
                username = parts[0]
                repo = parts[1]
    
    return token, username, repo

def create_github_release(version, token, username, repo):
    """Utwórz release na GitHub przez API"""
    try:
        url = f"https://api.github.com/repos/{username}/{repo}/releases"
        
        release_data = {
            "tag_name": f"v{version}",
            "target_commitish": "main",
            "name": f"🎉 KocurDOS v{version}",
            "body": f"""## 🐱‍💻 KocurDOS v{version}

### ✨ Zmiany w tej wersji:
- Pierwsza stabilna wersja KocurDOS
- Terminal z komendami DOS
- Edytor tekstu z obsługą Python
- Explorer plików z GUI
- System automatycznych aktualizacji
- Wieloplatformowość (Windows, Linux, macOS)

### 📦 Instalacja:
1. Pobierz wszystkie pliki
2. Uruchom: `python install.py`
3. Uruchom system: `python kocur_dos.py`

### 📋 Wymagania:
- Python 3.8+
- tkinter
- requests

### 🎮 Jak używać:
- `help` - pokaż dostępne komendy
- `dir` - lista plików
- `cd examples` - przejdź do przykładów
- `python kalkulator.py` - uruchom program

---
**KocurDOS** - Twój własny system DOS w Pythonie! 🚀""",
            "draft": False,
            "prerelease": False
        }
        
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        response = requests.post(url, json=release_data, headers=headers)
        
        if response.status_code == 201:
            release_info = response.json()
            print(f"✅ Release v{version} utworzony!")
            print(f"🔗 URL: {release_info['html_url']}")
            return release_info
        else:
            print(f"❌ Błąd tworzenia release: {response.status_code}")
            print(f"   {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Błąd API GitHub: {e}")
        return None

def upload_release_assets(release_info, token):
    """Upload plików do release"""
    files_to_upload = [
        "kocur_dos.py",
        "updater.py", 
        "install.py",
        "example_program.py",
        "system_info.py",
        "create_examples.py"
    ]
    
    upload_url = release_info['upload_url'].replace('{?name,label}', '')
    
    headers = {
        "Authorization": f"token {token}",
    }
    
    uploaded_count = 0
    for filename in files_to_upload:
        if Path(filename).exists():
            try:
                print(f"📤 Uploading {filename}...")
                
                with open(filename, 'rb') as f:
                    response = requests.post(
                        upload_url,
                        headers=headers,
                        params={'name': filename},
                        files={'file': (filename, f, 'application/octet-stream')}
                    )
                    
                if response.status_code == 201:
                    print(f"✅ {filename} uploaded")
                    uploaded_count += 1
                else:
                    print(f"⚠️  Błąd uploading {filename}: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Błąd uploading {filename}: {e}")
        else:
            print(f"⚠️  Plik {filename} nie istnieje")
    
    print(f"\n📦 Uploaded {uploaded_count}/{len(files_to_upload)} plików")

def main():
    print("🚀 Auto Deploy KocurDOS")
    print("=" * 30)
    
    # Sprawdź czy jesteśmy w repo git
    if not Path(".git").exists():
        print("❌ Nie jesteś w repozytorium git!")
        return 1
    
    # Sprawdź czy istnieje .env
    if not Path(".env").exists():
        print("📝 Brak pliku .env - tworzę szablon...")
        create_env_template()
        print("\n⚠️  Edytuj plik .env i dodaj swój GitHub token, potem uruchom ponownie")
        return 0
    
    # Pobierz aktualną wersję
    version = get_current_version()
    if not version:
        return 1
    
    print(f"📦 Wersja: {version}")
    
    # Pobierz konfigurację GitHub
    token, username, repo = get_github_config()
    if not token:
        return 1
    
    print(f"🔗 Repo: {username}/{repo}")
    
    # Commit i push
    print("\n📝 Commitowanie i push...")
    
    if run_command("git add .") is None:
        return 1
    
    commit_msg = f"Release v{version}"
    # Użyj listy zamiast stringa dla bezpieczeństwa
    if run_command(['git', 'commit', '-m', commit_msg]) is None:
        print("ℹ️  Brak zmian do commitowania")
    
    if run_command("git push origin main") is None:
        return 1
    
    print("✅ Kod wypchnięty na GitHub!")
    
    # Utwórz release
    print(f"\n🏷️  Tworzenie release v{version}...")
    release_info = create_github_release(version, token, username, repo)
    
    if release_info:
        # Upload plików
        print("\n📤 Upload plików...")
        upload_release_assets(release_info, token)
        
        print(f"\n🎉 Release v{version} gotowy!")
        print(f"🔗 {release_info['html_url']}")
        
        # Otwórz w przeglądarce
        try:
            response = input("\n🌐 Otworzyć release w przeglądarce? (t/n): ").lower()
            if response in ['t', 'y', 'tak', 'yes']:
                webbrowser.open(release_info['html_url'])
        except KeyboardInterrupt:
            pass
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Przerwano przez użytkownika")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Nieoczekiwany błąd: {e}")
        sys.exit(1)
