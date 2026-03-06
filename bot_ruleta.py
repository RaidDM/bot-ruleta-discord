import discord
from discord import app_commands
from discord.ext import commands
import random
import os  # <--- Importante para leer la variable de entorno

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Bot conectado como {bot.user}')

@bot.tree.command(name="ruleta", description="Divide un monto y organiza los nombres al azar")
async def ruleta(interaction: discord.Interaction, monto: float, nombres: str):
    lista_nombres = nombres.replace(",", " ").split()
    
    if len(lista_nombres) < 1:
        await interaction.response.send_message("❌ Debes ingresar al menos un nombre.")
        return

    random.shuffle(lista_nombres)
    cantidad_personas = len(lista_nombres)
    pago_por_persona = monto / cantidad_personas

    embed = discord.Embed(
        title="🎰 Resultado de la Ruleta",
        color=discord.Color.gold(),
        description=f"Se ha dividido **{monto:,.2f}** entre **{cantidad_personas}** personas."
    )
    
    cuerpo_lista = ""
    for i, nombre in enumerate(lista_nombres, 1):
        cuerpo_lista += f"**{i}.** {nombre} — `{pago_por_persona:,.2f}`\n"
    
    embed.add_field(name="Orden de Reparto y Montos:", value=cuerpo_lista, inline=False)
    embed.set_footer(text="El orden se generó de forma aleatoria.")

    await interaction.response.send_message(embed=embed)

# --- ESTA ES LA PARTE QUE CAMBIA ---
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: No se encontró la variable DISCORD_TOKEN")
