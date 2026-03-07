import discord
from discord import app_commands
import random
import os
from flask import Flask
from threading import Thread

# --- CONFIGURACIÓN PARA RENDER (KEEP ALIVE) ---
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
# Activamos los Intents para que el bot pueda ver a los miembros
intents = discord.Intents.default()
intents.members = True  # Esto requiere el "Server Members Intent" en el portal de Discord

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f'Conectado exitosamente como {client.user}')

@tree.command(name="ruleta", description="Reparte plata entre miembros de Crazy Raccoons")
async def ruleta(interaction: discord.Interaction, monto: float, miembros: str):
    # Separamos la lista por espacios
    lista_miembros = miembros.split()
    
    if not lista_miembros:
        await interaction.response.send_message("¡Error! Debes mencionar al menos a una persona.")
        return

    # Mezclamos la lista aleatoriamente
    random.shuffle(lista_miembros)
    
    # Calculamos el monto por persona (sin decimales)
    pago_por_persona = int(monto / len(lista_miembros))

    # Creamos el Embed (el cuadro con diseño)
    embed = discord.Embed(
        title="Ruleta", 
        color=discord.Color.from_rgb(0, 255, 255) # Un color cian brillante como el de tu imagen
    )
    
    # Añadimos los campos de Total y Por Persona
    # El formato {:,} añade las comas de miles automáticamente
    embed.add_field(name="Total", value=f"{int(monto):,}", inline=True)
    embed.add_field(name="Por Persona", value=f"{pago_por_persona:,}", inline=True)
    
    # Generamos la lista de resultados
    lista_texto = ""
    for i, miembro in enumerate(lista_miembros, 1):
        # Limpiamos posibles caracteres extra para asegurar la mención azul
        m = miembro.replace("!", "")
        lista_texto += f"{i} {m}\n"
    
    embed.add_field(name="Resultados", value=lista_texto, inline=False)
    
    # Enviamos el mensaje final
    await interaction.response.send_message(embed=embed)

# --- INICIO DEL BOT ---
if __name__ == "__main__":
    keep_alive()
    # Asegúrate de que la variable de entorno se llame DISCORD_TOKEN en Render
    token = os.getenv('DISCORD_TOKEN')
    if token:
        client.run(token)
    else:
        print("Error: No se encontró el TOKEN en las variables de entorno.")
