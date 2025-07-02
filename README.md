# 🚀 KocurDOS

Własny system DOS napisany w Pythonie z terminalem, edytorem tekstu, explorerem plików i systemem aktualizacji!

## ✨ Funkcje

- 🖥️ **Terminal DOS** - pełny terminal z komendami DOS
- ✏️ **Edytor tekstu** - tworzenie i edycja plików z obsługą Python
- 📁 **Explorer plików** - graficzny interfejs do zarządzania plikami
- 🔄 **System aktualizacji** - automatyczne aktualizacje z GitHub
- 🐍 **Obsługa Python** - uruchamianie skryptów bezpośrednio w systemie
- 🌍 **Wieloplatformowość** - działa na Windows, Linux i macOS

## 📋 Wymagania

- Python 3.8 lub nowszy
- tkinter (zwykle wbudowany w Python)
- requests (`pip install requests`)

## 🔧 Instalacja

### Automatyczna instalacja:
\`\`\`bash
python install.py
\`\`\`

### Ręczna instalacja:
\`\`\`bash
# Zainstaluj wymagane biblioteki
pip install requests

# Uruchom system
python kocur_dos.py
\`\`\`

## 🎮 Jak używać

### Terminal DOS
Dostępne komendy:
- `help` - pokaż pomoc
- `dir`, `ls` - wyświetl zawartość katalogu
- `cd <katalog>` - zmień katalog
- `mkdir <nazwa>` - utwórz katalog
- `rmdir <nazwa>` - usuń katalog
- `del`, `rm <plik>` - usuń plik
- `type`, `cat <plik>` - wyświetl zawartość pliku
- `echo <tekst>` - wyświetl tekst
- `cls`, `clear` - wyczyść terminal
- `python <plik>` - uruchom skrypt Python
- `ver` - pokaż wersję
- `exit` - wyjście

### Edytor tekstu
- Tworzenie, otwieranie i zapisywanie plików
- Uruchamianie skryptów Python
- Podświetlanie składni

### Explorer plików
- Przeglądanie plików i folderów
- Tworzenie nowych folderów
- Usuwanie plików i folderów
- Otwieranie plików w edytorze

## 📁 Struktura

\`\`\`
KocurDOS/
├── kocur_dos.py          # Główny system
├── updater.py            # Program aktualizujący
├── install.py            # Instalator
├── example_program.py    # Przykładowy program
├── system_info.py        # Informacje o systemie
├── version.json          # Informacje o wersji
├── KocurDOS-diskC/       # Główny dysk systemu
│   └── examples/         # Przykładowe programy
└── README.md            # Ten plik
\`\`\`

## 🔄 System aktualizacji

KocurDOS automatycznie sprawdza aktualizacje z GitHub. Gdy dostępna jest nowa wersja:
1. System pobiera updater
2. Updater tworzy kopię zapasową (`kocur_dos-old.py`)
3. Pobiera nową wersję
4. Uruchamia zaktualizowany system

## 🛠️ Rozwój

Aby dodać nowe funkcje:
1. Edytuj `kocur_dos.py`
2. Dodaj nowe komendy w metodzie `process_command()`
3. Zaktualizuj wersję w `VERSION`
4. Zaktualizuj `version.json`

## 📝 Licencja

Ten projekt jest dostępny na licencji MIT.

## 🤝 Współpraca

Zgłaszaj błędy i sugestie przez GitHub Issues!

---

**KocurDOS** - Twój własny system DOS w Pythonie! 🐱‍💻
