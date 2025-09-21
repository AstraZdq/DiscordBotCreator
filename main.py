import os
import sys
import platform
import subprocess
from pathlib import Path
from shutil import which
import requests

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nAppuie sur Entrée pour continuer...")

def check_command(cmd):
    return which(cmd) is not None

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception:
        return None

def detect_os():
    return platform.system()

def check_python():
    try:
        import discord
    except ImportError:
        print("⚠️ La librairie discord.py n'est pas installée !")
        print("👉 Installe-la avec : pip install discord.py python-dotenv")
        sys.exit(1)

def check_node():
    if not check_command("node"):
        print("⚠️ Node.js n'est pas installé. Installe-le depuis https://nodejs.org/")
        sys.exit(1)

def validate_token(token):
    url = "https://discord.com/api/v10/users/@me"
    headers = {"Authorization": f"Bot {token}"}
    try:
        r = requests.get(url, headers=headers)
        return r.status_code == 200
    except Exception:
        return False

def create_structure(base_path, language, token):
    base = Path(base_path)
    (base / "commands").mkdir(parents=True, exist_ok=True)
    (base / "events").mkdir(parents=True, exist_ok=True)
    (base / "config").mkdir(parents=True, exist_ok=True)

    with open(base / ".env", "w", encoding="utf-8") as f:
        f.write(f"DISCORD_TOKEN={token}\n")

    if language == "python":
        # main.py
        with open(base / "main.py", "w", encoding="utf-8") as f:
            f.write("""import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path
import importlib

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

events_path = Path("events")
for file in events_path.glob("*.py"):
    module = importlib.import_module(f"events.{file.stem}")
    if hasattr(module, "setup"):
        module.setup(bot)

# Charger automatiquement les commandes
commands_path = Path("commands")
for file in commands_path.glob("*.py"):
    module = importlib.import_module(f"commands.{file.stem}")
    if hasattr(module, "setup"):
        module.setup(bot)

bot.run(TOKEN)
""")

        with open(base / "requirements.txt", "w", encoding="utf-8") as f:
            f.write("discord.py>=2.3.2\npython-dotenv>=1.0.1\nrequests>=2.31.0\n")

        with open(base / "config" / "config.py", "w", encoding="utf-8") as f:
            f.write("""# Configuration du bot
COMMAND_PREFIX = "!"
""")

        with open(base / "commands" / "ping.py", "w", encoding="utf-8") as f:
            f.write("""def setup(bot):
    @bot.command()
    async def ping(ctx):
        await ctx.send("Pong!")
""")

        with open(base / "events" / "on_ready.py", "w", encoding="utf-8") as f:
            f.write("""def setup(bot):
    @bot.event
    async def on_ready():
        print(f"✅ Connecté en tant que {bot.user}")
""")

        with open(base / "events" / "on_message.py", "w", encoding="utf-8") as f:
            f.write("""def setup(bot):
    @bot.event
    async def on_message(message):
        if message.author.bot:
            return
        await bot.process_commands(message)
""")

    elif language == "javascript":
        with open(base / "index.js", "w", encoding="utf-8") as f:
            f.write("""require('dotenv').config();
const { Client, GatewayIntentBits, Collection } = require('discord.js');
const fs = require('fs');
const path = require('path');

const TOKEN = process.env.DISCORD_TOKEN;

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});

client.commands = new Collection();

const commandsPath = path.join(__dirname, 'commands');
for (const file of fs.readdirSync(commandsPath)) {
    if (file.endsWith('.js')) {
        const command = require(`./commands/${file}`);
        client.commands.set(command.name, command);
    }
}

const eventsPath = path.join(__dirname, 'events');
for (const file of fs.readdirSync(eventsPath)) {
    if (file.endsWith('.js')) {
        const event = require(`./events/${file}`);
        if (event.once) {
            client.once(event.name, (...args) => event.execute(...args, client));
        } else {
            client.on(event.name, (...args) => event.execute(...args, client));
        }
    }
}

client.login(TOKEN);
""")

        with open(base / "package.json", "w", encoding="utf-8") as f:
            f.write("""{
  "name": "discord-bot",
  "version": "1.0.0",
  "main": "index.js",
  "license": "MIT",
  "dependencies": {
    "discord.js": "^14.16.3",
    "dotenv": "^16.4.5"
  }
}
""")

        with open(base / "config" / "config.js", "w", encoding="utf-8") as f:
            f.write("""module.exports = {
    prefix: "!"
};
""")

        with open(base / "commands" / "ping.js", "w", encoding="utf-8") as f:
            f.write("""module.exports = {
    name: "ping",
    description: "Répond avec Pong!",
    execute(message) {
        message.channel.send("Pong!");
    }
};
""")

        with open(base / "events" / "ready.js", "w", encoding="utf-8") as f:
            f.write("""module.exports = {
    name: "ready",
    once: true,
    execute(client) {
        console.log(`✅ Connecté en tant que ${client.user.tag}`);
    }
};
""")

        with open(base / "events" / "messageCreate.js", "w", encoding="utf-8") as f:
            f.write("""const config = require("../config/config");

module.exports = {
    name: "messageCreate",
    execute(message, client) {
        if (!message.content.startsWith(config.prefix) || message.author.bot) return;

        const args = message.content.slice(config.prefix.length).trim().split(/ +/);
        const commandName = args.shift().toLowerCase();

        const command = client.commands.get(commandName);
        if (command) {
            command.execute(message, args, client);
        }
    }
};
""")

def main():
    clear()
    print("=== Générateur de Bot Discord ===")
    print(f"OS détecté : {detect_os()}")

    choix = ""
    while choix not in ["1", "2"]:
        print("\nChoisis ton langage :")
        print("1. Python (discord.py)")
        print("2. JavaScript (discord.js)")
        choix = input("👉 ")

    language = "python" if choix == "1" else "javascript"

    if language == "python":
        check_python()
    else:
        check_node()

    dest = input("\nEntre le dossier de destination du projet : ").strip()
    if not dest:
        print("❌ Dossier invalide")
        sys.exit(1)

    token = input("Entre le token de ton bot : ").strip()
    if not token:
        print("❌ Token invalide")
        sys.exit(1)

    if not validate_token(token):
        print("❌ Le token est invalide ou expiré.")
        sys.exit(1)

    create_structure(dest, language, token)

    print("\n✅ Projet généré avec succès dans :", dest)
    if language == "python":
        print("👉 Lance ton bot avec : python main.py")
    else:
        print("👉 Lance ton bot avec : node index.js")

if __name__ == "__main__":
    main()
