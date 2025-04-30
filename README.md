# ai-playground

## EN

This repo is a playground, I use is to mess around with Python and Mistral AI.

My goal is to create a chatbot were you can play textual games in French

## FR

Ce repo est un bac à sable, je m'en sers pour m'amuser avec Python et l'IA de Mistral.

Mon but est de coder un chatbot pour jouer à des jeux en texte en français.

Consulter 'CHANGELOG.MD' pour plus d'informations

### Prérequis

- Python 3.10 ou plus récent
- Obtenir une clé d'API Mistral ([documentation en anglais](https://docs.mistral.ai/getting-started/quickstart/#account-setup))
- Stocker la clé dans une variable d'environnement "MISTRAL_API_KEY"

### Utilisation

- Cloner le repo sur votre machine
- Lancer le script avec la commande python:

```bash
python chatbot-test.py
```

- De l'aide est disponible avec l'argument `-h`:

```bash
python chatbot-test.py -h              
usage: chatbot-test.py [-h] [--logLevel LOGLEVEL]

Requirements to use the AI playground chatbot

options:
  -h, --help           show this help message and exit
  --logLevel LOGLEVEL  Log level between DEBUG, INFO, WARNING, ERROR AND CRITICAL (default set to INFO)
```
