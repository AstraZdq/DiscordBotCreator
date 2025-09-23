# 🤖 Générateur de Bot Discord

Un script **simple** et **multi-plateformes** (Windows / Linux / MacOS) qui génère automatiquement un projet complet de **bot Discord** en **Python (discord.py)** ou **JavaScript (discord.js)**.  
👉 Le projet généré inclut directement une commande de test `!ping` ou `/ping`.

---

## 🌍 Fonctionnalités

✨ Ce générateur vous permet de :

✅ Détecter automatiquement votre système (Windows/Linux/MacOS)  
✅ Choisir entre **Python** ou **JavaScript**  
✅ Vérifier si les dépendances nécessaires sont installées (**Python / Node.js + librairies Discord**)  
✅ Générer une structure de projet prête à l’emploi :  

```bash
project/
│── commands/ # Commandes du bot
│── events/ # Événements du bot
│── config/ # Fichiers de configuration
│── .env # Stocke le token du bot
│── main.py # Point d’entrée si Python est choisi
│── index.js # Point d’entrée si JavaScript est choisi

```

✅ Crée automatiquement une commande de test `!ping` ou `/ping`  
✅ Permet de lancer immédiatement le bot après génération  

---

## 🚀 Installation & Utilisation

### 1️⃣ Cloner le dépôt

```bash
git clone https://github.com/AstraZdq/DiscordBotCreator.git
cd discord-bot-generator
```
2️⃣ Lancer le script générateur

```bash
python main.py
```

3️⃣ Suivre les instructions
Choisir Python ou JavaScript

Indiquer le dossier de destination

Coller le token de votre bot Discord (stocké en sécurité dans .env)

🐍 Utilisation avec Python (discord.py)
Installer les dépendances :
```bash
pip install -r requirements.txt
```

Lancer le bot :
```bash
python main.py
```

⚡ Utilisation avec JavaScript (discord.js)
Installer les dépendances :

```bash
npm install
```

Lancer le bot :

```bash
node index.js
```

⚠️ Notes importantes
Assurez-vous d’avoir Python 3.8+ ou Node.js 16+ installé.

Le token de votre bot doit être généré depuis le Discord Developer Portal.

❌ Ne partagez jamais votre token publiquement.

✨ Auteur
👨‍💻 Vs⊥rv
Créé avec ❤️ pour aider les débutants à lancer rapidement un projet de bot Discord.