# Setup przed lekcja 00

<!-- end_slide -->

## Otworz i zrob to

To jest minimalny setup uczestnika. Nie konfiguruj calego swiata. Masz tylko sprawdzic, czy na lekcji, w labach i w homeworku SQL masz gdzie pracowac.

<!-- end_slide -->

## 1. Gdzie pracujemy

Na Linuxie: zwykly terminal.

Na Windowsie: WSL Ubuntu. Komendy kursu odpalasz w terminalu Ubuntu, nie w PowerShell ani CMD.

Jednorazowo na Windowsie, w PowerShell jako administrator:

```powershell
wsl --install -d Ubuntu
```

Potem otworz aplikacje Ubuntu i pracuj juz tam:

```bash
mkdir -p ~/data-engineering-mentoring
cd ~/data-engineering-mentoring
code .
```

Trzymaj katalog kursu po stronie Linux/WSL, np. `~/data-engineering-mentoring`, a nie w `/mnt/c/...`.

<!-- end_slide -->

## 2. Narzedzia lokalne

Jesli jestes na Ubuntu albo WSL Ubuntu, zainstaluj minimum:

```bash
sudo apt update
sudo apt install -y git sqlite3 python3 python3-venv
```

Sprawdz w terminalu Linux/WSL:

```bash
git --version
sqlite3 --version
python3 --version
```

Minimalny wynik:

```text
[ ] VS Code dziala
[ ] terminal Linux/WSL otwiera sie w folderze kursu
[ ] Git dziala
[ ] SQLite dziala
[ ] Python 3.11+ dziala albo wiesz, ze trzeba go poprawic
```

<!-- end_slide -->

## 3. Repo GitHub

Utworz repo do labow i pracy domowej, np. `data-engineering-mentoring`.

Minimalna struktura:

```text
data-engineering-mentoring/
├── README.md
├── homework/
│   └── lesson_01/
├── labs/
│   └── lesson_00/
└── docs/
    └── questions.md
```

Jak pracujemy:

```text
lesson_00 -> aktywny lab -> PR albo logiczny commit
lesson_01+ -> homework/lesson_XX -> PR albo logiczny commit
```

Nie chodzi o perfekcyjny Git. Chodzi o to, zeby mentor mogl zobaczyc:

- co zrobiles,
- gdzie jest rozwiazanie,
- jak sprawdziles wynik,
- jakie masz pytania.

<!-- end_slide -->

## 4. Excalidraw

Otworz Excalidraw i sprawdz:

```text
[ ] umiem stworzyc nowy diagram
[ ] umiem dodac prostokat
[ ] umiem dodac strzalke
[ ] umiem dodac tekst
[ ] umiem zapisac albo udostepnic wynik
```

Pierwszy standard diagramu w kursie:

```text
source -> transformacja -> wynik -> odbiorca
```

<!-- end_slide -->

## 5. Co wyslac mentorowi przed lekcja

```text
System: Linux / WSL Ubuntu / inny
GitHub repo: link albo "jeszcze nie"
Git dziala: tak/nie
SQLite dziala: tak/nie
Excalidraw dziala: tak/nie
3 pytania na start:
1.
2.
3.
```