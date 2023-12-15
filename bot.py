import discord 
import responses 
import aiosqlite
from discord.ext import commands
from discord import app_commands
import os

async def send_message(message , user_message  , is_private):
    try:
        response = responses.handle_message(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e :
        print(e)

def run_discord_bot():
    TOKEN = os.getenv('reallycoolbot_token')
    print(TOKEN)
    intents = discord.Intents.default()
    intents.message_content = True
    intents.messages = True
    intents.guilds = True

    bot = commands.Bot(command_prefix='/'  , intents= intents)


    @bot.event
    async def on_ready():
        try : 
            synced = await bot.tree.sync() 
            print(f"synced  : {len(synced)} commands")
        except Exception as e : 
            print(e)

        
        print(f"{bot.user} is running ")
        async with aiosqlite.connect("main.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER, guild INTEGER)') 
            await db.commit()
    '''
     @bot.event 
    async def on_message(message) :
        if message.author == bot.user :
            return
        print("message content ", message.content)
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'this message "{user_message}" was sent by {username} on channel : {channel}"')

        await send_message(message , user_message , is_private=False )
        await send_message(message , user_message , is_private=True )
    '''
   
    
    @bot.tree.command(name="enroll")
    async def enroll(interaction: discord.Interaction):
        
        async with aiosqlite.connect("main.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute(" insert into users (text) values(?) ;" , (interaction.user.name , )) 
            await db.commit()

        await interaction.response.send_message(f"{interaction.user.mention } congrats you're in !")

        async with aiosqlite.connect("main.db") as db:
            participants = []
            async with db.cursor() as cursor:
                await cursor.execute(" select * from dummyData ") 
                rows  = await cursor.fetchall()
                for row in rows :
                    participants.append(row[1])
            await db.commit()
        multilined = "\n".join(participants)
        await interaction.followup.send(f"along side : \n{ multilined }")

    ####################################### start event ################################################
    @bot.tree.command(name="start_evt")
    @app_commands.describe(evt_args='what is the event name ? ')
    async def startevt(interaction: discord.Interaction , evt_args:str):
        params = evt_args.split(" ") 

        print(params)
    
        async with aiosqlite.connect("main.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute(" insert into event (name , start_date , end_date) values(? , ? , ? ) ;" , (params[0] ,params[1] ,params[2] , )) 
            await db.commit()

        await interaction.response.send_message(f" new event started by {interaction.user.nick}")
    ####################################### add challenges ################################################
    @bot.tree.command(name="add_challenge")
    @app_commands.describe(evt_id='to which event ?')
    async def add_challenge(interaction: discord.Interaction , evt_id:str):
        
        await interaction.response.send_message("chat is the challenge id ")
        challenge_id = await bot.wait_for("message", check=lambda msg: msg.author == interaction.user)
        print(f"recieved : {challenge_id.content}")


        start_date = await bot.wait_for("message", check=lambda msg: msg.author == interaction.user)
        print(f"recieved #2 : {start_date.content}")

        #await interaction.response.send_message("enter starting date  ")
        #start_date = await bot.wait_for("message", check=lambda msg: msg.author == interaction.user)

        

    
        async with aiosqlite.connect("main.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute(" insert into challenges (id , id_event , start_date) values(? , ? , ? ) ;" , (challenge_id.content ,evt_id ,start_date.content , )) 
            await db.commit()

        await interaction.followup.send(f" new challenge added by  {interaction.user.nick}")
        '''

        async with aiosqlite.connect("main.db") as db:
            participants = []
            async with db.cursor() as cursor:
                await cursor.execute(" select * from dummyData ") 
                rows  = await cursor.fetchall()
                for row in rows :
                    participants.append(row[1])
            await db.commit()
        multilined = "\n".join(participants)
        await interaction.followup.send(f"along side : \n{ multilined }")

        '''
        
        
        

    
        
    
    bot.run(TOKEN)


