import discord
from discord import app_commands
import random
import os
from flask import Flask
from threading import Thread

# --- CONFIGURACIÓN PARA RENDER ---
app = Flask('')
@app.route('/')
def home(): 
    return "¡Bot de Crazy Raccoons Online!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURACIÓN DEL BOT ---
intents = discord.Intents.default()
intents.members = True # Requiere 'Server Members Intent' en el Portal

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f'Bot conectado como {client.user}')

@tree.command(name="ruleta", description="Reparto con menciones azules infinitas")
async def ruleta(interaction: discord.Interaction, monto: float, miembros: str):
    # Separamos la cadena de texto por espacios
    elementos = miembros.split()
    
    if not elementos:
        await interaction.response.send_message("Menciona a los miembros con @")
        return

    # Mezclamos la lista
    random.shuffle(elementos)
    
    # Calculamos el pago por persona
    pago_por_persona = int(monto / len(elementos))

    # Diseño del Embed (Color Cian de los Crazy Raccoons)
    embed = discord.Embed(
        title="Ruleta - Crazy Raccoons", 
        color=discord.Color.from_rgb(0, 255, 255)
    )
    
    embed.add_field(name="Total", value=f"{int(monto):,}", inline=True)
    embed.add_field(name="Por Persona", value=f"{pago_por_persona:,}", inline=True)
    
    # Construimos la lista de resultados
    resultados = ""
    for i, m in enumerate(elementos, 1):
        # El bot simplemente imprime lo que recibe. 
        # Si seleccionas el nombre de la lista de Discord, se verá azul.
        resultados += f"{i}. {m}\n"
    
    embed.add_field(name="Resultados", value=resultados, inline=False)
    
    await interaction.response.send_message(embed=embed)

if __name__ == "__main__":
    keep_alive()
    client.run(os.getenv('DISCORD_TOKEN'))
