# 🤖 Discord Bot Generator

A simple cross-platform script (Windows/Linux/MacOS) that generates a fully working Discord bot project in Python (discord.py) or JavaScript (discord.js) with a !ping command.

Un script simple et multi-plateformes (Windows/Linux/MacOS) qui génère un projet bot Discord fonctionnel en Python (discord.py) ou JavaScript (discord.js) avec une commande !ping.

# 🌍 Features | Fonctionnalités

Detects your OS (Windows/Linux/MacOS)

Lets you choose between Python or JavaScript

Checks if required dependencies are installed (Python/Node.js + discord libraries)

Creates a ready-to-run bot project structure:

commands/ → bot commands

events/ → bot events

config/ → configuration files

.env → stores your bot token

Generates working code with a !ping command

Project runs immediately after setup

# 🚀 How to Use | Comment utiliser
1. Clone or download this repository
git clone https://github.com/your-username/discord-bot-generator.git
cd discord-bot-generator

2. Run the generator script | Lancez le script générateur
python setup_bot.py

3. Follow the instructions | Suivez les instructions

Choose Python or JavaScript

Enter the destination folder for your project

Enter your Discord bot token (saved securely in .env)

# 🐍 For Python (discord.py)
Install dependencies | Installer les dépendances
pip install -r requirements.txt

Run your bot | Lancer le bot
python main.py

⚡ For JavaScript (discord.js)
Install dependencies | Installer les dépendances
npm install

Run your bot | Lancer le bot
node index.js

📂 Project Structure | Structure du projet
project/
│── commands/      # Bot commands | Commandes du bot
│── events/        # Bot events   | Événements du bot
│── config/        # Config files | Fichiers de configuration
│── .env           # Stores your Discord token | Contient le token du bot
│── main.py        # Entry point if Python is chosen | Entrée si Python est choisi
│── index.js       # Entry point if JavaScript is chosen | Entrée si JavaScript est choisi

# ⚠️ Notes

Make sure you have Python 3.8+ or Node.js 16+ installed.

Your bot token must be generated from the Discord Developer Portal
.

Never share your token publicly.

✨ Author | >_ Vs⊥rv

Created with ❤️ to help beginners easily start a Discord bot project.