---
title: Setup Python - pyenv, pipx, uv i Poetry
author: Data Engineering Course
date: 2026-08-17
---

# Setup Python

Przygotowanie srodowiska do lekcji Python

```text
system -> pyenv -> Python -> pipx/uv -> Poetry -> .venv projektu
```

Cel: kazdy uczestnik ma uruchamiac ten sam projekt na tej samej wersji Pythona.

<!-- end_slide -->

# Po co setup

Bez uporzadkowanego srodowiska kazdy moze miec:

```text
inna wersje Pythona,
inne paczki,
inny interpreter,
inny folder virtualenv,
inne bledy przy uruchomieniu.
```

W Data Engineeringu to szybko psuje powtarzalnosc projektu.

<!-- end_slide -->

# Narzedzia

```text
pyenv
  wybiera wersje Pythona

pipx
  instaluje globalne narzedzia CLI w izolacji

uv
  szybkie install/run/tools dla Pythona

Poetry
  zaleznosci projektu, pyproject.toml, poetry.lock, .venv
```

Jedno narzedzie = jedna odpowiedzialnosc.

<!-- end_slide -->

# Docelowa struktura

Po setupie projekt ma miec:

```text
homework/lesson_05/
├── .python-version
├── pyproject.toml
├── poetry.lock
├── .venv/                 # lokalnie, nie commitujemy
├── python_basics.py
├── test_python_basics.py
└── orders.csv
```

Do review commitujesz kod i pliki konfiguracyjne.

Nie commitujesz `.venv/`.

<!-- end_slide -->

# Linux / WSL: system packages

Ubuntu / WSL Ubuntu:

```bash
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev curl git libffi-dev
```

Te paczki sa potrzebne, zeby `pyenv` mogl zbudowac Pythona lokalnie.

<!-- end_slide -->

# Linux / WSL: pyenv

Instalacja:

```bash
curl https://pyenv.run | bash
```

Dodaj do `~/.zshrc`:

```bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

Potem uruchom nowy shell.

<!-- end_slide -->

# Linux / WSL: Python

```bash
pyenv --version
pyenv install 3.13.0
pyenv global 3.13.0
python --version
```

Oczekiwane:

```text
Python 3.13.0
```

`pyenv global` ustawia domyslna wersje dla terminala.

<!-- end_slide -->

# pyenv local

W katalogu projektu:

```bash
cd homework/lesson_05
pyenv local 3.13.0
cat .python-version
python --version
```

`.python-version` jest informacja dla `pyenv`:

```text
w tym folderze uzyj tej wersji Pythona
```

<!-- end_slide -->

# pipx

Instalacja:

```bash
python -m pip install --user pipx
python -m pipx ensurepath
exec zsh
pipx --version
```

Do czego uzywamy `pipx`?

```text
Do instalacji narzedzi CLI, np. Poetry.
```

`pipx` izoluje narzedzia od projektow.

<!-- end_slide -->

# uv

Instalacja Linux / WSL:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
```

Przyklady uzycia:

```bash
uv tool install ruff
uvx ruff --version
uv run --with pydantic python script.py
```

`uv` jest szybkie i przydatne do jednorazowych runow.

<!-- end_slide -->

# Poetry

Rekomendacja dla tej lekcji: instaluj Poetry przez `pipx`.

```bash
pipx install poetry
poetry --version
poetry config virtualenvs.in-project true
```

Dlaczego `virtualenvs.in-project true`?

```text
.venv powstaje w katalogu projektu,
latwiej zobaczyc, ktore srodowisko nalezy do projektu,
latwiej debugowac interpreter.
```

<!-- end_slide -->

# Projekt Poetry

W katalogu homeworku:

```bash
mkdir -p homework/lesson_05
cd homework/lesson_05
pyenv local 3.13.0
poetry init --name lesson-05-python-intro --python "^3.13" --no-interaction
poetry add --group dev pytest
```

Po tym powinny powstac:

```text
.python-version
pyproject.toml
poetry.lock
.venv/
```

<!-- end_slide -->

# Uruchamianie projektu

Z katalogu `homework/lesson_05`:

```bash
poetry run python python_basics.py
poetry run pytest
```

Najwazniejsza zasada:

```text
python             moze wskazywac przypadkowy interpreter
poetry run python  uzywa interpretera z .venv tego projektu
```

<!-- end_slide -->

# macOS

Przez Homebrew:

```bash
brew install pyenv pipx uv
pipx ensurepath
pipx install poetry
poetry config virtualenvs.in-project true
pyenv install 3.13.0
pyenv global 3.13.0
```

Jesli shell nie widzi `pyenv`, sprawdz wpisy w pliku startowym shell'a.

<!-- end_slide -->

# Windows

Rekomendacja kursowa:

```text
Windows + WSL Ubuntu
```

Wtedy uzyj instrukcji Linux / WSL.

Natywnie w PowerShell:

```powershell
winget install pyenv-win.pyenv-win
python -m pip install --user pipx
python -m pipx ensurepath
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
pipx install poetry
```

<!-- end_slide -->

# Verification checklist

Po setupie sprawdz:

```bash
python --version
pyenv --version
pipx --version
uv --version
poetry --version
poetry env info
```

W katalogu projektu:

```bash
cat .python-version
ls -la .venv
poetry run python --version
poetry run pytest
```

<!-- end_slide -->

# Najczestsze problemy

```text
python ma zla wersje
  -> sprawdz pyenv local/global i .python-version

poetry nie tworzy .venv w projekcie
  -> poetry config virtualenvs.in-project true

command not found: pyenv/pipx/uv/poetry
  -> otworz nowy shell albo sprawdz PATH

pytest nie dziala
  -> poetry add --group dev pytest
```

<!-- end_slide -->

# Co commitowac

Commitujesz:

```text
.python-version
pyproject.toml
poetry.lock
python_basics.py
test_python_basics.py
orders.csv
notes.md
```

Nie commitujesz:

```text
.venv/
__pycache__/
.pytest_cache/
.coverage
```

<!-- end_slide -->

# Closing check

Powiedz na glos:

```text
pyenv wybiera wersje Pythona.
pipx instaluje globalne narzedzia CLI.
uv pomaga szybko uruchamiac i instalowac narzedzia.
Poetry zarzadza zaleznosciami projektu.
poetry run uruchamia kod w .venv projektu.
```
