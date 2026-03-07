import discord
from discord import app_commands
import random
import os

# Configuración básica de Intents
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    # Sincroniza los comandos con Discord
    await tree.sync()
    print(f'Bot conectado como {client.user}')

@tree.command(name="ruleta", description="Divide un monto entre una lista de personas en orden aleatorio")
async def ruleta(interaction: discord.Interaction, monto: float, nombres: str):
    # Convertimos el string de nombres en una lista
    # Ejemplo: "Jugador1, Jugador2, Jugador3"
    lista_nombres = [n.strip() for n in nombres.split(",")]
    
    if len(lista_nombres) == 0:
        await interaction.response.send_message("Debes ingresar al menos un nombre.")
        return

    # Mezclamos la lista de forma aleatoria
    random.shuffle(lista_nombres)
    
    # Calculamos la división
    pago_por_persona = monto / len(lista_nombres)
    
    # Construimos el mensaje de respuesta
    respuesta = f"**💰 División de Botín 💰**\n"
    respuesta += f"Monto total: ${monto:,.2f}\n"
    respuesta += f"Cada uno recibe: **${pago_por_persona:,.2f}**\n\n"
    respuesta += "**Orden de la ruleta:**\n"
    
    for i, nombre in enumerate(lista_nombres, 1):
        respuesta += f"{i}. {nombre}\n"
    
    await interaction.response.send_message(respuesta)

# Token del bot (obtenido de las variables de entorno)
token = os.getenv('DISCORD_TOKEN')
client.run(token)
