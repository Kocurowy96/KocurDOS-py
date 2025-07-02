#!/usr/bin/env python3
"""
Skrypt tworzący przykładowe pliki dla KocurDOS
"""

from pathlib import Path

def create_examples():
    # Utwórz folder examples w dysku C
    examples_dir = Path("KocurDOS-diskC/examples")
    examples_dir.mkdir(parents=True, exist_ok=True)
    
    # Przykład 1: Prosty kalkulator
    calculator = """#!/usr/bin/env python3
# Prosty kalkulator dla KocurDOS

print("=== Kalkulator KocurDOS ===")

while True:
    try:
        print("\\n1. Dodawanie (+)")
        print("2. Odejmowanie (-)")
        print("3. Mnożenie (*)")
        print("4. Dzielenie (/)")
        print("5. Potęgowanie (**)")
        print("6. Wyjście")
        
        wybor = input("\\nWybierz operację (1-6): ")
        
        if wybor == '6':
            print("Do widzenia!")
            break
            
        if wybor in ['1', '2', '3', '4', '5']:
            a = float(input("Pierwsza liczba: "))
            b = float(input("Druga liczba: "))
            
            if wybor == '1':
                print(f"Wynik: {a} + {b} = {a + b}")
            elif wybor == '2':
                print(f"Wynik: {a} - {b} = {a - b}")
            elif wybor == '3':
                print(f"Wynik: {a} * {b} = {a * b}")
            elif wybor == '4':
                if b != 0:
                    print(f"Wynik: {a} / {b} = {a / b}")
                else:
                    print("Błąd: Dzielenie przez zero!")
            elif wybor == '5':
                print(f"Wynik: {a} ** {b} = {a ** b}")
        else:
            print("Nieprawidłowy wybór!")
            
    except ValueError:
        print("Błąd: Podaj prawidłową liczbę!")
    except KeyboardInterrupt:
        print("\\nProgram przerwany")
        break
"""
    
    # Przykład 2: Generator haseł
    password_gen = """#!/usr/bin/env python3
# Generator haseł dla KocurDOS

import random
import string

def generate_password(length=12, use_symbols=True):
    characters = string.ascii_letters + string.digits
    if use_symbols:
        characters += "!@#$%^&*"
    
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

print("=== Generator haseł KocurDOS ===")

while True:
    try:
        print("\\n1. Generuj hasło")
        print("2. Wyjście")
        
        choice = input("Wybierz opcję (1-2): ")
        
        if choice == '2':
            break
        elif choice == '1':
            length = int(input("Długość hasła (domyślnie 12): ") or "12")
            symbols = input("Użyć symboli? (t/n, domyślnie t): ").lower()
            use_symbols = symbols != 'n'
            
            password = generate_password(length, use_symbols)
            print(f"\\nWygenerowane hasło: {password}")
            print(f"Długość: {len(password)} znaków")
        else:
            print("Nieprawidłowy wybór!")
            
    except ValueError:
        print("Błąd: Podaj prawidłową liczbę!")
    except KeyboardInterrupt:
        print("\\nProgram przerwany")
        break
"""
    
    # Przykład 3: Lista zadań
    todo_list = """#!/usr/bin/env python3
# Lista zadań dla KocurDOS

import json
from pathlib import Path

class TodoList:
    def __init__(self):
        self.file_path = Path("todo.json")
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        if self.file_path.exists():
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_tasks(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)
    
    def add_task(self, task):
        self.tasks.append({"task": task, "done": False})
        self.save_tasks()
        print(f"Dodano zadanie: {task}")
    
    def list_tasks(self):
        if not self.tasks:
            print("Brak zadań!")
            return
        
        print("\\n=== Lista zadań ===")
        for i, task in enumerate(self.tasks, 1):
            status = "✓" if task["done"] else "○"
            print(f"{i}. {status} {task['task']}")
    
    def complete_task(self, index):
        if 1 <= index <= len(self.tasks):
            self.tasks[index-1]["done"] = True
            self.save_tasks()
            print(f"Zadanie {index} oznaczone jako wykonane!")
        else:
            print("Nieprawidłowy numer zadania!")
    
    def remove_task(self, index):
        if 1 <= index <= len(self.tasks):
            removed = self.tasks.pop(index-1)
            self.save_tasks()
            print(f"Usunięto zadanie: {removed['task']}")
        else:
            print("Nieprawidłowy numer zadania!")

def main():
    todo = TodoList()
    
    print("=== Lista zadań KocurDOS ===")
    
    while True:
        try:
            print("\\n1. Pokaż zadania")
            print("2. Dodaj zadanie")
            print("3. Oznacz jako wykonane")
            print("4. Usuń zadanie")
            print("5. Wyjście")
            
            choice = input("Wybierz opcję (1-5): ")
            
            if choice == '5':
                break
            elif choice == '1':
                todo.list_tasks()
            elif choice == '2':
                task = input("Nowe zadanie: ")
                if task.strip():
                    todo.add_task(task.strip())
            elif choice == '3':
                todo.list_tasks()
                try:
                    index = int(input("Numer zadania do oznaczenia: "))
                    todo.complete_task(index)
                except ValueError:
                    print("Podaj prawidłowy numer!")
            elif choice == '4':
                todo.list_tasks()
                try:
                    index = int(input("Numer zadania do usunięcia: "))
                    todo.remove_task(index)
                except ValueError:
                    print("Podaj prawidłowy numer!")
            else:
                print("Nieprawidłowy wybór!")
                
        except KeyboardInterrupt:
            print("\\nProgram przerwany")
            break

if __name__ == "__main__":
    main()
"""
    
    # Zapisz przykłady
    (examples_dir / "kalkulator.py").write_text(calculator, encoding='utf-8')
    (examples_dir / "generator_hasel.py").write_text(password_gen, encoding='utf-8')
    (examples_dir / "lista_zadan.py").write_text(todo_list, encoding='utf-8')
    
    # Utwórz plik README dla przykładów
    readme_content = """# Przykładowe programy KocurDOS

Ten folder zawiera przykładowe programy do uruchamiania w KocurDOS.

## Dostępne programy:

### 1. kalkulator.py
Prosty kalkulator z podstawowymi operacjami matematycznymi.
Uruchom: `python kalkulator.py`

### 2. generator_hasel.py  
Generator bezpiecznych haseł z opcjami konfiguracji.
Uruchom: `python generator_hasel.py`

### 3. lista_zadan.py
Aplikacja do zarządzania listą zadań z zapisem do pliku.
Uruchom: `python lista_zadan.py`

## Jak uruchamiać:

1. W terminalu KocurDOS wpisz: `cd examples`
2. Następnie: `python nazwa_programu.py`

Możesz też edytować te programy w edytorze KocurDOS!
"""
    
    (examples_dir / "README.txt").write_text(readme_content, encoding='utf-8')
    
    print(f"✅ Utworzono przykładowe programy w: {examples_dir}")
    print("   - kalkulator.py")
    print("   - generator_hasel.py") 
    print("   - lista_zadan.py")
    print("   - README.txt")

if __name__ == "__main__":
    create_examples()
