import csv 
import sqlite3 
import aiosqlite
import random
from contextlib import contextmanager
from typing import Final
from crawler import get_recent_submissions , verifiy_existance


@contextmanager
def connection(database):
    connection = sqlite3.connect(database)
    try:
        yield connection
    finally:
        connection.commit()
        connection.close()

PATH:Final = "C:\\Users\\sts\\Documents\\CODING\\python\\DiscordBot\\main.db"

#IMPLEMENT LATER
class DatabaseError(sqlite3.Error):
    message = None

    def __init__(self):
        
        if self.sqlite_errorcode == 1555:
            self.message = "You're already in!"
        else:
            self.message = f"SQLite error with code {self.args}"

        print(f"##################33{self.sqlite_errorcode}#################")
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

def previous_qsts():
    with connection(PATH) as db_con: 
        cursor = db_con.cursor()

        cursor.execute('SELECT id FROM challenges')
        rows = cursor.fetchall()
        #convert tuples into ints 
        id_list = [t[0] for t in rows]


        cursor.close()
        return id_list

def chose_random(query , n:int) :
    
    with connection(PATH) as db_con: 
        cursor = db_con.cursor()

        cursor.execute('SELECT COUNT(*) FROM questions where  ' + query)
        count = cursor.fetchone()[0]
        cursor.execute("select * FROM questions where "+ query)
        rows = cursor.fetchall()
        
        rand_set = set()
        print(len(rows))
        while len(rand_set) !=n : 
            nbr = random.randint(0 , count)
            #check if question already chosen 
            if nbr not in previous_qsts() :
                rand_set.add(nbr)


        cursor.close()
        return rand_set
    
def enrollement(itrc_name , evt):
    try : 
        with connection(PATH) as db_con:
            cursor = db_con.cursor()
            cursor.execute('select * from participant where discord_id = ? ;' , (itrc_name , ) )
            result = cursor.fetchone()
            print(1)
            if result :
                
                cursor.execute("insert into enrollement(participant_id , event_id , score) values(? , ? , 0);" , (result[0] , evt , ))
                
            else :
                
                #cursor.execute("insert into participant(discord_id , username , enrollement_date) values( ? , ? , strftime('%s' , 'now'));" , (itrc_name , itrc_nick ,) )
                #cursor.execute("insert into enrollement(participant_id , event_id , score) values(last_insert_rowid() , ?  , 0);", (evt , ))
                cursor.close()
                raise Exception("you must register yourself first using the `/register` command , then try again")
                
    except sqlite3.Error as e : 
        if e.sqlite_errorcode == 1555:
            raise Exception("You're already in!") from e
        else:
            raise Exception(f"SQLite error with code {e.args[0]}") from e
            
        
def registering(itrc_name , username):
    try : 
        with connection(PATH) as db_con:
            if verifiy_existance(username) : 
                cursor = db_con.cursor()
                cursor.execute("insert into participant(discord_id , username , register_date) values( ? , ? , strftime('%s' , 'now'));" , (itrc_name , username ,) )  
                cursor.close()
            else : 
                raise Exception("make sure that the username is valid :grin: ")
                    
    except sqlite3.Error as e : 
        if e.sqlite_errorcode == 2067:
            raise Exception("You're already registered") from e
        else:
            raise Exception(f"SQLite error with code {e.args[0]}") from e
        
        

def list_challenges_for(evt):
    with connection(PATH) as db_con: 
        cursor = db_con.cursor()

        cursor.execute('select title , titleSlug  from challenges join questions on challenges.id = questions.id where id_event = ? ;' , (evt) )
        rows = cursor.fetchall()
        cursor.close()
        
        
        return rows
    
#this one will be performed periodically   
def populate_submissions():
    with connection(PATH) as db_con: 
        cursor = db_con.cursor()
        # selecting only participants enrollend in an event 
        cursor.execute('select * from enrollement join participant on enrollement.participant_id = participant.id;' )
        rows = cursor.fetchall()
        for row in rows : 
            scraped_challenges = get_recent_submissions(row[5])

            cursor.execute('select titleSlug , challenges.id , challenges.id_event from challenges join questions on challenges.id == questions.id where id_event = ? ;' , ( row[1] ,) )
            challenges_tuples = cursor.fetchall()
            #challenges_slugs = [t[0] for t in challenges] #tuple convertd to list 

            
            print(scraped_challenges)
            #only checks for challenges relevant to the event 
            for scraped_challenge in scraped_challenges : 
                for tuple in challenges_tuples :
                    if scraped_challenge.get('titleSlug') == tuple[0] : 
                        try:
                            cursor.execute("insert into submissions (participant_id , challenge_id , challenge_event_id , completion_time ) values(? , ? ,? , ?) ;" , (row[0] , tuple[1] , tuple[2] , scraped_challenge.get('timestamp') , ))
                        except sqlite3.IntegrityError as e:
                            pass


        
        cursor.close()
        print("submissions populated")
    update_scores()

def update_scores():
    with connection(PATH) as db_con: 
        cursor = db_con.cursor()
        #ONGOING events
        cursor.execute('select participant_id , event_id from enrollement' )
        rows = cursor.fetchall()
        for row in rows :
            cursor.execute('select  CASE WHEN (completion_time - start_date )/3600 < 0 THEN 0 ELSE (completion_time - start_date )/3600 END AS completion_time from submissions join challenges on submissions.challenge_id = challenges.id  where (submissions.participant_id= ?) and (challenges.id_event = ? )  ;' , (row[0] , row[1] ,) )
            delays = cursor.fetchall()
            score = len(delays)
            
            cursor.execute('update enrollement set score = ? where (participant_id = ?) and (event_id = ?) ' , ( score , row[0], row[1],))
        
        cursor.close()
        print("scores updated ")

populate_submissions()
#enrollement("eimen_" , "" , 4)
#query = "difficulty='Easy' and topicTags not like '%Math%'  "
#chose_random(query , 40)
#populate_from_csv( db_con , 'C:\\Users\\sts\\Documents\\CODING\\python\\DiscordBot\\challenges.csv' )
