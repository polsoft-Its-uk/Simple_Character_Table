# 🗺️ Simple Character Table (Tablica Znaków)

![Screenshot aplikacji](screenshot.png)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey.svg)]()

Lekka, nowoczesna i wielojęzyczna alternatywa dla systemowego programu **charmap.exe** (Tablica Znaków) w systemie Windows. Aplikacja została napisana w czystym Pythonie z wykorzystaniem wbudowanej biblioteki graficznej **Tkinter**, dzięki czemu uruchomisz ją na każdym systemie operacyjnym bez konieczności instalowania zewnętrznych zależności.

---

## ✨ Główne funkcje

* 🌍 **Pełne wsparcie dla dwóch języków:** Błyskawiczne przełączanie interfejsu pomiędzy językiem polskim (**PL**) a angielskim (**EN**).
* 📂 **Podział na kategorie:** Łatwy dostęp do podstawowych znaków łacińskich, alfabetu IPA, greki, cyrylicy, symboli matematycznych, strzałek, a nawet podstawowych emotikon (Emoji).
* 🔍 **Wyszukiwarka na żywo:** Filtruj znaki po ich nazwach Unicode, kodach szesnastkowych (np. `U+00C0`) lub dziesiętnych.
* ⭐ **System ulubionych:** Kliknij prawym przyciskiem myszy na dowolny znak, aby dodać go do listy ulubionych. Twoje ulubione znaki zostaną zapisane w pliku `ulubione.txt` i będą dostępne po ponownym uruchomieniu aplikacji.
* 📋 **Szybkie kopiowanie:** Jednym kliknięciem skopiujesz sam znak lub jego sekwencję ucieczki (escape sequence) przygotowaną pod Pythona (`\uXXXX`).

---

## 🚀 Jak uruchomić?

Aplikacja nie wymaga instalacji żadnych dodatkowych pakietów (takich jak `pip`). Jedyne, czego potrzebujesz, to zainstalowany **Python 3**.

### Krok 1: Pobierz repozytorium
Sklonuj repozytorium na swój dysk:
```bash
git clone [https://github.com/polsoft-its-uk/simple-character-table.git](https://github.com/polsoft-its-uk/simple-character-table.git)
cd simple-character-table
Krok 2: Uruchom aplikację
W zależności od posiadanego systemu operacyjnego wpisz w terminalu:

Windows:

DOS
python tablica_znakow.py
Linux / macOS:

Bash
python3 tablica_znakow.py
🛠️ Technologie
Projekt opiera się wyłącznie na bibliotece standardowej Pythona, co gwarantuje pełne bezpieczeństwo oraz brak problemów z kompatybilnością:

Python 3

Tkinter (interfejs graficzny)

Unicodedata (baza danych o znakach Unicode)

📂 Struktura projektu
tablica_znakow.py – główny kod źródłowy aplikacji.

screenshot.png – zrzut ekranu prezentujący interfejs aplikacji.

ulubione.txt – plik generowany automatycznie przy dodaniu znaków do ulubionych.

README.md – dokumentacja projektu.

📝 Licencja
Projekt jest udostępniany na licencji MIT. Szczegóły znajdziesz w pliku LICENSE.

👥 Autor
Autor: Sebastian Januchowski

Kontakt: polsoft.its@mail.com

GitHub: polsoft-its-uk