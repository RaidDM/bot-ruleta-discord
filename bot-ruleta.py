import discord
from discord import app_commands
import random
import os
from flask import Flask
from threading import Thread

# Servidor para Render (Gratis)
app = Flask('')
@app.route('/')
def home(): return "Bot Online!"

def run(): app.run(host='0.0.0.0', port=10000)
def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f'Conectado como {client.user}')

@tree.command(name="ruleta", description="Reparto de botín con menciones")
async def ruleta(interaction: discord.Interaction, monto: float, miembros: str):
    # Separa las menciones por espacio
    lista_miembros = miembros.split()
    
    if not lista_miembros:
        await interaction.response.send_message("Menciona a los miembros con @")
        return

    random.shuffle(lista_miembros)
    pago_por_persona = int(monto / len(lista_miembros))

    # Diseño del mensaje (Embed)
    embed = discord.Embed(title="Ruleta", color=discord.Color.blue())
    embed.add_field(name="Total", value=f"{int(monto):,}", inline=True)
    embed.add_field(name="Por Persona", value=f"{pago_por_persona:,}", inline=True)
    
    resultados = ""
    for i, m in enumerate(lista_miembros, 1):
        resultados += f"{i} {m}\n"
    
    embed.add_field(name="Resultados", value=resultados, inline=False)
    await interaction.response.send_message(embed=embed)

keep_alive()
client.run(os.getenv('DISCORD_TOKEN'))
