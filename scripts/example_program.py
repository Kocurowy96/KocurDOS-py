#!/usr/bin/env python3
"""
Przykładowy program do testowania w KocurDOS
"""

print("=== Przykładowy program KocurDOS ===")
print("Witaj w przykładowym programie!")

# Prosty kalkulator
while True:
    try:
        print("\nKalkulator KocurDOS")
        print("1. Dodawanie")
        print("2. Odejmowanie") 
        print("3. Mnożenie")
        print("4. Dzielenie")
        print("5. Wyjście")
        
        choice = input("Wybierz opcję (1-5): ")
        
        if choice == '5':
            print("Do widzenia!")
            break
            
        if choice in ['1', '2', '3', '4']:
            a = float(input("Podaj pierwszą liczbę: "))
            b = float(input("Podaj drugą liczbę: "))
            
            if choice == '1':
                print(f"Wynik: {a} + {b} = {a + b}")
            elif choice == '2':
                print(f"Wynik: {a} - {b} = {a - b}")
            elif choice == '3':
                print(f"Wynik: {a} * {b} = {a * b}")
            elif choice == '4':
                if b != 0:
                    print(f"Wynik: {a} / {b} = {a / b}")
                else:
                    print("Błąd: Dzielenie przez zero!")
        else:
            print("Nieprawidłowa opcja!")
            
    except ValueError:
        print("Błąd: Podaj prawidłową liczbę!")
    except KeyboardInterrupt:
        print("\nProgram przerwany przez użytkownika")
        break
