import csv 
import aiosqlite , asyncio
import random
from contextlib import asynccontextmanager
from typing import Final
from crawler import get_recent_submissions , verifiy_existance
from validator import *

@asynccontextmanager
async def connection(database) :
    connection = await aiosqlite.connect(database)
    try:
        yield connection
    finally:
        await connection.commit()
        await connection.close()


class DatabaseManager:

    def __init__(self, database_path):
        self.database_path = database_path

    
    #used it once brk
    def populate_from_csv(db_con , csv_file):

        #establishing connection 
        
        cursor = db_con.cursor() 

        with open(csv_file , 'r' , newline='' , encoding='utf-8') as csv_file : 
            reader = csv.DictReader(csv_file) 
            for row in reader:
                is_favor = 1 if row['isFavor'].lower() == 'true' else 0
                paid_only = 1 if row['paidOnly'].lower() == 'true' else 0
                has_solution = 1 if row['hasSolution'].lower() == 'true' else 0
                has_video_solution = 1 if row['hasVideoSolution'].lower() == 'true' else 0

                cursor.execute('''
                    INSERT INTO questions (
                        acRate,
                        difficulty,
                        frontendQuestionId,
                        isFavor,
                        paidOnly,
                        title,
                        titleSlug,
                        hasSolution,
                        hasVideoSolution,
                        topicTags
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    float(row['acRate']),
                    row['difficulty'],
                    int(row['frontendQuestionId']),
                    is_favor,
                    paid_only,
                    row['title'],
                    row['titleSlug'],
                    has_solution,
                    has_video_solution,
                    row['topicTags']
                ))

        db_con.commit()
        db_con.close()

    async def previous_qsts(self):
        async with connection(self.database_path) as db_con: 
            cursor = await db_con.cursor()

            await cursor.execute('SELECT id FROM challenges')
            rows = await cursor.fetchall()
            # Convert tuples into ints 
            id_list = [t[0] for t in rows]

            await cursor.close()
            return id_list

    async def chose_random(self , query):
        async with connection(self.database_path) as db_con:
            cursor = await db_con.cursor()
            # something to worry abt later
            # system will run out of unrepeated questions eventually 

            await cursor.execute(f"select * from questions Left join challenges on challenges.id=questions.id  where { query } and challenges.id is null ")
            rows = await cursor.fetchall()
            rand_ids = [row[0] for row in rows] 
            await cursor.close()
            print(rand_ids)

            return rand_ids
        

    async def enrollement(self ,itrc_name, evt):
        try:
            async with connection(self.database_path) as db_con:
                cursor = await db_con.cursor()
                await cursor.execute('select * from participant where discord_id = ? ;', (itrc_name,))
                result = await cursor.fetchone()
                if result:
                    await cursor.execute("insert into enrollement(participant_id , event_id , score) values(? , ? , 0);", (result[0], evt,))
                else:
                    await cursor.close()
                    raise Exception("You must register yourself first using the `/register` command, then try again")

        except aiosqlite.Error as e:
            if e.sqlite_errorcode == 1555:  
                raise Exception("You're already in!") from e
            else:
                raise Exception(f"SQLite error with code {e.code}") from e
            

    async def add_challenge(self ,evt_id:str , chal_id:int , start_time:int):

        try:
            async with connection(self.database_path) as db_con:

                cursor = await db_con.cursor()
                await cursor.execute(f"select start_date , end_date from event where id ={evt_id}") 
                result:int  = await cursor.fetchone()
                if result :
                    start_date  = result[0] 
                    end_date =  result[1] 
                    
                validate_add_challenge(start_date , start_time)
                    
                await cursor.execute(" insert into challenges ( id , id_event , start_date ) values(? , ? , ? ) ;" , (chal_id , evt_id , start_time + random.randint(-3500 , 3500) , )) 
                if start_time > end_date :
                    sixpm = start_time - (start_time % (24 * 3600)) + (18 * 3600)
                    await cursor.execute("update event set end_date = ? where id = ?", (sixpm + 3600 , evt_id ,)) 
                    print(f"new end date : {sixpm} ")

        except aiosqlite.Error as e:
                raise Exception() from e
    
    async def start_evt(self ,evt_id:str, evt_name , start_date:int , end_date:int, wherestmt:str , guild_id:int , channel_id:int):
        
                
        try:
            async with connection(self.database_path) as db_con:

                cursor = await db_con.cursor()
                await cursor.execute(" insert into event ( id  , name , start_date , end_date , guild_id , channel_id) values( ? , ? , ? , ? , ?,?) ;" , ( str(evt_id) , evt_name , start_date,end_date ,guild_id , channel_id , )) 
                
                #is set to six pm , change 18 to anything else if you want another time
                sixpm = start_date - (start_date % (24 * 3600)) + (18 * 3600)
                qst_set = await self.chose_random(wherestmt)

                days = (end_date-start_date)//86400
                if days > len(qst_set) : 
                    raise ValueError(f"not enough questions try another query")
                else :
                    qst_list = random.sample(qst_set , days)
                    for qst_id in qst_list : 
                        sixpm += 86400  
                        await cursor.execute(" insert into challenges ( id , id_event , start_date ) values(? , ? , ? ) ;" , (qst_id , evt_id , sixpm + random.randint(-3500 , 3500) , )) 
                        
                

        except aiosqlite.Error as e:
                raise Exception() from e
            
            
    async def registering(self, itrc_name, username):
        try:
            async with connection(self.database_path) as db_con:
                if verifiy_existance(username):
                    cursor = await db_con.cursor()
                    await cursor.execute("insert into participant(discord_id , username , register_date) values( ? , ? , strftime('%s' , 'now'));", (itrc_name, username,))
                    await cursor.close()
                else:
                    raise Exception("Make sure that the username is valid 😁")

        except aiosqlite.Error as e:
            if e.sqlite_errorcode == 2067:  
                raise Exception("You're already registered") from e
            else:
                raise Exception(f"SQLite error with code {e.code}") from e
    
    async def get_challenge_details(self, id , id_evt) :
        async with connection(self.database_path) as db_con:
            cursor = await db_con.cursor()

            await cursor.execute("select title, titleSlug , challenges.start_date , challenges.id , guild_id , channel_id , challenges.id_event from challenges join questions on challenges.id = questions.id join event on event.id = challenges.id_event  where id_event = ? and challenges.id = ? ;", (id_evt,id ,))
            challenge = await cursor.fetchone()
            await cursor.close()
            
            return challenge
        
    async def mark_challenge_sent(self,id , id_evt)  :

        async with connection(self.database_path) as db_con:
            cursor = await db_con.cursor()

            await cursor.execute(f" UPDATE challenges SET done = 2 WHERE challenges.id = {id} AND challenges.id_event = {id_evt} ; ", (id , id_evt,))
            await cursor.close()
            print("challenge updated")
            

    async def list_challenges_for(self, evt):
        #validate :evt code exists
        async with connection(self.database_path) as db_con:
            cursor = await db_con.cursor()

            await cursor.execute("select title, titleSlug , start_date , challenges.id from challenges join questions on challenges.id = questions.id where id_event = ? and challenges.done != 1;", (evt,))
            rows = await cursor.fetchall()
            await cursor.close()
            
            return rows

    async def list_ongoing_evts(self):
    
        async with connection(self.database_path) as db_con:
            cursor = await db_con.cursor()

            await cursor.execute("select id , name , date(start_date, 'unixepoch') , date(end_date, 'unixepoch')  from event where strftime('%s', 'now')< end_date ; ")
            rows = await cursor.fetchall()
            await cursor.close()
            
            return rows

    async def update_scores(self , cur):

        async with connection(self.database_path) as db_con:
            cursor = cur
            
            await cursor.execute('select participant_id, event_id from enrollement;')
            rows = await cursor.fetchall()
            
            for row in rows:
                await cursor.execute('select CASE WHEN (completion_time - start_date) / 3600 < 0 THEN 0 ELSE (completion_time - start_date) / 3600 END AS completion_time from submissions join challenges on submissions.challenge_id = challenges.id where (submissions.participant_id= ?) and (challenges.id_event = ? )  ;', (row[0], row[1],))
                delays = await cursor.fetchall()
                score = len(delays)
                
                await cursor.execute('update enrollement set score = ? where (participant_id = ?) and (event_id = ?);', (score, row[0], row[1]))
            
            await cursor.close()
            print("scores updated")

    # Modified populate_submissions() function
    async def populate_submissions(self):
        async with connection(self.database_path) as db_con:
            cursor = await db_con.cursor()
            #ongoing enrollements  :
            await cursor.execute("select username , event.id , start_date , participant.id  from enrollement join participant on enrollement.participant_id = participant.id join event on event.id = enrollement.event_id  where  strftime('%s', 'now') < end_date  ;")
            enrollements = await cursor.fetchall()
            #for every user that is in an ongoing event 
            for enrollement in enrollements : 

                scraped_challenges = get_recent_submissions(enrollement[0]) #returns a list of dictionaries based on leetcode username
                print(f"participant {enrollement[0]}")

                await cursor.execute("select titleSlug, challenges.id, challenges.id_event , event.start_date from challenges join questions on challenges.id == questions.id join event on event.id==challenges.id_event where  strftime('%s', 'now') < end_date and event.id = ?  ;" , (enrollement[1],))
                ongoing_challenges = await cursor.fetchall()

                #keep only the challenges after the event started 
                cleaned_challenges = [chlg  for chlg in scraped_challenges if int(chlg['timestamp']) >= int(enrollement[2]) ] # remove all challenges done before the start of the event 

                
                print(f"scraped : {len(scraped_challenges)} , left : {len(cleaned_challenges)}")
                print(scraped_challenges)

                match_found = False
                i = 0

                #match the two sets 
                #use while loop to find the element with the earliest timestamp
                while not match_found : 

                    for ongoing_challenge in ongoing_challenges:
                        if scraped_challenges[i].get('titleSlug') == ongoing_challenge[0]:
                            match_found = True
                            try:
                                await cursor.execute("insert into submissions (participant_id, challenge_id, challenge_event_id, completion_time) values(?, ?, ?, ?);", (enrollement[3], ongoing_challenge[1], ongoing_challenge[2], scraped_challenges[i].get('timestamp')))
                                break
                            except aiosqlite.IntegrityError as e:
                                print(e)
                                continue
                                pass
                            
                    if match_found :
                        break

            print("submissions refreshed")
            await self.update_scores(cursor)



    #populate_submissions()
    #enrollement("eimen_" , "" , 4)
    #query = "difficulty='Easy' and topicTags not like '%Math%'  "
    #chose_random(query , 40)
    #populate_from_csv( db_con , 'C:\\Users\\sts\\Documents\\CODING\\python\\DiscordBot\\challenges.csv' )
