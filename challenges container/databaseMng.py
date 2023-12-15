import csv 
import sqlite3 

def populate_from_csv(db_path , csv_file):

    #establishing connection 
    db_con = sqlite3.connect(db_path)
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

populate_from_csv('C:\\Users\\sts\\Documents\\CODING\\python\\DiscordBot\\main.db' , 'C:\\Users\\sts\\Documents\\CODING\\python\\DiscordBot\\challenges.csv' )