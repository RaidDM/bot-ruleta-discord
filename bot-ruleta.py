import discord
from discord.ext import commands
import random
import os
from flask import Flask
from threading import Thread

# --- SECCIÓN KEEP-ALIVE (Para que Render no lo apague) ---
app = Flask('')

@app.route('/')
def home():
    return "El bot está en línea y funcionando."

def run():
    # Render usa el puerto 8080 por defecto para servicios web gratuitos
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURACIÓN DEL BOT ---
intents = discord.Intents.default()
intents.message_content = True  # Necesario para leer comandos

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Conectado como {bot.user.name}')
    print('------')

@bot.command()
async def ruleta(ctx):
    """Comando de ruleta rusa simple"""
    respuestas = [
        "¡PUM! Estás fuera. 💥",
        "Clic... te has salvado. 🛡️",
        "Clic... la cámara está vacía. ✨",
        "¡PUM! Mala suerte esta vez. 💀"
    ]
    await ctx.send(random.choice(respuestas))

@bot.command()
async def hola(ctx):
    await ctx.send(f"Hola {ctx.author.mention}, ¡listo para la acción!")

# --- EJECUCIÓN ---
if __name__ == "__main__":
    # 1. Iniciamos el servidor web en segundo plano
    keep_alive()
    
    # 2. Iniciamos el bot de Discord
    # Asegúrate de tener el TOKEN en las variables de entorno de Render
    token = os.getenv('DISCORD_TOKEN')
    
    if token:
        bot.run(token)
    else:
        print("Error: No se encontró la variable de entorno DISCORD_TOKEN")
