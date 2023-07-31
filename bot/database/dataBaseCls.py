import pymysql.cursors
import os
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv


load_dotenv()

class DataBase:

    '''Class for database management'''
    host = '127.0.0.1'
    passw = 'Bobrdobr12!lisa'
    port = int(os.getenv('PORT'))
    user = os.getenv('USER')
    print(user, host, passw, port)
    def __init__(self):
        self.con = pymysql.connect( # connect to database
            host='127.0.0.1',
            user=self.user,
            password=self.passw,
            port=self.port,
            database='taxipopolambot',
            cursorclass=pymysql.cursors.DictCursor
        )
    

    def check_user_exists(self, user_id: int) -> bool:
        '''Check if user is already in the db'''

        with self.con.cursor() as cur:
            cur.execute("""SELECT `user_id` FROM `users` WHERE `user_id` = %s""", (str(user_id),))
            
            return cur.fetchone() # if result is empty, func will return false


    def get_user_name(self, user_id: int) -> str:
        with self.con.cursor() as cur:
            cur.execute("""SELECT `user_name` FROM `users` WHERE `user_id` = %s""", (str(user_id),))
        return cur.fetchone()['user_name']


    def add_user(self, user_id: int, user_name: str) -> None:
        '''Add user(buyer) in the db'''
        tz = timezone(timedelta(hours=5))
        today = datetime.now(tz)
        with self.con.cursor() as cur:
            cur.execute(
                'INSERT INTO `users` (user_id, user_name, registr_datetime) VALUES(%s, %s, %s)',
                (user_id, user_name, today)
            )
            self.commit()
        return today


    def get_user_id_list(self) -> tuple:
        '''Get list of users tg id for mailing'''
        with self.con.cursor() as cur:
            cur.execute(
                'SELECT `user_id`, `user_name`, `registr_date` FROM `users`'
            )
            return cur.fetchall()
    

    def add_trip(self, user_id, fromDirect, fromPoint, whereDirect, wherePoint, date, time) -> int:
        tz = timezone(timedelta(hours=5))
        today = datetime.now(tz)
        with self.con.cursor() as cur:
            cur.execute(
                '''INSERT INTO `trips` (`user_id`, `date`, `time`, `from_direct`,
`from_point`, `where_direct`, `where_point`, `add_date`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
            (user_id, date, time, fromDirect, fromPoint, whereDirect, wherePoint, today)
            )
            cur.execute('SELECT MAX(`id`) AS id FROM `trips`')
            self.commit()
            return cur.fetchone()['id']
        
    
    def get_passengers(self, user_id, fromDirect, fromPoint, date) -> tuple:
        with self.con.cursor() as cur:
            cur.execute(
                '''SELECT `user_id`, `date`, `time`, `from_direct`,
`from_point`, `where_direct`, `where_point` FROM `trips`
 WHERE `active` = 1 AND `date` = %s AND (`from_direct` = %s AND `from_point` LIKE %s) AND NOT `user_id` = %s
''' ,
            (date, fromDirect, f'{fromPoint.split("*")[0]}*%', user_id)
            )
            return cur.fetchall()
        
    
    def cancel_search_for_pass(self, trip_id) -> None:
        with self.con.cursor() as cur:
            cur.execute(
                '''UPDATE `trips` SET `active` = 0 WHERE `id` = %s''' ,
            (trip_id,)
            )
        self.commit()
    

    def get_all_today_drives(self, date) -> tuple:
        with self.con.cursor() as cur:
            cur.execute(
                '''SELECT `user_id`, `date`, `time`, `from_direct`,
`from_point`, `where_direct`, `where_point`, `active`, `success` FROM `trips`
 WHERE `add_date` LIKE %s''',
            (f'{date}%',)
            )
            fetch = cur.fetchall()
            for user in fetch:
                cur.execute('''SELECT `user_name` FROM `users` WHERE `user_id` = %s''', (user['user_id']))
                user['user_name'] = cur.fetchone()['user_name']
        return fetch


    def check_active_trips(self) -> tuple:
        tz = timezone(timedelta(hours=10))
        now = datetime.now(tz).hour
        with self.con.cursor() as cur:
            cur.execute(
                '''SELECT `user_id`, `id` FROM `trips` WHERE
`time` LIKE %s AND `active` = 1''',
                (f'{now}%',)
            )
            fetch = cur.fetchall()
            cur.execute(
                '''UPDATE `trips` SET `active` = 0 WHERE `active` = 1 AND `time` LIKE %s''',
                (f'{now}%',)
            )
            self.commit()
            return fetch
    

    def set_trip_success(self, trip_id, succes: bool) -> None:
        if succes:
            succes = 1
        else:
            succes = 2
        with self.con.cursor() as cur:
            cur.execute(
                '''UPDATE `trips` SET `success` = %s WHERE `id` = %s''',
                (succes, trip_id)
            )


    def commit(self) -> None:
        '''Saving changes in the db'''

        self.con.commit()
    

    def close_db(self) -> None:
        '''Close connection in the end of bot working'''
        self.con.close()
    