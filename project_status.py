#!/usr/bin/env python3
"""
Skrypt do sprawdzania statusu projektu KocurDOS
"""

import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime
import requests

def run_command(command, capture_output=True):
    """Uruchom komendę i zwróć wynik"""
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
    except subprocess.CalledProcessError:
        return None

def check_files():
    """Sprawdź obecność wymaganych plików"""
    required_files = [
        "kocur_dos.py",
        "updater.py",
        "install.py",
        "version.json",
        "README.md"
    ]
    
    optional_files = [
        "example_program.py",
        "system_info.py",
        "create_examples.py",
        "deploy.py",
        "bump_version.py"
    ]
    
    print("📁 Status plików:")
    print("-" * 20)
    
    all_present = True
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} (wymagany)")
            all_present = False
    
    for file in optional_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"⚪ {file} (opcjonalny)")
    
    return all_present

def get_version_info():
    """Pobierz informacje o wersji"""
    try:
        with open("kocur_dos.py", "r", encoding="utf-8") as f:
            content = f.read()
            import re
            match = re.search(r'VERSION = ["\'](.+?)["\']', content)
            if match:
                return match.group(1)
    except:
        pass
    return None

def check_git_status():
    """Sprawdź status git"""
    print("\n🔄 Status Git:")
    print("-" * 15)
    
    if not Path(".git").exists():
        print("❌ Nie jest to repozytorium git")
        return False
    
    # Sprawdź branch
    branch = run_command("git branch --show-current")
    if branch:
        print(f"🌿 Branch: {branch}")
    
    # Sprawdź remote
    remote = run_command("git remote get-url origin")
    if remote:
        print(f"🔗 Remote: {remote}")
    
    # Sprawdź status
    status = run_command("git status --porcelain")
    if status:
        print(f"📝 Niezcommitowane zmiany: {len(status.splitlines())}")
        for line in status.splitlines()[:5]:  # Pokaż pierwsze 5
            print(f"   {line}")
        if len(status.splitlines()) > 5:
            print(f"   ... i {len(status.splitlines()) - 5} więcej")
    else:
        print("✅ Brak zmian do commitowania")
    
    # Sprawdź czy jest ahead/behind
    try:
        ahead_behind = run_command("git rev-list --left-right --count origin/main...HEAD")
        if ahead_behind:
            behind, ahead = ahead_behind.split('\t')
            if int(ahead) > 0:
                print(f"⬆️  Ahead: {ahead} commitów")
            if int(behind) > 0:
                print(f"⬇️  Behind: {behind} commitów")
    except:
        pass
    
    return True

def check_github_releases():
    """Sprawdź releases na GitHub"""
    print("\n🏷️  GitHub Releases:")
    print("-" * 20)
    
    try:
        response = requests.get(
            "https://api.github.com/repos/kocurowy96/KocurDOS-py/releases",
            timeout=5
        )
        
        if response.status_code == 200:
            releases = response.json()
            if releases:
                print(f"📦 Ostatni release: {releases[0]['tag_name']}")
                print(f"📅 Data: {releases[0]['published_at'][:10]}")
                print(f"📊 Łącznie releases: {len(releases)}")
                
                # Sprawdź czy aktualna wersja ma release
                current_version = get_version_info()
                if current_version:
                    has_release = any(r['tag_name'] == f"v{current_version}" for r in releases)
                    if has_release:
                        print(f"✅ Wersja {current_version} ma release")
                    else:
                        print(f"⚠️  Wersja {current_version} nie ma release")
            else:
                print("📦 Brak releases")
        else:
            print(f"❌ Błąd API GitHub: {response.status_code}")
    
    except requests.RequestException:
        print("❌ Nie można połączyć z GitHub API")

def check_version_consistency():
    """Sprawdź spójność wersji w plikach"""
    print("\n🔢 Spójność wersji:")
    print("-" * 18)
    
    # Wersja z kocur_dos.py
    main_version = get_version_info()
    if main_version:
        print(f"📄 kocur_dos.py: {main_version}")
    else:
        print("❌ Nie można odczytać wersji z kocur_dos.py")
        return False
    
    # Wersja z version.json
    try:
        with open("version.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            json_version = data.get("version")
            if json_version:
                print(f"📄 version.json: {json_version}")
                if json_version == main_version:
                    print("✅ Wersje są spójne")
                else:
                    print("⚠️  Wersje są różne!")
            else:
                print("❌ Brak wersji w version.json")
    except:
        print("❌ Nie można odczytać version.json")
    
    return True

def show_summary():
    """Pokaż podsumowanie"""
    print("\n" + "="*50)
    print("📊 PODSUMOWANIE")
    print("="*50)
    
    version = get_version_info()
    if version:
        print(f"🏷️  Aktualna wersja: {version}")
    
    print(f"📅 Data sprawdzenia: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n💡 Przydatne komendy:")
    print("   python bump_version.py patch  # Zwiększ wersję")
    print("   python deploy.py              # Deploy do GitHub")
    print("   python install.py             # Test instalacji")
    print("   python kocur_dos.py           # Uruchom system")

def main():
    print("📊 KocurDOS Project Status")
    print("=" * 30)
    
    # Sprawdź pliki
    files_ok = check_files()
    
    # Sprawdź git
    git_ok = check_git_status()
    
    # Sprawdź spójność wersji
    version_ok = check_version_consistency()
    
    # Sprawdź GitHub releases
    check_github_releases()
    
    # Podsumowanie
    show_summary()
    
    # Status końcowy
    if files_ok and git_ok and version_ok:
        print("\n🎉 Projekt w dobrej kondycji!")
        return 0
    else:
        print("\n⚠️  Znaleziono problemy do rozwiązania")
        return 1

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
