import os
import sys
import platform
import subprocess
from pathlib import Path
from shutil import which
import requests

# ==========================
# SYSTÈME DE LANGUES
# ==========================
LANG = {
    "fr": {
        "welcome": "=== Générateur de Bot Discord ===",
        "choose_lang": "\nChoisis ton langage :",
        "option_python": "1. Python (discord.py)",
        "option_js": "2. JavaScript (discord.js)",
        "choose_cmd": "\nMode des commandes :",
        "option_cmd": "1. Commandes classiques (!ping)",
        "option_slash": "2. Slash commands (/ping)",
        "invalid_folder": "❌ Dossier invalide",
        "invalid_token": "❌ Le token est invalide ou expiré.",
        "project_ok": "\n✅ Projet généré avec succès dans :",
        "launch_python": "👉 Lance ton bot avec : python main.py",
        "launch_js": "👉 Lance ton bot avec : node index.js"
    },
    "en": {
        "welcome": "=== Discord Bot Generator ===",
        "choose_lang": "\nChoose your language:",
        "option_python": "1. Python (discord.py)",
        "option_js": "2. JavaScript (discord.js)",
        "choose_cmd": "\nCommand mode:",
        "option_cmd": "1. Classic commands (!ping)",
        "option_slash": "2. Slash commands (/ping)",
        "invalid_folder": "❌ Invalid folder",
        "invalid_token": "❌ Invalid or expired token.",
        "project_ok": "\n✅ Project successfully generated in:",
        "launch_python": "👉 Run your bot with: python main.py",
        "launch_js": "👉 Run your bot with: node index.js"
    }
}

# ==========================
# FONCTIONS UTILITAIRES
# ==========================
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

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

# ==========================
# CRÉATION DES FICHIERS
# ==========================
def create_structure(base_path, language, token, is_slash):
    base = Path(base_path)
    (base / "commands").mkdir(parents=True, exist_ok=True)
    (base / "events").mkdir(parents=True, exist_ok=True)
    (base / "config").mkdir(parents=True, exist_ok=True)

    with open(base / ".env", "w", encoding="utf-8") as f:
        f.write(f"DISCORD_TOKEN={token}\n")

    # -------------------------
    # PYTHON
    # -------------------------
    if language == "python":
        with open(base / "main.py", "w", encoding="utf-8") as f:
            if is_slash:
                f.write("""import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Connecté en tant que {bot.user}")

@bot.tree.command(name="ping", description="Répond avec Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

bot.run(TOKEN)
""")
            else:
                f.write("""import sos
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

bot.run(TOKEN)
""")

        with open(base / "requirements.txt", "w", encoding="utf-8") as f:
            f.write("discord.py>=2.3.2\npython-dotenv>=1.0.1\nrequests>=2.31.0\n")

    # -------------------------
    # JAVASCRIPT
    # -------------------------
    elif language == "javascript":
        with open(base / "index.js", "w", encoding="utf-8") as f:
            if is_slash:
                f.write("""require('dotenv').config();
const { Client, GatewayIntentBits, SlashCommandBuilder, REST, Routes } = require('discord.js');

const TOKEN = process.env.DISCORD_TOKEN;
const CLIENT_ID = "TON_CLIENT_ID"; // ⚠️ Mets ton client ID
const GUILD_ID = "TON_GUILD_ID";   // ⚠️ Mets ton serveur ID (ou enlève pour global)

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

const commands = [
    new SlashCommandBuilder()
        .setName('ping')
        .setDescription('Répond avec Pong!')
        .toJSON()
];

const rest = new REST({ version: '10' }).setToken(TOKEN);

(async () => {
    try {
        console.log('🔄 Chargement des slash commands...');
        await rest.put(Routes.applicationGuildCommands(CLIENT_ID, GUILD_ID), { body: commands });
        console.log('✅ Slash commands chargées !');
    } catch (error) {
        console.error(error);
    }
})();

client.on('ready', () => {
    console.log(`✅ Connecté en tant que ${client.user.tag}`);
});

client.on('interactionCreate', async interaction => {
    if (!interaction.isChatInputCommand()) return;
    if (interaction.commandName === 'ping') {
        await interaction.reply('Pong!');
    }
});

client.login(TOKEN);
""")
            else:
                f.write("""require('dotenv').config();
const { Client, GatewayIntentBits } = require('discord.js');

const TOKEN = process.env.DISCORD_TOKEN;

const client = new Client({
    intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent]
});

client.on('ready', () => {
    console.log(`✅ Connecté en tant que ${client.user.tag}`);
});

client.on('messageCreate', message => {
    if (message.author.bot) return;
    if (message.content === '!ping') {
        message.channel.send('Pong!');
    }
});

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

# ==========================
# MAIN
# ==========================
def main():
    clear()

    # choix de langue
    print("1. Français")
    print("2. English")
    lang_choice = input("👉 ")
    current_lang = "fr" if lang_choice == "1" else "en"

    print(LANG[current_lang]["welcome"])
    print(f"OS détecté : {detect_os()}")

    # choix langage bot
    choix = ""
    while choix not in ["1", "2"]:
        print(LANG[current_lang]["choose_lang"])
        print(LANG[current_lang]["option_python"])
        print(LANG[current_lang]["option_js"])
        choix = input("👉 ")

    language = "python" if choix == "1" else "javascript"

    if language == "python":
        check_python()
    else:
        check_node()

    # choix type de commandes
    print(LANG[current_lang]["choose_cmd"])
    print(LANG[current_lang]["option_cmd"])
    print(LANG[current_lang]["option_slash"])
    cmd_mode = input("👉 ")
    is_slash = cmd_mode == "2"

    # destination projet
    dest = input("\nEntre le dossier de destination du projet : ").strip()
    if not dest:
        print(LANG[current_lang]["invalid_folder"])
        sys.exit(1)

    token = input("Entre le token de ton bot : ").strip()
    if not token:
        print(LANG[current_lang]["invalid_token"])
        sys.exit(1)

    if not validate_token(token):
        print(LANG[current_lang]["invalid_token"])
        sys.exit(1)

    create_structure(dest, language, token, is_slash)

    print(LANG[current_lang]["project_ok"], dest)
    if language == "python":
        print(LANG[current_lang]["launch_python"])
    else:
        print(LANG[current_lang]["launch_js"])

if __name__ == "__main__":
    main()