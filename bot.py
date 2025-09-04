import os
from pathlib import Path

import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv, dotenv_values

# === Carrega o .env que está AO LADO do bot.py ===
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")  # deixe vazio para registrar globalmente

# Validação amigável
if not TOKEN:
    keys = list(dotenv_values(ENV_PATH).keys())
    raise RuntimeError(
        f"DISCORD_TOKEN não encontrado no arquivo {ENV_PATH}.\n"
        f"Chaves detectadas nesse .env: {keys}\n"
        f"Verifique o nome da chave e se o arquivo está no mesmo diretório do bot.py."
    )

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Logado como {bot.user} (ID: {bot.user.id})")
    try:
        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            # copia os comandos (definidos abaixo) para o escopo do seu servidor
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            print(f"✅ {len(synced)} comandos sincronizados (escopo do servidor {GUILD_ID}).")
        else:
            # registra globalmente (pode demorar alguns minutos para aparecer)
            synced = await bot.tree.sync()
            print(f"✅ {len(synced)} comandos globais sincronizados.")
    except Exception as e:
        print(f"Erro ao sincronizar: {e}")

@bot.tree.command(name="ping", description="Responde com Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@bot.tree.command(name="say", description="O bot repete sua mensagem")
@app_commands.describe(text="Texto para o bot falar")
async def say(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(text)

bot.run(TOKEN)
