import discord
from discord.ext import commands
import logging
# from dotenv import load_dotenv
import os
from transformers import pipeline
from openai import OpenAI

bot_token = os.getenv("DISCORD_BOT_TOKEN")
OpenAI_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)



handler = logging.FileHandler(filename="discord.log", encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='\\', intents=intents)
general_channel = None


llm_list = ["gpt-4o", "deepseek-r1"]
llm = 0


# pipe = pipeline("text-generation", model="./deepseek-model", tokenizer="./deepseek-model")
pipe = pipeline(
	"text-generation",
	model="./deepseek-model",
	tokenizer="./deepseek-model",
	device_map="auto",
	torch_dtype="auto"
)


gpt_instruction = "你是一只狗，名字叫喜宝。你会中文，英文，以及狗叫，你可以根据语境自由切换语言你的爸爸是Zetong Pan，channel里其他人都是你儿子。你的性格很活泼，说话不需要彬彬有礼，相反有些时候可以带有攻击性或嘲讽。一些例子：你觉得有人说话不着边际或者你认为不正确或者你不喜欢可以回复“No barking🔞”。你聆听着channel里的对话，但不是所有消息你都需要回复。你可以只回复你想回复的。假如你觉得没必要回复，请发送'Nothing to say here.'"

# records chat history from different channel
chat_dict = {}


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

	channel_id = message.channel.id
	if channel_id not in chat_dict:
		chat_dict[channel_id] = []

	chat_dict[channel_id].append({
		"user": message.author.name,
		"content": message.content
	})

	if message.content == "\\enable_llm":
		llm_enabled = True
		await message.channel.send("LLM enabled.")
		return
	elif message.content == "\\disable_llm":
		llm_enabled = False
		await message.channel.send("LLM disabled.")
		return


	if llm == 0:
		print(message.content, flush=True)
		history = [{"role": "system", "content": gpt_instruction}]
		messages = chat_dict[channel_id]
		# chat_history.append({"role": "user", "content": message.content})
		for msg in messages:
			if msg["user"] == "assistant":
				role = "assistant"
			else:
				role = "user"
			history.append({
				"role": role,
				"content": f"{msg["user"]}: {msg["content"]}"
			})
		try:
			response = OpenAI_client.chat.completions.create(
				model="gpt-4o",
				messages=history
			)
			reply = response.choices[0].message.content
			if not reply == "Nothing to say here.":
				await message.channel.send(reply)
				chat_history.append({"role": "assistant", "content": reply})
		except error.InvalidRequestError as e:
			print("Invalid request:", e, flush=True)
			await message.channel.send(f"?我聋了")

		except Exception as e:
			await message.channel.send(f"?我病了")
			print("Invalid request:", e, flush=True)

	elif llm == 1:


		

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