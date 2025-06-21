import discord
from discord.ext import commands
import random
from keys import TOKEN

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix=None, intents=intents)


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


@bot.command(name='roll', description='Rolls a dice')
async def roll(ctx, n: int):
    if n <= 0:
        await ctx.respond('You must roll at least one die.')
        return
    results = roll_dice(n)
    fives_and_sixes = [roll for roll in results if roll >= 5]
    await ctx.respond(f'You rolled: {results}\nSuccesses: {sum(fives_and_sixes)}')

bot.run(TOKEN)
