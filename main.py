import discord
from discord.ext import commands
from discord import app_commands
import random
from keys import TOKEN

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix='dice', intents=intents)
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


def roll_dice(n):
    results = []

    def recursive_roll(n):
        print(f" Rolling {n} dice")
        for _ in range(n):
            roll = random.randint(1, 6)
            print(f"  Rolled a {roll}")
            results.append(roll)
            if roll == 6:
                print("  Rolled a 6, rolling an additional die")
                recursive_roll(1)

    recursive_roll(n)
    print(f"Final results: {results}")
    return results


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.tree.sync()


@bot.tree.command(name='roll', description='Rolls a dice')
@app_commands.describe(num_dice="How many dice?")
async def roll(interaction: discord.Interaction, num_dice: int):
    if num_dice <= 0:
        await interaction.response.send_message('You must roll at least one die.')
        return
    results = roll_dice(num_dice)
    successes = len([roll for roll in results if roll >= 5])
    await interaction.response.send_message(f'You rolled: {results}\nSuccesses: {successes}')

bot.run(TOKEN)
