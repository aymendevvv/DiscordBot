import csv 
import aiosqlite , asyncio
import time 
import random
from contextlib import asynccontextmanager
from typing import Final
from scraper import get_recent_submissions , verify_existance
from validator import Validator

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
        
    async def convert_to_datetime(self , unix): 
        return time.strftime("%d/%m/%Y %H:%M", time.localtime(unix))

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
            

    async def add_challenge(self ,evt_id:str , chal_id:int , start_time:int|None):

        try:
            async with connection(self.database_path) as db_con:

                cursor = await db_con.cursor()
                await cursor.execute(f"select start_date , end_date from event where id ={evt_id}") 
                result:int  = await cursor.fetchone()
                if result :
                    start_date  = result[0] 
                    end_date =  result[1] 
                    
                Validator.validate_add_challenge(start_date , start_time)
                if start_time == None : 
                    #random start time between 12:00 and 20:00 
                    start_time = end_date - (end_date % (24 * 3600)) + (random.randint(43000 , 75000)) + 86400
                    
                    
                    
                await cursor.execute(" insert into challenges ( id , id_event , start_date ) values(? , ? , ? ) ;" , (chal_id , evt_id , start_time + random.randint(-3500 , 3500) , )) 
                
                if start_time > end_date :
                    await cursor.execute("update event set end_date = ? where id = ?", (start_time + 3600 , evt_id ,)) 
                    return f"event end date updated : {await self.convert_to_datetime(start_time + 3600)}"
                else : 
                    return None 

        except aiosqlite.Error as e:
                raise Exception() from e
    
    async def start_evt(self ,evt_id:str, evt_name , start_date:int , end_date:int, wherestmt:str , guild_id:int , channel_id:int , notif_time:int):
        
                
        try:
            async with connection(self.database_path) as db_con:

                
                
                h = time.localtime().tm_hour ; 
                if notif_time < h + 1  :
                    start_date += 86400 
                Validator.validate_start_evt(event=evt_name, end_date= end_date, start_date=start_date,notif_time= notif_time)
                
                cursor = await db_con.cursor()
                await cursor.execute(" insert into event ( id  , name , start_date , end_date , guild_id , channel_id) values( ? , ? , ? , ? , ?,?) ;" , ( str(evt_id) , evt_name , start_date,(end_date +4500) ,guild_id , channel_id , )) 
                
                ajusted_start_date = start_date - (start_date % (24 * 3600)) + (notif_time * 3600)
                starting = ajusted_start_date ; 
                qst_set = await self.chose_random(wherestmt)
                

                days = (end_date-start_date)/86400
                
                #instead of importing math.ceil()
                days = int((-(-days // 1) ) + 1 )
                
                if days > len(qst_set) : 
                    raise ValueError(f"not enough questions try another query")
                else :
                    qst_list = random.sample(qst_set , days)
                    for qst_id in qst_list : 
                        await cursor.execute(" insert into challenges ( id , id_event , start_date ) values(? , ? , ? ) ;" , (qst_id , evt_id , ajusted_start_date + random.randint(-3500 , 3500) , )) 
                        ajusted_start_date += 86400  
                        
                return f"\n first challenge starts at around  { await self.convert_to_datetime(starting)} \n the event lasts : {days} days "
                        
                

        except aiosqlite.Error as e:
                raise Exception() from e
            
    async def delete_evt(self , evt_id:int):
        
                
        try:
            async with connection(self.database_path) as db_con:
                
                cursor = await db_con.cursor()
                await cursor.execute(" delete from event where id = ? ;" , (evt_id ,)) 
                

        except aiosqlite.Error as e:
                raise Exception() from e
            
            
    async def registering(self, itrc_name, username , nick):
        try:
            async with connection(self.database_path) as db_con:
                if verify_existance(username):
                    cursor = await db_con.cursor()
                    await cursor.execute("insert into participant(discord_id , username , register_date , nick) values( ? , ? , strftime('%s' , 'now') , ?);", (itrc_name, username,nick,))
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
        
    async def get_event_details(self, id_evt) :
        async with connection(self.database_path) as db_con:
            cursor = await db_con.cursor()

            await cursor.execute("select * from event where id = ?", (id_evt ,))
            details = await cursor.fetchone()
            
            await cursor.close()
            
            return f"Event : {details[1]} \n starts : {await self.convert_to_datetime(details[2])} \n ends : {await self.convert_to_datetime(details[3])}"
        
    async def mark_challenge_sent(self,id , id_evt)  :

        async with connection(self.database_path) as db_con:
            cursor = await db_con.cursor()

            await cursor.execute(f" UPDATE challenges SET post_sent = 1 WHERE challenges.id = ? AND challenges.id_event = ? ; ", (id , id_evt,))
            await cursor.close()
            print("challenge updated")
            

    async def list_challenges_for(self, evt):
        #validate :evt code exists
        async with connection(self.database_path) as db_con:
            cursor = await db_con.cursor()

            await cursor.execute("select title, titleSlug , start_date , challenges.id , post_sent from challenges join questions on challenges.id = questions.id where id_event = ? and challenges.post_sent != 1;", (evt,))
            rows = await cursor.fetchall()
            await cursor.close()
            
            return rows
    async def get_leaderboard(self, evt_id):
        #validate :evt code exists
        async with connection(self.database_path) as db_con:
            cursor = await db_con.cursor()

            await cursor.execute("select  participant.nick , enrollement.score from enrollement join event on enrollement.event_id = event.id join participant on participant.id = enrollement.participant_id where strftime('%s' , 'now') < event.end_date and event.id = ? ORDER BY enrollement.score DESC ; ", (evt_id,))
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

    async def calculate_streaks(self , user_id) :
        async with connection(self.database_path) as db_con:
            cursor = await db_con.cursor()
            await cursor.execute("select * from submissions where participant_id = ? ORDER BY  completion_time DESC ; " , (user_id,))
            submissions = await cursor.fetchall()
            print("subs : {}".format(submissions))
            streaks = []
            streak = 1
            for i in range(1 , len(submissions)) :
                
                #its counted as a streak if the interval between two challenges is less than 24H and more than 5h
                
                
                if 18000 < int(submissions[i-1][4]) - int(submissions[i][4]) < 86400 :
                    streak += 1
                else :
                    streaks.append(streak)
                    streak = 1
                    
                    
            streaks.append(streak)
                    
            return streaks
    async def get_stats(self , username ) :
        async with connection(self.database_path) as db_con:
            cursor = await db_con.cursor()
            await cursor.execute("select * from participant where discord_id = ? ; " , (username,))
            id = await cursor.fetchone()
            print(id[0])
            id = id[0]
            
            
            await cursor.execute("select event.name , enrollement.score from enrollement join event on event.id = enrollement.event_id where strftime('%s', 'now')< end_date  and enrollement.participant_id = ? ; " , (id,))
            active_enrollemnts = await cursor.fetchall()
            print(active_enrollemnts)
            
            await cursor.execute("select event.name , enrollement.score from enrollement join event on event.id = enrollement.event_id where strftime('%s', 'now') > end_date  and enrollement.participant_id = ? ; " , (id,))
            previous_enrollemnts = await cursor.fetchall()
            print(previous_enrollemnts)
            
            await cursor.execute("select count(*) from submissions where participant_id = ? ; " , (id,))
            nbrChallenges = await cursor.fetchone()
            nbrChallenges = nbrChallenges[0]
            
            await cursor.execute("select register_date from participant where id = ? ; " , (id,))
            joinDate = await cursor.fetchone()
            joinDate = await self.convert_to_datetime(joinDate[0])
            print(joinDate)
            
            longest_streak = max(await self.calculate_streaks(id))
            
            return active_enrollemnts , previous_enrollemnts , nbrChallenges , joinDate , longest_streak
            
            
        
    async def update_scores(self , cur):

        async with connection(self.database_path) as db_con:
            
            #maybe the update_scores function and populate_submissions should be part of one big function
            cursor = cur
            
            #select the ongoing evetns
            events = await self.list_ongoing_evts()
            
            for event in events  :
                
                #get the participants of that event and initialize scores to 0
                await cursor.execute("select * from enrollement where event_id = ? ; " , (event[0],))
                participants = await cursor.fetchall()
                participants_dict = {participant[0]: 0 for participant in participants}
                #get the challenges of that event
                await cursor.execute("select * from challenges where id_event = ? ; " , (event[0],))
                challenges = await cursor.fetchall()
                
                
                for challenge in challenges :
                    await cursor.execute("select * from submissions where challenge_event_id = ? and challenge_id = ? ORDER BY  completion_time ASC ; " , (event[0],challenge[0],))
                    submissions_ordered = await cursor.fetchall()
                    print(submissions_ordered)
                    
                    for i , submission in enumerate(submissions_ordered) :
                        #score based on the submission date
                        if i == 0 :
                            participants_dict[submission[1]] += 10
                        elif i == 1  :
                            participants_dict[submission[1]] += 8
                        elif i == 2  :
                            participants_dict[submission[1]] += 6
                        else :
                            participants_dict[submission[1]] += 4
                        
                        print(f"streaks for {submission[1]} : {await self.calculate_streaks(submission[1])}")
                    
                
                for paraticipant  in participants_dict :
                    await cursor.execute('update enrollement set score = ? where (participant_id = ?) and (event_id = ?);', (participants_dict[paraticipant], paraticipant, event[0]))
                    
            
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

                #keep only the challenges after the event starting date
                relevant_challenges = [chlg  for chlg in scraped_challenges if int(chlg['timestamp']) >= int(enrollement[2]) ] # remove all challenges done before the start of the event 

                
                print(f"ongoin : {ongoing_challenges} \nrelevant  : {relevant_challenges}")
                #print(scraped_challenges)

            
                for ongoing_challenge in ongoing_challenges:
                    
                    for challenge in relevant_challenges :
                        if ongoing_challenge[0] == challenge.get('titleSlug') :
                            try:
                                await cursor.execute("insert into submissions (participant_id, challenge_id, challenge_event_id, completion_time) values(?, ?, ?, ?);", (enrollement[3], ongoing_challenge[1], ongoing_challenge[2], challenge.get('timestamp')))
                                print(f"inserted {enrollement[0]} {ongoing_challenge[0]}")
                                break
                            except aiosqlite.IntegrityError :
                                continue
                    
                                
                    

            print("submissions refreshed")
            await self.update_scores(cursor)
    



    #populate_submissions()
    #enrollement("eimen_" , "" , 4)
    #query = "difficulty='Easy' and topicTags not like '%Math%'  "
    #chose_random(query , 40)
    #populate_from_csv( db_con , 'C:\\Users\\sts\\Documents\\CODING\\python\\DiscordBot\\challenges.csv' )
