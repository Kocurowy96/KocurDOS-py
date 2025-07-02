#!/usr/bin/env python3
"""
Skrypt do automatycznego zwiększania wersji KocurDOS
"""

import re
import json
import sys
from pathlib import Path
from datetime import datetime

def get_current_version():
    """Pobierz aktualną wersję"""
    try:
        with open("kocur_dos.py", "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'VERSION = ["\'](.+?)["\']', content)
            if match:
                return match.group(1)
    except FileNotFoundError:
        print("❌ Nie znaleziono pliku kocur_dos.py!")
        return None
    
    print("❌ Nie można odczytać wersji!")
    return None

def parse_version(version_str):
    """Parsuj wersję na komponenty"""
    try:
        parts = version_str.split('.')
        return [int(part) for part in parts]
    except ValueError:
        print(f"❌ Nieprawidłowy format wersji: {version_str}")
        return None

def bump_version(version_parts, bump_type):
    """Zwiększ wersję"""
    if bump_type == "major":
        version_parts[0] += 1
        version_parts[1] = 0
        version_parts[2] = 0
    elif bump_type == "minor":
        version_parts[1] += 1
        version_parts[2] = 0
    elif bump_type == "patch":
        version_parts[2] += 1
    else:
        print(f"❌ Nieprawidłowy typ: {bump_type}")
        return None
    
    return ".".join(map(str, version_parts))

def update_version_in_file(filename, old_version, new_version):
    """Zaktualizuj wersję w pliku"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Zamień wersję
        content = re.sub(
            rf'VERSION = ["\']({re.escape(old_version)})["\']',
            f'VERSION = "{new_version}"',
            content
        )
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"❌ Błąd aktualizacji {filename}: {e}")
        return False

def update_version_json(new_version):
    """Zaktualizuj version.json"""
    try:
        with open("version.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        data["version"] = new_version
        data["release_date"] = datetime.now().strftime("%Y-%m-%d")
        
        # Zaktualizuj URLs
        base_url = "https://github.com/kocurowy96/KocurDOS-py/releases/download"
        data["download_urls"] = {
            "all_platforms": f"{base_url}/v{new_version}/kocur_dos.py",
            "updater": f"{base_url}/v{new_version}/updater.py"
        }
        
        with open("version.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)  "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"❌ Błąd aktualizacji version.json: {e}")
        return False

def show_help():
    """Pokaż pomoc"""
    print("🔢 Bump Version - Zwiększanie wersji KocurDOS")
    print("=" * 45)
    print("")
    print("Użycie:")
    print("  python bump_version.py <typ>")
    print("")
    print("Typy:")
    print("  major  - Zwiększ główną wersję (1.0.0 -> 2.0.0)")
    print("  minor  - Zwiększ drugorzędną (1.0.0 -> 1.1.0)")
    print("  patch  - Zwiększ poprawkę (1.0.0 -> 1.0.1)")
    print("")
    print("Przykłady:")
    print("  python bump_version.py patch   # 1.0.0 -> 1.0.1")
    print("  python bump_version.py minor   # 1.0.0 -> 1.1.0")
    print("  python bump_version.py major   # 1.0.0 -> 2.0.0")

def main():
    if len(sys.argv) != 2 or sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
        return 0
    
    bump_type = sys.argv[1].lower()
    
    if bump_type not in ['major', 'minor', 'patch']:
        print(f"❌ Nieprawidłowy typ: {bump_type}")
        show_help()
        return 1
    
    print(f"🔢 Zwiększanie wersji ({bump_type})")
    print("=" * 30)
    
    # Pobierz aktualną wersję
    current_version = get_current_version()
    if not current_version:
        return 1
    
    print(f"📦 Aktualna wersja: {current_version}")
    
    # Parsuj wersję
    version_parts = parse_version(current_version)
    if not version_parts:
        return 1
    
    # Zwiększ wersję
    new_version = bump_version(version_parts, bump_type)
    if not new_version:
        return 1
    
    print(f"🆕 Nowa wersja: {new_version}")
    
    # Potwierdź
    try:
        response = input(f"\n✅ Zaktualizować wersję z {current_version} na {new_version}? (t/n): ").lower()
        if response not in ['t', 'y', 'tak', 'yes']:
            print("⚠️  Anulowano")
            return 0
    except KeyboardInterrupt:
        print("\n⚠️  Anulowano przez użytkownika")
        return 0
    
    # Aktualizuj pliki
    print("\n📝 Aktualizowanie plików...")
    
    success = True
    
    # Aktualizuj kocur_dos.py
    if update_version_in_file("kocur_dos.py", current_version, new_version):
        print("✅ kocur_dos.py zaktualizowany")
    else:
        success = False
    
    # Aktualizuj version.json
    if update_version_json(new_version):
        print("✅ version.json zaktualizowany")
    else:
        success = False
    
    if success:
        print(f"\n🎉 Wersja zaktualizowana do {new_version}!")
        print("\n📋 Następne kroki:")
        print("1. Sprawdź zmiany: git diff")
        print("2. Uruchom deploy: python deploy.py")
        print("3. Utwórz release na GitHub")
    else:
        print("\n❌ Wystąpiły błędy podczas aktualizacji")
        return 1
    
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
