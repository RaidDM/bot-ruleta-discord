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

@tree.command(name="ruleta", description="Divide un monto entre miembros mencionados")
async def ruleta(interaction: discord.Interaction, monto: float, miembros: str):
    # Separamos las menciones (ejemplo: @usuario1 @usuario2)
    # Al poner las menciones en el comando, Discord las envía como <@id>
    lista_miembros = miembros.split() 
    
    if not lista_miembros:
        await interaction.response.send_message("Menciona a los miembros (ej: @Daniel @Yarod).")
        return
    
    # Mezclamos el orden
    random.shuffle(lista_miembros)
    
    # Calculamos la división (sin decimales largos para que se vea limpio)
    pago_por_persona = int(monto / len(lista_miembros))
    
    # Creamos el diseño (Embed)
    embed = discord.Embed(
        title="Ruleta",
        color=discord.Color.blue() # Color de la barra lateral
    )
    
    # Añadimos los campos de Total y Por Persona uno al lado del otro
    embed.add_field(name="Total", value=f"{int(monto):,}", inline=True)
    embed.add_field(name="Por Persona", value=f"{pago_por_persona:,}", inline=True)
    
    # Creamos la lista numerada con las menciones
    lista_texto = ""
    for i, miembro in enumerate(lista_miembros, 1):
        lista_texto += f"{i} {miembro}\n"
    
    embed.add_field(name="Resultados", value=lista_texto, inline=False)
    
    await interaction.response.send_message(embed=embed)

# Iniciamos el servidor falso y luego el bot
keep_alive()
token = os.getenv('DISCORD_TOKEN')
client.run(token)


