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
intents.members = True 
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f'Conectado como {client.user}')

@tree.command(name="ruleta", description="Reparto de botín para miembros infinitos")
async def ruleta(interaction: discord.Interaction, monto: float, miembros: str):
    # Usamos las menciones reales que Discord detecta en el texto
    # Esto filtra solo a los usuarios mencionados (los que salen en azul)
    lista_miembros = interaction.data.get('resolved', {}).get('users', {})
    
    # Si no detectó menciones integradas, intentamos separar por espacios el texto
    if not lista_miembros:
        lista_final = miembros.split()
    else:
        # Convertimos los IDs detectados en menciones de formato <@id>
        lista_final = [f"<@{user_id}>" for user_id in lista_miembros.keys()]

    if not lista_final:
        await interaction.response.send_message("Menciona a los miembros (ej: @Daniel @Yarod).")
        return

    random.shuffle(lista_final)
    pago_por_persona = int(monto / len(lista_final))

    # Diseño del Embed (Cuadro)
    embed = discord.Embed(
        title="Ruleta - Crazy Raccoons", 
        color=discord.Color.from_rgb(0, 255, 255)
    )
    
    embed.add_field(name="Total", value=f"{int(monto):,}", inline=True)
    embed.add_field(name="Por Persona", value=f"{pago_por_persona:,}", inline=True)
    
    resultados = ""
    for i, m in enumerate(lista_final, 1):
        # Forzamos que el bot use el formato de mención para el color azul
        resultados += f"{i}. {m}\n"
    
    embed.add_field(name="Resultados", value=resultados, inline=False)
    
    await interaction.response.send_message(embed=embed)

if __name__ == "__main__":
    keep_alive()
    token = os.getenv('DISCORD_TOKEN')
    if token:
        client.run(token)
