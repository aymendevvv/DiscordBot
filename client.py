'''
   ####################### DEPRECATED #########################
'''

import discord 
import sandbox 
import aiosqlite
from discord.ext import commands
from discord import app_commands

async def send_message(message , user_message  , is_private):
    try:
        response = sandbox.handle_message(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e :
        print(e)

def run_discord_bot():
    TOKEN = 'MTE2Njc5MDE1NzAxNDQyMTU2NQ.GQvrYe.PF_sf2IAjUjIKj2QWoICvOFlJfjdpZSoCQk1e8'
    intents=discord.Intents.default()
    #intents.messages = True
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        
        print(f"{client.user} is running ")
        async with aiosqlite.connect("main.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER, guild INTEGER)') 
            await db.commit()

    @client.event 
    async def on_message(message) :
        if message.author == client.user:
            return
        print("message content ", message.content)
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'this message "{user_message}" was sent by {username} on channel : {channel}"')

        await send_message(message , user_message , is_private=False )
        await send_message(message , user_message , is_private=True )
    

    
        
    
    client.run(TOKEN)


