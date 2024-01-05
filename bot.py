import discord 
import responses 
import aiosqlite
import random
from discord.ext import commands
from discord import app_commands
import os
from databaseMng import chose_random , list_challenges_for , enrollement , registering




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
   
    #################################### enroll ###################################################
    
    @bot.tree.command(name="enroll")
    @app_commands.describe(evt='enter event id')
    async def enroll( interaction: discord.Interaction , evt:str):
        try : 
            enrollement(interaction.user.name , evt )
            await interaction.response.send_message(f"{interaction.user.mention } congrats you're in ")
        except Exception as e : 
            await interaction.response.send_message(f"{e.args[0]}")
    #################################### register ###################################################
            

    @bot.tree.command(name="register")
    @app_commands.describe(username='enter leetcode username')
    async def register( interaction: discord.Interaction , username:str):
        try : 
            registering(interaction.user.name , username )
            await interaction.response.send_message(f"{interaction.user.mention } you're now resigtered in the system !")
        except Exception as e : 
            await interaction.response.send_message(e)



    ####################################### start event ################################################
    @bot.tree.command(name="start_evt")
    @app_commands.describe(evt_args='what is the event name ? ')
    async def startevt(interaction: discord.Interaction , evt_args:str):
        params = evt_args.split(":::") 

        print(params)
        start_date = int(params[1])
        end_date = int(params[2])
        
    
        async with aiosqlite.connect("main.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute(" insert into event (name , start_date , end_date) values(? , ? , ? ) ;" , (params[0] , start_date,end_date , )) 
            await db.commit()

        await interaction.response.send_message(f" new event started by {interaction.user.nick} , lasts {((end_date-start_date) // 86400)+1 } days")
    
    
    ####################################### add challenges ################################################
    @bot.tree.command(name="add_challenge")
    @app_commands.describe(evt_id='to which event ?')
    async def add_challenge(interaction: discord.Interaction , evt_id:str):
        
        await interaction.response.send_message("what is the challenge id ")
        query = await bot.wait_for("message", check=lambda msg: msg.author == interaction.user)
        print(f"recieved : {query.content}")


        num = await bot.wait_for("message", check=lambda msg: msg.author == interaction.user)
        print(f"recieved #2 : {num.content}")
        
        async with aiosqlite.connect("main.db") as db:
            #get the event starting date : 
            async with db.cursor() as cursor:
                await cursor.execute(f"select start_date from event where id ={evt_id}") 
                result:int  = await cursor.fetchone()
                if result :
                    start_date = result[0]
                    
                sixpm = start_date - (start_date % (24 * 3600)) + (18 * 3600)

                for qst_id in chose_random(query.content  , int(num.content)) : 
                    sixpm += 86400  
                    await cursor.execute(" insert into challenges (id , id_event , start_date) values(? , ? , ? ) ;" , (qst_id , evt_id , sixpm + random.randint(-3500 , 3500) , )) 
            await db.commit()

        await interaction.followup.send(f"{num.content} random challenges were added")
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
    ####################################### list_challenges_for ################################################
    @bot.tree.command(name="list_challenges_for")
    @app_commands.describe(evnt_slug='get the list of challenges ')
    async def list_challenges(interaction: discord.Interaction , evnt_slug:str):
        
        rows = list_challenges_for(evnt_slug)
        rows_list = [t[0] for t in rows]
        rowsLines = "\n".join(rows_list)
        

        await interaction.response.send_message( rowsLines )

        
        
    
    bot.run(TOKEN)


