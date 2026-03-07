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
    return "¡Bot de Crazy Raccoons Online!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURACIÓN DEL BOT ---
intents = discord.Intents.default()
intents.members = True  # RECUERDA: Activar 'Server Members Intent' en el Discord Developer Portal

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Sincroniza los comandos para que aparezcan en Discord
        await self.tree.sync()
        print("Comandos sincronizados con éxito.")

client = MyBot()

# Comando con 10 espacios para miembros (puedes añadir más si quieres)
@client.tree.command(name="ruleta", description="Reparto de botín con menciones azules aseguradas")
@app_commands.describe(
    monto="Cantidad total de plata",
    m1="Miembro 1", m2="Miembro 2", m3="Miembro 3", m4="Miembro 4", 
    m5="Miembro 5", m6="Miembro 6", m7="Miembro 7", m8="Miembro 8"
)
async def ruleta(interaction: discord.Interaction, monto: float, 
                 m1: discord.Member, m2: discord.Member, 
                 m3: discord.Member = None, m4: discord.Member = None, 
                 m5: discord.Member = None, m6: discord.Member = None,
                 m7: discord.Member = None, m8: discord.Member = None):
    
    # Filtramos solo los miembros que seleccionaste
    miembros_lista = [m for m in [m1, m2, m3, m4, m5, m6, m7, m8] if m is not None]
    
    # Mezclamos el orden para la ruleta
    random.shuffle(miembros_lista)
    
    # Calculamos el pago por persona
    pago_por_persona = int(monto / len(miembros_lista))

    # Creamos el diseño (Embed) con el color cian
    embed = discord.Embed(
        title="Ruleta - Crazy Raccoons", 
        color=discord.Color.from_rgb(0, 255, 255) 
    )
    
    # Formateamos los números con comas (ej: 1,000,000)
    embed.add_field(name="Total", value=f"{int(monto):,}", inline=True)
    embed.add_field(name="Por Persona", value=f"{pago_por_persona:,}", inline=True)
    
    # Generamos la lista de resultados usando .mention para forzar el color AZUL
    resultados = ""
    for i, miembro in enumerate(miembros_lista, 1):
        resultados += f"{i}. {miembro.mention}\n"
    
    embed.add_field(name="Resultados", value=resultados, inline=False)
    
    # Enviamos la respuesta
    await interaction.response.send_message(embed=embed)

# --- INICIO DEL BOT ---
if __name__ == "__main__":
    keep_alive()
    token = os.getenv('DISCORD_TOKEN')
    if token:
        client.run(token)
    else:
        print("Error: No se encontró el TOKEN en las variables de entorno.")
