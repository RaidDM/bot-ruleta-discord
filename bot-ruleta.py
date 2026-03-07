import discord
from discord import app_commands
import random
import os
from flask import Flask
from threading import Thread

# --- CONEXIÓN PARA RENDER (KEEP ALIVE) ---
app = Flask('')
@app.route('/')
def home(): 
    return "Bot de Crazy Raccoons Online!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURACIÓN DEL BOT ---
intents = discord.Intents.default()
intents.members = True          # IMPORTANTE: Activar en Developer Portal
intents.message_content = True  # IMPORTANTE: Activar en Developer Portal

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    # Sincroniza los comandos con Discord
    await tree.sync()
    print(f'Logueado como {client.user}')

@tree.command(name="ruleta", description="Reparte botín con menciones azules")
async def ruleta(interaction: discord.Interaction, monto: float, miembros: str):
    # Separamos lo que escribiste por espacios
    lista_cruda = miembros.split()
    
    if not lista_cruda:
        await interaction.response.send_message("Debes mencionar a alguien.")
        return

    # Mezclamos la lista
    random.shuffle(lista_cruda)
    
    # Cálculo de plata por persona
    pago_por_persona = int(monto / len(lista_cruda))

    # Creamos el diseño del cuadro (Embed)
    embed = discord.Embed(
        title="Ruleta - Crazy Raccoons", 
        color=discord.Color.from_rgb(0, 255, 255) # Color cian
    )
    
    # Formato de números con comas (1,000,000)
    embed.add_field(name="Total", value=f"{int(monto):,}", inline=True)
    embed.add_field(name="Por Persona", value=f"{pago_por_persona:,}", inline=True)
    
    # Construcción de la lista de resultados
    resultados = ""
    for i, m in enumerate(lista_cruda, 1):
        # Si el nombre no tiene el formato <@ID>, intentamos que Discord lo reconozca
        # Para que salga azul, DEBES seleccionar al usuario de la lista de Discord
        resultados += f"{i}. {m}\n"
    
    embed.add_field(name="Resultados", value=resultados, inline=False)
    
    # Enviamos la respuesta
    await interaction.response.send_message(embed=embed)

# --- INICIO ---
if __name__ == "__main__":
    keep_alive()
    token = os.getenv('DISCORD_TOKEN')
    if token:
        client.run(token)
    else:
        print("Error: No se encontró el TOKEN en las variables de entorno.")
