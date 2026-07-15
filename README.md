# 🗺️ Simple Character Table

![App Screenshot](screenshot.png)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey.svg)]()

A lightweight, modern, and multilingual alternative to the Windows system utility **charmap.exe** (Character Map). Built with pure Python using the built-in **Tkinter** GUI library, it runs seamlessly on any operating system without requiring any external dependencies.

---

## ✨ Features

* 🌍 **Full Dual-Language Support:** Instant interface switching between English (**EN**) and Polish (**PL**).
* 📂 **Categorized Layout:** Quick access to Basic Latin, IPA phonetic symbols, Greek, Cyrillic, Mathematical symbols, Arrows, and basic Emojis.
* 🔍 **Live Search:** Filter characters dynamically by their Unicode name, hex code (e.g., `U+00C0`), or decimal value.
* ⭐ **Favorites System:** Right-click any character to add it to your favorites list. Your favorites are saved to `ulubione.txt` and persist across application restarts.
* 📋 **Quick Copy:** Copy either the character itself or its Python-ready escape sequence (`\uXXXX`) with a single click.

---

## 🚀 Getting Started

The application does not require any external packages (no `pip` installs needed). All you need is **Python 3** installed on your system.

### Step 1: Clone the Repository
Clone the repository to your local machine:
```bash
git clone [https://github.com/polsoft-its-uk/simple-character-table.git](https://github.com/polsoft-its-uk/simple-character-table.git)
cd simple-character-table
Step 2: Run the Application
Depending on your operating system, run the following command in your terminal:

Windows:

DOS
python tablica_znakow.py
Linux / macOS:

Bash
python3 tablica_znakow.py
🛠️ Built With
This project relies exclusively on the Python Standard Library, ensuring maximum compatibility and security:

Python 3

Tkinter (Graphical User Interface)

Unicodedata (Unicode character database lookup)

📂 Project Structure
tablica_znakow.py – Main application source code.

screenshot.png – Interface preview image.

ulubione.txt – Automatically generated file storing your favorite character codes.

README.md – Project documentation.

📝 License
This project is licensed under the MIT License. See the LICENSE file for details.

👥 Author
Author: Sebastian Januchowski

Email: polsoft.its@mail.com

GitHub: polsoft-its-uk