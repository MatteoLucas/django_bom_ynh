#!/usr/bin/env python3

"""
    Bootstrap CLI for Django-Bom development
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Just call this file, and the magic happens ;)
"""

import hashlib
import shlex
import subprocess
import sys
import venv
from pathlib import Path


def print_no_pip_error():
    print('Error: Pip not available!')
    print('Hint: "apt-get install python3-venv"\n')


try:
    from ensurepip import version
except ModuleNotFoundError as err:
    print(err)
    print('-' * 100)
    print_no_pip_error()
    raise
else:
    if not version():
        print_no_pip_error()
        sys.exit(-1)


assert sys.version_info >= (3, 11), f'Python version {sys.version_info} is too old!'


if sys.platform == 'win32':  # Windows-specific handling
    BIN_NAME = 'Scripts'
    FILE_EXT = '.exe'
else:
    BIN_NAME = 'bin'
    FILE_EXT = ''

BASE_PATH = Path(__file__).parent
VENV_PATH = BASE_PATH / '.venv'
BIN_PATH = VENV_PATH / BIN_NAME
PYTHON_PATH = BIN_PATH / f'python3{FILE_EXT}'
PIP_PATH = BIN_PATH / f'pip{FILE_EXT}'
PIP_SYNC_PATH = BIN_PATH / f'pip-sync{FILE_EXT}'

# 🚨 MODIFICATION : Utilisation unique de requirements.txt
DEP_LOCK_PATH = BASE_PATH / 'requirements.txt'  
DEP_HASH_PATH = VENV_PATH / '.dep_hash'

# Script défini dans `pyproject.toml` sous `[project.scripts]`
PROJECT_SHELL_SCRIPT = BIN_PATH / 'django_bom_dev'


def get_dep_hash():
    """Get SHA512 hash from lock file content."""
    return hashlib.sha512(DEP_LOCK_PATH.read_bytes()).hexdigest()


def store_dep_hash():
    """Generate .venv/.dep_hash"""
    DEP_HASH_PATH.write_text(get_dep_hash())


def venv_up2date():
    """Check if existing .venv is up-to-date"""
    if DEP_HASH_PATH.is_file():
        return DEP_HASH_PATH.read_text() == get_dep_hash()
    return False


def verbose_check_call(*popen_args):
    print(f'\n+ {shlex.join(str(arg) for arg in popen_args)}\n')
    return subprocess.check_call(popen_args)


def main(argv):
    assert DEP_LOCK_PATH.is_file(), f'File not found: "{DEP_LOCK_PATH}" !'

    # Créer un environnement virtuel si inexistant
    if not PYTHON_PATH.is_file():
        print(f'Creating virtual environment at: {VENV_PATH.absolute()}')
        builder = venv.EnvBuilder(symlinks=True, upgrade=True, with_pip=True)
        builder.create(env_dir=VENV_PATH)

    # Mettre à jour les dépendances si nécessaire
    if not PROJECT_SHELL_SCRIPT.is_file() or not venv_up2date():
        verbose_check_call(PYTHON_PATH, '-m', 'pip', 'install', '-U', 'pip')

        # Installer pip-tools
        verbose_check_call(PYTHON_PATH, '-m', 'pip', 'install', '-U', 'pip-tools')

        # 🚨 MODIFICATION : Installation des dépendances depuis requirements.txt
        verbose_check_call(PIP_SYNC_PATH, str(DEP_LOCK_PATH))

        # Installer Django-Bom en mode développement
        verbose_check_call(PIP_PATH, 'install', '--no-deps', '-e', '.')

        store_dep_hash()

    # Lancer le CLI du projet
    try:
        verbose_check_call(PROJECT_SHELL_SCRIPT, *argv[1:])
    except subprocess.CalledProcessError as err:
        sys.exit(err.returncode)
    except KeyboardInterrupt:
        print('Bye!')
        sys.exit(130)


if __name__ == '__main__':
    main(sys.argv)
