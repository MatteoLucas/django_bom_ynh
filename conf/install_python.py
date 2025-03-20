#!/usr/bin/env python3

"""
    Install Python for Django-Bom on YunoHost
    -----------------------------------------
    This script checks if the system Python version is sufficient.
    If not, it downloads and installs a precompiled standalone version.
    Then, it sets up a virtual environment and installs dependencies.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Version minimale requise de Python pour Django-Bom
REQUIRED_PYTHON_VERSION = "3.12"

# Chemins d'installation
LOCAL_PYTHON_DIR = Path.home() / ".local" / f"python{REQUIRED_PYTHON_VERSION}"
PYTHON_BIN = LOCAL_PYTHON_DIR / "bin" / f"python{REQUIRED_PYTHON_VERSION}"
VENV_DIR = LOCAL_PYTHON_DIR / "venv"
REQUIREMENTS_FILE = Path(__file__).parent / "requirements.txt"

def get_system_python_version():
    """Vérifie la version actuelle de Python installée."""
    try:
        output = subprocess.check_output(["python3", "--version"], text=True).strip()
        return output.split()[1]  # Extrait la version
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None

def is_python_installed():
    """Vérifie si la bonne version de Python est déjà installée."""
    system_version = get_system_python_version()
    if system_version and system_version.startswith(REQUIRED_PYTHON_VERSION):
        return True  # La version système est suffisante
    try:
        output = subprocess.check_output([PYTHON_BIN, "--version"], text=True).strip()
        return REQUIRED_PYTHON_VERSION in output
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def install_python():
    """Télécharge et installe une version précompilée de Python."""
    print(f"Installing Python {REQUIRED_PYTHON_VERSION}...")

    # URL de la version précompilée de Python
    PYTHON_TAR_URL = f"https://github.com/indygreg/python-build-standalone/releases/latest/download/cpython-{REQUIRED_PYTHON_VERSION}-x86_64-unknown-linux-gnu.tar.zst"

    # Supprimer l'ancienne installation si existante
    shutil.rmtree(LOCAL_PYTHON_DIR, ignore_errors=True)

    # Téléchargement et extraction
    TMP_DIR = Path("/tmp/python_install")
    TMP_DIR.mkdir(exist_ok=True)
    TAR_FILE = TMP_DIR / "python.tar.zst"

    print("Downloading Python...")
    subprocess.run(["wget", "-O", TAR_FILE, PYTHON_TAR_URL], check=True)

    if not TAR_FILE.exists():
        print("Error: Download failed!")
        sys.exit(1)

    print("Extracting Python...")
    subprocess.run(["tar", "--use-compress-program=zstd", "-xf", TAR_FILE, "-C", TMP_DIR], check=True)

    if not (TMP_DIR / "python").exists():
        print("Error: Extraction failed!")
        sys.exit(1)

    # Déplacement vers le dossier final
    shutil.move(str(TMP_DIR / "python"), str(LOCAL_PYTHON_DIR))

    if not PYTHON_BIN.exists():
        print("Error: Python installation failed!")
        sys.exit(1)

    print("Python installation completed.")

def setup_virtualenv():
    """Configure un environnement virtuel et installe les dépendances."""
    print("Setting up virtual environment...")

    # Création du venv
    subprocess.run([PYTHON_BIN, "-m", "venv", VENV_DIR], check=True)

    venv_python = VENV_DIR / "bin" / "python"
    venv_pip = VENV_DIR / "bin" / "pip"

    # Mise à jour de pip et installation des dépendances
    print("Upgrading pip and installing dependencies...")
    subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"], check=True)

    if REQUIREMENTS_FILE.exists():
        subprocess.run([venv_pip, "install", "-r", str(REQUIREMENTS_FILE)], check=True)
    else:
        print("Warning: requirements.txt not found, skipping dependencies installation.")

    print("Virtual environment setup completed.")

def main():
    """Exécute le script d’installation si nécessaire."""
    if is_python_installed():
        print(f"Python {REQUIRED_PYTHON_VERSION} is already installed.")
    else:
        install_python()
    
    setup_virtualenv()

    # Affiche le chemin pour les scripts shell
    print(VENV_DIR / "bin" / "python")

if __name__ == "__main__":
    main()
