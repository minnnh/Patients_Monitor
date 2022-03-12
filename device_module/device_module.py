import logging
import os
import sqlite3
import json

class Device:
    def __init__(self, jsfile):
        logging.basicConfig(format='%(levelname)s - %(message)s')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        f = open(jsfile) # data.json
        self.data = json.loads(f.read())

    def init(self, dbfile):
        # first step is to initialize
        if os.path.exists(dbfile):
            os.remove(dbfile)
        os.system('python table.py')

    def importdb(self, dbfile):
        # get the data of the database
        con = sqlite3.connect(dbfile) # table.db
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM Storage')

        self.user_id_list = []
        self.device_id_list = []

        for row in cur:
            self.user_id_list.append(row['User_id'])
            self.device_id_list.append(row['Device_id'])

    def get_device(self, num):
        int(num)
        self.user_id = self.data[num][0]['User_id']
        self.device_id = self.data[num][1]['Device_id']
        self.role = self.data[num][0]['Roles']

    def check_user_id(self):
        if self.user_id in self.user_id_list:
            self.logger.error("The user id has been recorded.")
        elif not isinstance(self.user_id, int):
            self.logger.error("The format of user id is wrong.")
        else:
            return True

    def check_device_id(self):
        if self.device_id in self.device_id_list:
            self.logger.error("The device id has been recorded.")
        elif not isinstance(self.device_id, int):
            self.logger.error("The format of device id is wrong.")
        else:
            return True   

    def check_role(self):
        roles = ["Patient", "Doctor", "Nurse", "AI_Developer", "Administrator"]
        if self.role not in roles:
            self.logger.error("Your role is not acceptable.")
        else:
            return True

    def create_device(self, dt, dbfile):
        Users = tuple(list(dt[0].values()))
        Devices = tuple(list(dt[1].values()))
        Measurements = tuple(list(dt[2].values()))
        Assignments = tuple(list(dt[3].values()))

        conn = sqlite3.connect(dbfile) # table.db
        cur = conn.cursor()

        sql_statement = 'INSERT INTO Users VALUES (?, ?, ?, ?, ?)'
        cur.executemany(sql_statement, [Users])

        sql_statement = 'INSERT INTO Devices VALUES (?, ?, ?, ?, ?)'
        cur.executemany(sql_statement, [Devices])

        sql_statement = 'INSERT INTO Measurements VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        cur.executemany(sql_statement, [Measurements])
        
        sql_statement = 'INSERT INTO Assignments VALUES (?, ?, ?, ?)'
        cur.executemany(sql_statement, [Assignments])

        cur.execute(f'INSERT INTO Storage VALUES ((SELECT MAX(Premission) + 1 FROM Storage),{self.user_id}, {self.device_id}, "{self.role}")')

        conn.commit()
        conn.close

    def control(self, dbfile):
        self.init(dbfile)

        keys = list(self.data.keys())
        for key in keys:
            self.logger.info(f"number {key}'s data")
            self.importdb(dbfile)

            self.get_device(key)
            a = self.check_user_id()
            b = self.check_device_id()
            c = self.check_role()
            if (a == b == c == True):
                self.create_device(self.data[key],dbfile)
                self.logger.info(f"your information is recorded succesfully\n")

            else:
                self.logger.info(f"The user's information failed to be recorded.\n")
                continue

if __name__ == '__main__':
    dm = Device("data.json") # "data.json"
    dm.control("table.db") # "table.db"
