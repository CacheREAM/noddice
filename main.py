from discord.ext import commands
import random
from keys import TOKEN

bot = commands.Bot(command_prefix='!')


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


@bot.command(name='roll')
async def roll(ctx, n: int):
    if n <= 0:
        await ctx.send('You must roll at least one die.')
        return
    results = roll_dice(n)
    fives_and_sixes = [roll for roll in results if roll >= 5]
    await ctx.send(f'You rolled: {results}\nSuccesses: {sum(fives_and_sixes)}')

bot.run(TOKEN)
