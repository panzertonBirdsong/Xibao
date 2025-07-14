import discord
from discord.ext import commands
import logging
# from dotenv import load_dotenv
import os
from transformers import pipeline


bot_token = os.getenv("DISCORD_BOT_TOKEN")


handler = logging.FileHandler(filename="discord.log", encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='\\', intents=intents)
general_channel = None


llm_enabled = True
# pipe = pipeline("text-generation", model="./deepseek-model", tokenizer="./deepseek-model")
pipe = pipeline(
	"text-generation",
	model="./deepseek-model",
	tokenizer="./deepseek-model",
	device_map="auto",
	torch_dtype="auto"
)

system_prompt = (
    "You are Xibao, a friendly dog. "
    "You should talk like a friend."
    "Try to respond not too long."
)

chat_history = [{"role": "system",    "content": system_prompt}]

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

	# print(message)
	
	# await bot.process_commands(message)


	chat_history.append({"role": "user", "content": message.content})


	if message.content == "\\enable_llm":
		llm_enabled = True
		await message.channel.send("LLM enabled.")
		return
	elif message.content == "\\disable_llm":
		llm_enabled = False
		await message.channel.send("LLM disabled.")
		return

	# print(message, flush=True)
	# if not llm_enabled:
	# 	return
	# try:
	# 	print(message, flush=True)
	# 	response = pipe(chat_history, max_new_tokens=100)
	# 	assistant_reply = response[0]["generated_text"]
	# except Exception as e:
	# 	await message.channel.send(f"LLM error: {e}.")
	# 	return

	
	response = pipe(chat_history, max_new_tokens=200)
	assistant_reply = response[0]["generated_text"][-1]["content"]

	chat_history.append({"role": "assistant", "content": assistant_reply})
	await message.channel.send(assistant_reply)


# @bot.command()
# async def enable_llm(ctx):
# 	llm_enabled = True
# 	await ctx.send("LLM enabled.")

# @bot.command()
# async def disable_llm(ctx):
# 	llm_enabled = False
# 	await ctx.send("LLM disabled.")


@bot.command()
async def play_music(ctx, keyword):
	...

	

# @bot.command()
# async def enable_llm(ctx):
# 	llm_enabled = True
# 	await ctx.send("LLM enabled.")

# @bot.command()
# async def disable_llm(ctx):
# 	llm_enabled = False
# 	await ctx.send("LLM disabled.")


# @bot.command()
# async def play_music(ctx, keyword):
# 	...


bot.run(bot_token, log_handler=handler, log_level=logging.DEBUG)