import discord ,  sandbox , aiosqlite , random ,  os , time , asyncio 
from typing import Final
from discord.ext import commands
from discord import app_commands , Embed
#from databaseMng import chose_random , list_challenges_for , enrollement , registering
from asyncDatabaseMng import DatabaseManager
from uuid import uuid4

PATH:Final = "C:\\Users\\sts\\Documents\\CODING\\python\\DiscordBot\\main.db"
dbmanager = DatabaseManager(PATH)



async def sendPost(bot , details , dbmanager):
    #details contain the server to send to + channel + time of posting
    while True : 

        print("infinit loop ")
        current_time = time.localtime()
        current_hour = current_time.tm_hour
        current_minute = current_time.tm_min
        posting_time = time.localtime(int(details[2]))
        posting_hour = posting_time.tm_hour
        posting_minute = posting_time.tm_min
        

        # Check if the current time matches the target time
        if (current_hour > posting_hour) or (current_hour == posting_hour  and current_minute > posting_minute) :
            print("message to be sent ")
            ## make it send notification to the concerned channel only 
            for server in bot.guilds:
                print(f"server id : {server.id } matching with {details[4]}")
                if server.id == details[4] : 
                    for channel in server.channels :
                        if channel.type.name == 'text' and channel.id == details[5]:
                            
                            await channel.send(f"here's todays challenge : \nhttps://leetcode.com/problems/{details[1]}/description/  \nenjoy! " , suppress_embeds=True)
                            dbmanager.mark_challenge_sent(details[3] , details[6])
        await asyncio.sleep(60)


async def fetch_today_challenges():

    ongoing_evts = await dbmanager.list_ongoing_evts()
    ongoing_evts_ids = [evt[0] for evt in ongoing_evts]
    print(ongoing_evts_ids)
    for evt in ongoing_evts_ids :
        challenges = await dbmanager.list_challenges_for(evt) 
        challenges_list = []
        for challenge in challenges :
            #if the challenge is today and time has passed 
            if (int(challenge[2])//86400 == int(time.time())//86400)  :
                challenges_list.append((challenge[3] , evt , challenge[2]))
        return challenges_list
                

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
            #text_channel_list = []
            synced = await bot.tree.sync() 
            print(f"synced  : {len(synced)} commands")

            #EVERYDAY
            while True : 
                await dbmanager.populate_submissions() 
                today_challs = await fetch_today_challenges()
                print(today_challs)
                for chall in today_challs :     

                                    
                    challenge_details = await dbmanager.get_challenge_details( chall[0] , chall[1] )
                    print(f"challenge_details : {challenge_details}")
                    sendPost(bot , challenge_details , dbmanager)
                await asyncio.sleep(10)
                print('next day')
            

        except Exception as e : 
            print(e.with_traceback())
            



        
        print(f"{bot.user} is running ")
   
   
    #################################### enroll ###################################################
    
    @bot.tree.command(name="enroll")
    @app_commands.describe(evt='enter event id')
    async def enroll( interaction: discord.Interaction , evt:str):
        try : 
            await dbmanager.enrollement(interaction.user.name , evt )
            await interaction.response.send_message(f"{interaction.user.mention } congrats you're in ")
        except Exception as e : 
            await interaction.response.send_message(f"{e.args[0]}")
    #################################### register ###################################################
            

    @bot.tree.command(name="register")
    @app_commands.describe(username='enter leetcode username')
    async def register( interaction: discord.Interaction , username:str):
        try : 

            await dbmanager.registering(interaction.user.name , username )
            await interaction.response.send_message(f"{interaction.user.mention } you're now resigtered in the system !")
        except Exception as e : 
            await interaction.response.send_message(e)



    ####################################### start event ################################################
    @bot.tree.command(name="start_evt")
    @app_commands.describe(event='what is the event about ? ' , start_date = 'when is it starting' , end_date="when it ending "  )
    async def startevt(interaction: discord.Interaction , event:str , start_date:int , end_date:int ):
        try : 
            print(f"was sent from : {interaction.channel.name}")
            
            await interaction.response.send_message("enter search query ")
            query = await bot.wait_for("message", check=lambda msg: msg.author == interaction.user)
            event_id = uuid4().int%1000000
            wherestmt = query.content
            
            # AT AROUND WHAT TIME WOULD YOU LIKE TO RECIEVE THE NOTIFICATION
            await dbmanager.start_evt(event_id , event , start_date , end_date  , wherestmt , interaction.guild_id , interaction.channel_id)
            #fix , when time is above 6pm , start_date = next day
        
            await interaction.followup.send(f" new event started by {interaction.user.nick} , lasts {((end_date-start_date) // 86400)+1 } days \n code : {event_id} (you'll need this to enroll in the event)")

        except Exception as e :

            await interaction.followup.send(f"something went wrong : \n{e} ")

            
    
    
    ####################################### add challenge ################################################
    @bot.tree.command(name="add_challenge")
    @app_commands.describe(chal_id='challenge id' ,evt_id='to which event ?', start_time='when is it starting?')
    async def add_challenge(interaction: discord.Interaction , evt_id:str , chal_id:int , start_time:int):
        
        try :
            await dbmanager.add_challenge( evt_id ,  chal_id , start_time) 


            
        except Exception as e :
            await interaction.response.send_message(e)
        
        
        await interaction.response.send_message("new challenge was added")
        

    ####################################### list_challenges_for ################################################
    @bot.tree.command(name="list_challenges_for")
    @app_commands.describe(evnt_id='get the list of challenges ')
    async def list_challenges(interaction: discord.Interaction , evnt_id:str):
        
        rows = await dbmanager.list_challenges_for(evnt_id)
        rows_list = [t[0] for t in rows if int(time.time())>int(t[2])]

        rows_list =[' ']+rows_list
        rowsLines = "\n• ".join(rows_list)
        

        await interaction.response.send_message( f"past challenges :\n{rowsLines} \n------------------\n this event contains {len(rows)} challenges in total \n the rest will be revealed according to their respective starting time" )
    ####################################### list_ongoing_events ################################################
    @bot.tree.command(name="list_ongoing")
    async def list_ongoing(interaction: discord.Interaction ):
        
        rows = await dbmanager.list_ongoing_evts()
        if len(rows) != 0 :
                
            rows_list = []
            for row in rows :
                rows_list.append(f"event : {row[1]} \nwith code: {row[0]} \n[ from {row[2]} to {row[3]}]\n")
            rowsLines = "\n".join(rows_list)
            await interaction.response.send_message( rowsLines )
        else  :
            await interaction.response.send_message( "there are no ongoin event currently " )
        
        
    
    bot.run(TOKEN)


