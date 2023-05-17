import discord
import responses
import constants
import aiohttp
import io

# Send messages
async def send_message(message, user_message, is_private):
    chat_response=[]
    image_url=''
    try:
        chat_response = responses.handle_response(user_message)
        image_url = responses.generate_dalle_image(chat_response[0])
        async with aiohttp.ClientSession() as session: # creates session
            async with session.get(image_url) as resp: # gets image from url
                img = await resp.read() # reads image from response
                with io.BytesIO(img) as file: # converts to file-like object    
                    await message.channel.send(chat_response[0])    
                    if chat_response[1] == '1':
                        await message.channel.send(file=discord.File(file, "dalleResponse.png"))

        # await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = constants.token
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        # Make sure bot doesn't get stuck in an infinite loop
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        # Debug printing
        print(f"{username} said: '{user_message}' ({channel})")

        await send_message(message, user_message, is_private=False)

    client.run(TOKEN)