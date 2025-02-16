# Open School Success

Ce projet est un projet Django privé. Veuillez suivre les instructions ci-dessous pour configurer et lancer le projet.

## Prérequis

Assurez-vous d'avoir les éléments suivants installés sur votre machine :

- Python 3.11
- pip (gestionnaire de paquets Python)
- venv

## Installation

1. Clonez le dépôt du projet :

    ```bash
    git clone https://github.com/divad437/lost_and_found
    cd lost_and_found
    ```

2. Créez un environnement virtuel et activez-le :

    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
    ```

3. Installez les dépendances du projet :

    ```bash
    pip install -r requirements.txt
    ```

4. Migrez vers la branche de développement :

    ```bash
    git checkout dev
    ```

## Configuration

1. Appliquez les migrations de la base de données :

    ```bash
    python manage.py migrate
    ```

## Lancement du projet

1. Démarrez le serveur de développement Django :

    ```bash
    python manage.py runserver
    ```

2. Accédez à l'application via votre navigateur à l'adresse `http://127.0.0.1:8000`.



## Support

Pour toute question ou problème, veuillez contacter l'administrateur du projet.
