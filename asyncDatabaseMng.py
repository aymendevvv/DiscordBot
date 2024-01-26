import csv 
import aiosqlite
import random
from contextlib import asynccontextmanager
from typing import Final
from crawler import get_recent_submissions , verifiy_existance


@asynccontextmanager
async def connection(database) :
    connection = await aiosqlite.connect(database)
    try:
        yield connection
    finally:
        await connection.commit()
        await connection.close()

PATH:Final = "C:\\Users\\sts\\Documents\\CODING\\python\\DiscordBot\\main.db"

#IMPLEMENT LATER
class DatabaseError(aiosqlite.Error):
    message = None

    def __init__(self):
        
        if self.sqlite_errorcode == 1555:
            self.message = "You're already in!"
        else:
            self.message = f"SQLite error with code {self.args}"
            print(f"##################{self.sqlite_errorcode}#################")
            
        super().__init__(self)
    

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

    # Commit the changes and close the connection
    db_con.commit()
    db_con.close()

async def previous_qsts():
    async with connection(PATH) as db_con: 
        cursor = await db_con.cursor()

        await cursor.execute('SELECT id FROM challenges')
        rows = await cursor.fetchall()
        # Convert tuples into ints 
        id_list = [t[0] for t in rows]

        await cursor.close()
        return id_list

async def chose_random(query, n: int):
    async with connection(PATH) as db_con:
        cursor = await db_con.cursor()

        await cursor.execute('SELECT COUNT(*) FROM questions where ' + query)
        count = (await cursor.fetchone())[0]
        await cursor.execute("select * FROM questions where " + query)
        rows = await cursor.fetchall()

        rand_set = set()
        print(len(rows))
        while len(rand_set) != n:
            nbr = random.randint(0, count)
            # check if question already chosen 
            # change later to a sql join query 
            
            if nbr not in await previous_qsts():
                rand_set.add(nbr)

        await cursor.close()
        return rand_set
async def enrollement(itrc_name, evt):
    try:
        async with connection(PATH) as db_con:
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
          
        
async def registering(itrc_name, username):
    try:
        async with connection(PATH) as db_con:
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
  
        

async def list_challenges_for(evt):
    async with connection(PATH) as db_con:
        cursor = await db_con.cursor()

        await cursor.execute('select title, titleSlug from challenges join questions on challenges.id = questions.id where id_event = ? ;', (evt,))
        rows = await cursor.fetchall()
        await cursor.close()
        
        return rows

async def list_ongoing_evts():
    async with connection(PATH) as db_con:
        cursor = await db_con.cursor()

        await cursor.execute("select id , name , date(start_date, 'unixepoch') , date(end_date, 'unixepoch')  from event ; ")
        rows = await cursor.fetchall()
        await cursor.close()
        
        return rows

# Modified populate_submissions() function
async def populate_submissions():
    async with connection(PATH) as db_con:
        cursor = await db_con.cursor()
        await cursor.execute('select * from enrollement join participant on enrollement.participant_id = participant.id;')
        rows = await cursor.fetchall()
        
        for row in rows:
            scraped_challenges = get_recent_submissions(row[5])

            await cursor.execute('select titleSlug, challenges.id, challenges.id_event from challenges join questions on challenges.id == questions.id where id_event = ? ;', (row[1],))
            challenges_tuples = await cursor.fetchall()
            
            for scraped_challenge in scraped_challenges:
                for tuple in challenges_tuples:
                    if scraped_challenge.get('titleSlug') == tuple[0]:
                        try:
                            await cursor.execute("insert into submissions (participant_id, challenge_id, challenge_event_id, completion_time) values(?, ?, ?, ?);", (row[0], tuple[1], tuple[2], scraped_challenge.get('timestamp')))
                        except aiosqlite.IntegrityError as e:
                            pass

        await cursor.close()
        print("submissions populated")
        await update_scores()

async def update_scores():
    async with connection(PATH) as db_con:
        cursor = await db_con.cursor()
        
        cursor.execute('select participant_id, event_id from enrollement;')
        rows = await cursor.fetchall()
        
        for row in rows:
            await cursor.execute('select CASE WHEN (completion_time - start_date) / 3600 < 0 THEN 0 ELSE (completion_time - start_date) / 3600 END AS completion_time from submissions join challenges on submissions.challenge_id = challenges.id where (submissions.participant_id= ?) and (challenges.id_event = ? )  ;', (row[0], row[1],))
            delays = await cursor.fetchall()
            score = len(delays)
            
            await cursor.execute('update enrollement set score = ? where (participant_id = ?) and (event_id = ?);', (score, row[0], row[1]))
        
        await cursor.close()
        print("scores updated")
    
#populate_submissions()
#enrollement("eimen_" , "" , 4)
#query = "difficulty='Easy' and topicTags not like '%Math%'  "
#chose_random(query , 40)
#populate_from_csv( db_con , 'C:\\Users\\sts\\Documents\\CODING\\python\\DiscordBot\\challenges.csv' )
