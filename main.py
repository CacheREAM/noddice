import discord
from discord.ext import commands
from discord import app_commands
import random
from keys import TOKEN

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix=None, intents=intents)
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


def roll_dice(n):
    results = []

    def recursive_roll(n):
        rolls = [random.randint(1, 6) for _ in range(n)]
        results.extend(rolls)
        for i, roll in enumerate(rolls):
            if roll == 6:
                recursive_roll(1)
    recursive_roll(n)
    return sorted(results)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.tree.sync()


@bot.tree.command(name='roll', description='Rolls a dice')
@app_commands.nodroll(num_dice="How many dice?")
async def roll(interaction: discord.Interaction, num_dice: int):
    if num_dice <= 0:
        await interaction.response.send_message('You must roll at least one die.')
        return
    results = roll_dice(num_dice)
    fives_and_sixes = [roll for roll in results if roll >= 5]
    await interaction.response.send_message(f'You rolled: {results}\nSuccesses: {sum(fives_and_sixes)}')

bot.run(TOKEN)
