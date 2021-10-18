import discord
from conversation import Conversation

TOKEN = 'token here'
client = discord.Client()
conv = Conversation()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):

    text = None

    # If bot is mentioned
    if message.mentions:
        if message.mentions[0].id == client.user.id:

            # Mentioned by name
            if message.content[3:21] == str(message.mentions[0].id):
                # Extract text
                text = message.content[23:]
            else:
                # Mentioned by reply
                text = message.content

    # If no text provided in either case return error
    if not text:
        return None

    # If command
    if text.split()[0] == "-model":
        model = text.split()[1]
        if model in ["large", "medium", "small"]:
            response = await message.channel.send("Switching models...")
            conv.switch_model(model)
            return await response.edit(content="Done!")
        else:
            return message.reply("Legal models are: large, medium, small")

    # If proper response
    response = conv.generate_response(text)
    # Reply with generated response
    await message.reply(response)

client.run(TOKEN)