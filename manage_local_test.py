#!/usr/bin/env python3

"""
    Call the "manage.py" from the local test environment for Django-Bom.
"""

import os
import sys
import subprocess

# Définir l'environnement local de test
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_bom.settings")
os.environ.setdefault("ENV_TYPE", "local")

def run_local_test_manage():
    """ Exécute manage.py avec les arguments donnés """
    manage_py_path = os.path.join(os.path.dirname(__file__), "manage.py")

    if not os.path.exists(manage_py_path):
        print("Erreur : `manage.py` introuvable. Vérifiez que vous êtes dans le bon répertoire.")
        sys.exit(1)

    command = [sys.executable, manage_py_path] + sys.argv[1:]
    subprocess.run(command, check=True)

if __name__ == '__main__':
    run_local_test_manage()
