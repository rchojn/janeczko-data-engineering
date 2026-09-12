# Setup: pyenv, pipx, uv i Poetry

## Po co ten setup

W projektach Python nie chcemy zgadywac, jaka wersja Pythona i jakie zaleznosci sa akurat w systemie.

Ustawiamy cztery rzeczy:

```text
pyenv  -> wybiera wersje Pythona dla projektu
pipx   -> instaluje narzedzia CLI w osobnych srodowiskach
uv     -> szybkie nowoczesne narzedzie do Pythona: install/run/tools
Poetry -> tworzy venv i zarzadza zaleznosciami projektu w tej lekcji
```

Na tej lekcji projekt robimy przez Poetry, bo chcemy zobaczyc klasyczny `pyproject.toml` + `poetry.lock` + `.venv/`.

`uv` warto miec od poczatku, bo w nowych projektach coraz czesciej zastapi czesc pracy `pip`, `pipx` albo Poetry.

## Ktorego narzedzia uzywam do czego

| Narzedzie | Do czego | Przyklad |
|---|---|---|
| `pyenv` | wersja Pythona | `pyenv local 3.13.0` |
| `pipx` | globalne narzedzia CLI | `pipx install poetry` |
| `uv` | szybkie instalowanie i uruchamianie narzedzi | `uv tool install ruff` |
| `Poetry` | zaleznosci projektu lekcji | `poetry add --group dev pytest` |

Najprostsza zasada:

```text
projekt lekcji 05 -> Poetry
narzedzia globalne -> pipx albo uv tool
wersja Pythona -> pyenv
```

## Linux / WSL Ubuntu

### 1. Zaleznosci systemowe dla pyenv

```bash
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
  libreadline-dev libsqlite3-dev curl git libncursesw5-dev xz-utils tk-dev \
  libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

### 2. pyenv

```bash
curl https://pyenv.run | bash
```

Dodaj do `~/.zshrc`:

```bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

Odpal ponownie shell:

```bash
exec zsh
pyenv --version
```

### 3. Python dla kursu

```bash
pyenv install 3.13.0
pyenv global 3.13.0
python --version
```

W projekcie:

```bash
pyenv local 3.13.0
cat .python-version
```

### 4. pipx

```bash
python -m pip install --user pipx
python -m pipx ensurepath
exec zsh
pipx --version
```

### 5. uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
exec zsh
uv --version
```

### 6. Poetry

Rekomendacja dla tej lekcji: instaluj Poetry przez `pipx`.

```bash
pipx install poetry
poetry --version
poetry config virtualenvs.in-project true
```

Alternatywa, jesli chcesz instalowac narzedzia przez `uv`:

```bash
uv tool install poetry
poetry --version
```

## macOS

### 1. Homebrew

Jesli nie masz Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. pyenv

```bash
brew update
brew install pyenv
```

Dodaj do `~/.zshrc`:

```bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

Odpal ponownie shell:

```bash
exec zsh
pyenv --version
```

### 3. Python dla kursu

```bash
pyenv install 3.13.0
pyenv global 3.13.0
python --version
```

### 4. pipx

```bash
brew install pipx
pipx ensurepath
exec zsh
pipx --version
```

### 5. uv

```bash
brew install uv
uv --version
```

Alternatywnie:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
exec zsh
uv --version
```

### 6. Poetry

```bash
pipx install poetry
poetry --version
poetry config virtualenvs.in-project true
```

Alternatywa:

```bash
uv tool install poetry
poetry --version
```

## Windows

Rekomendacja kursowa: Windows + WSL Ubuntu. Wtedy uzyj sekcji `Linux / WSL Ubuntu`.

Jesli pracujesz natywnie w Windows PowerShell, uzyj tych krokow.

### 1. pyenv-win

```powershell
winget install pyenv-win.pyenv-win
```

Zamknij i otworz PowerShell ponownie.

Sprawdz:

```powershell
pyenv --version
```

### 2. Python dla kursu

```powershell
pyenv install 3.13.0
pyenv global 3.13.0
python --version
```

W projekcie:

```powershell
pyenv local 3.13.0
Get-Content .python-version
```

### 3. pipx

```powershell
python -m pip install --user pipx
python -m pipx ensurepath
```

Zamknij i otworz PowerShell ponownie.

```powershell
pipx --version
```

### 4. uv

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Zamknij i otworz PowerShell ponownie.

```powershell
uv --version
```

Alternatywnie przez WinGet:

```powershell
winget install --id=astral-sh.uv -e
```

### 5. Poetry

```powershell
pipx install poetry
poetry --version
poetry config virtualenvs.in-project true
```

Alternatywa:

```powershell
uv tool install poetry
poetry --version
```

## Minimalny projekt lekcji 05

W katalogu homeworku:

```bash
mkdir -p homework/lesson_05
cd homework/lesson_05
pyenv local 3.13.0
poetry init --name lesson-05-python-intro --python "^3.13" --no-interaction
poetry add --group dev pytest
```

Utworz pliki:

```bash
touch python_basics.py test_python_basics.py notes.md
```

Skopiuj `orders.csv` z materialow kursu do tego katalogu. Jesli tworzysz homework wewnatrz katalogu lekcji, mozesz zrobic to z katalogu lekcji tak:

```bash
cp student/lab/data/orders.csv homework/lesson_05/orders.csv
```

Jesli pracujesz w osobnym repo uczestnika, skopiuj `orders.csv` recznie z materialow kursu.

## Uruchamianie projektu Poetry

```bash
poetry run python python_basics.py
poetry run pytest
```

Sprawdzenie srodowiska:

```bash
python --version
poetry run python --version
poetry env info --path
```

## Gdzie wchodzi uv

W tej lekcji nie musisz przepisywac projektu z Poetry na `uv`.

`uv` warto znac, bo przyda sie do:

```bash
uv --version
uv tool install ruff
uvx ruff --version
uv pip install pytest
```

Interpretacja:

```text
uv tool install ruff -> instaluje narzedzie CLI globalnie
uvx ruff --version  -> uruchamia narzedzie bez recznej instalacji w projekcie
uv pip install ...   -> szybka alternatywa dla pip w aktywnym venv
```

Na razie kontrakt homeworku zostaje:

```text
pyenv + Poetry + pytest
```

## Co commitowac

Commituj:

```text
.python-version
pyproject.toml
poetry.lock
python_basics.py
test_python_basics.py
orders.csv
notes.md
```

Nie commituj:

```text
.venv/
__pycache__/
.pytest_cache/
```

## Szybki debug setupu

| Problem | Co sprawdzic |
|---|---|
| `pyenv: command not found` | Czy shell byl odswiezony po instalacji? |
| `poetry: command not found` | Czy `pipx ensurepath` albo `uv tool install poetry` bylo wykonane? |
| `uv: command not found` | Czy shell byl odswiezony po instalacji `uv`? |
| `pytest: command not found` | Uzyj `poetry run pytest`, nie globalnego `pytest`. |
| VS Code widzi zly Python | Wybierz interpreter z `.venv/bin/python`. |
| Inna wersja Pythona w terminalu | Sprawdz `pyenv version` i `.python-version`. |
