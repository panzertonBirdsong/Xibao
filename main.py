import discord
from discord.ext import commands
import logging
# from dotenv import load_dotenv
import os



bot_token = os.getenv("DISCORD_BOT_TOKEN")


handler = logging.FileHandler(filename="discord.log", encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='\\', intents=intents)
general_channel = None


llm_enabled = False

@bot.event
async def onready():
	print("No barking.")


@bot.event
async def on_member_join(member):
	# channel = member.guild.system_channel
	# await member.send("Welcome my son!")
	for channel in member.guild.text_channels:
		if channel.permissions_for(member).read_messages and channel.permissions_for(member).send_messages:
			await channel.send(f"Welcome my son, {member.mention}!")
			break

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	
	await bot.process_commands(message)

	if llm_enabled:
		...
	else:
		return



	

@bot.command()
async def enable_llm(ctx):
	llm_enabled = True
	await ctx.send("LLM enabled.")

@bot.command()
async def disable_llm(ctx):
	llm_enabled = False
	await ctx.send("LLM disabled.")


@bot.command()
async def play_music(ctx):
	


bot.run(bot_token, log_handler=handler, log_level=logging.DEBUG)