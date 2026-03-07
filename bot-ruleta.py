import discord
from discord import app_commands
import random
import os
from flask import Flask
from threading import Thread

# --- TRUCO PARA RENDER GRATIS ---
app = Flask('')

@app.route('/')
def home():
    return "Bot de Ruleta Online!"

def run():
    # Render usa el puerto 10000 por defecto
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()
# --------------------------------

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f'Bot conectado como {client.user}')

@tree.command(name="ruleta", description="Divide un monto entre una lista")
async def ruleta(interaction: discord.Interaction, monto: float, nombres: str):
    lista_nombres = [n.strip() for n in nombres.split(",")]
    if not lista_nombres:
        await interaction.response.send_message("Escribe nombres separados por comas.")
        return
    
    random.shuffle(lista_nombres)
    pago_por_persona = monto / len(lista_nombres)
    
    respuesta = f"**Ruleta**\n"
    respuesta += f"Monto: ${monto:,.2f} | Cada uno: **${pago_por_persona:,.2f}**\n\n"
    for i, nombre in enumerate(lista_nombres, 1):
        respuesta += f"{i}. {nombre}\n"
    
    await interaction.response.send_message(respuesta)

# Iniciamos el servidor falso y luego el bot
keep_alive()
token = os.getenv('DISCORD_TOKEN')
client.run(token)

