#!/usr/bin/env python3

import os
import sys
from pathlib import Path

# Définition du répertoire de l'application Django-Bom
DATA_DIR = Path(os.getenv('DATA_DIR', '/home/yunohost.app/django-bom'))
VENV_BIN = DATA_DIR / ".venv" / "bin" / "python3"

def main():
    """ Exécute les commandes Django depuis le bon environnement virtuel. """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_bom.settings')

    # Vérifier si l'environnement virtuel existe
    if not VENV_BIN.exists():
        sys.stderr.write("Erreur: L'environnement virtuel Python n'existe pas.\n")
        sys.exit(1)

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
