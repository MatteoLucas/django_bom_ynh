#!/usr/bin/env python3

"""
    Setup Python for Django-Bom under YunoHost
    ------------------------------------------
    This script checks if the system Python version is compatible with Django-Bom.
    If not, it downloads and installs the correct standalone version.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Python version required for Django-Bom
REQUIRED_PYTHON_VERSION = "3.12"

# Paths
LOCAL_PYTHON_DIR = Path.home() / ".local" / f"python{REQUIRED_PYTHON_VERSION}"
PYTHON_BIN = LOCAL_PYTHON_DIR / "bin" / f"python{REQUIRED_PYTHON_VERSION}"
VENV_DIR = LOCAL_PYTHON_DIR / "venv"
REQUIREMENTS_FILE = Path(__file__).parent / "requirements.txt"

def is_python_installed():
    """Check if the required Python version is installed."""
    try:
        output = subprocess.check_output([PYTHON_BIN, "--version"], text=True).strip()
        return REQUIRED_PYTHON_VERSION in output
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def install_python():
    """Download and install Python standalone version."""
    print(f"Installing Python {REQUIRED_PYTHON_VERSION}...")

    # Define the URL for Python standalone build
    PYTHON_TAR_URL = f"https://github.com/indygreg/python-build-standalone/releases/latest/download/cpython-{REQUIRED_PYTHON_VERSION}-x86_64-unknown-linux-gnu.tar.zst"

    # Remove old installations
    shutil.rmtree(LOCAL_PYTHON_DIR, ignore_errors=True)

    # Download and extract
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

    # Move to final location
    shutil.move(str(TMP_DIR / "python"), str(LOCAL_PYTHON_DIR))

    if not PYTHON_BIN.exists():
        print("Error: Python installation failed!")
        sys.exit(1)

    print("Python installation completed.")

def setup_virtualenv():
    """Set up and activate a virtual environment, then install dependencies."""
    print("Setting up virtual environment...")
    subprocess.run([PYTHON_BIN, "-m", "venv", VENV_DIR], check=True)

    # Activate virtual environment
    venv_python = VENV_DIR / "bin" / "python"
    venv_pip = VENV_DIR / "bin" / "pip"

    print("Upgrading pip and installing dependencies...")
    subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"], check=True)

    if REQUIREMENTS_FILE.exists():
        subprocess.run([venv_pip, "install", "--upgrade", "-r", str(REQUIREMENTS_FILE)], check=True)
    else:
        print("Warning: requirements.txt not found, skipping dependencies installation.")

    print("Virtual environment setup completed.")

def main():
    """Main execution"""
    if is_python_installed():
        print(f"Python {REQUIRED_PYTHON_VERSION} is already installed.")
    else:
        install_python()
    
    setup_virtualenv()
    
    # Print the path to be used in shell scripts
    print(VENV_DIR / "bin" / "python")

if __name__ == "__main__":
    main()
