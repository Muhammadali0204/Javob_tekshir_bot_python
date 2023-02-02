import sqlite3


class Database:
    def __init__(self, path_to_db="data/Users.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        # connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data


    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())
    
    
    
    # Users
    

    def add_user(self, user_id, name : str, username : str, status, kanal): # this
        sql = """
        INSERT INTO Users(user_id, name, username, status, kanal) VALUES(?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(user_id, name, username, status, kanal), commit=True)

    def select_all_users(self): # this
        sql = """
        SELECT * FROM Users WHERE user_id > 100
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)
    
    def select_user_id(self, id): # this
        sql = f"""
        SELECT * FROM Users WHERE user_id = ?
        """
        return self.execute(sql = sql, parameters=(id,), fetchone=True)
    
    def kanallar(self):
        return self.execute(sql="SELECT username FROM Users WHERE user_id = 2", fetchone=True)
    
    def count_users(self): # this
        return self.execute("SELECT COUNT(*) FROM Users WHERE user_id > 100", fetchone=True)

    def update_user_name(self, id, ism): # this
        self.execute("UPDATE Users SET name = ? WHERE user_id = ?", parameters=(ism,id), commit=True)

    def select_limits_oddiy(self): #this
        return self.execute("SELECT * FROM Users WHERE user_id = 3", fetchone=True)
    
    def select_limits_blok(self): #this
        return self.execute("SELECT * FROM Users WHERE user_id = 4", fetchone=True)
    
    def take_test_kodi(self): # this
        data = self.execute("SELECT Username FROM Users WHERE user_id = ?", parameters=(1,), fetchone=True)
        new_code = int(data[0]) + 1
        self.execute("UPDATE Users SET username = ? WHERE user_id = 1", parameters=(str(new_code),), commit=True)
        return data[0]
    def select_test_kodi(self): # this
        data = self.execute("SELECT Username FROM Users WHERE user_id = ?", parameters=(1,), fetchone=True)
        return data[0]
    
    
    
# Tuzilgan savollar


    
    def add_test_oddiy(self, user_id, test_kodi, fan_nomi, javoblar : str, avto_vaqt, faollik, avto_post): # this
        sql = """
        INSERT INTO Oddiy_test(user_id, test_kodi, fan_nomi, javoblar, avto_vaqt, faollik, avto_post) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        self.execute(sql=sql, parameters=(user_id, test_kodi, fan_nomi, javoblar, avto_vaqt, faollik, avto_post), commit=True)
        
    def add_test_blok(self, user_id, test_kodi, fan_nomi, javoblar, beriladigan_ballar, avto_vaqt, faollik, avto_post):
        sql = """
        INSERT INTO Blok_test(user_id, test_kodi, fan_nomi, javoblar, beriladigan_ballar, avto_vaqt, faollik, avto_post) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(sql=sql, parameters=(user_id, test_kodi, fan_nomi, javoblar, beriladigan_ballar, avto_vaqt, faollik, avto_post), commit=True)
        
        
    def select_test_oddiy_by_test_kodi(self, test_kodi):
        sql = """
        SELECT * FROM Oddiy_test WHERE test_kodi = ?
        """
        
        return self.execute(sql=sql, parameters=(test_kodi,), fetchone=True)
    
    def select_test_blok_by_test_kodi(self, test_kodi):
        sql = """
        SELECT * FROM Blok_test WHERE test_kodi = ?
        """
        
        return self.execute(sql=sql, parameters=(test_kodi,), fetchone=True)
    
    def update_test_post(self, test_turi, test_kodi):
        sql = f" UPDATE {test_turi} SET avto_post = 1 WHERE test_kodi = ?"
        self.execute(sql=sql, parameters=(test_kodi,), commit=True)
        
    def all_tests_oddiy_sana(self):
        return self.execute(sql="SELECT * FROM Oddiy_test WHERE avto_vaqt LIKE '%.%' ", fetchall=True)
    def all_tests_blok_sana(self):
        return self.execute(sql="SELECT * FROM Blok_test WHERE avto_vaqt LIKE '%.%' ", fetchall=True)

# Berilgan javoblar

    def javob_berganmi_oddiy(self, test_kodi, user_id):
        sql = "SELECT * FROM Oddiy_test WHERE test_kodi = ? AND user_id = ?"
        return self.execute(sql, parameters=(test_kodi, user_id), fetchone=True)
    def javob_berganmi_blok(self, test_kodi, user_id):
        sql = "SELECT * FROM Blok_test WHERE test_kodi = ? AND user_id = ?"
        return self.execute(sql, parameters=(test_kodi, user_id), fetchone=True)
    def add_javob_oddiy(self, id, kod, tuplagan_bal, xato_javoblari):
        sql = "INSERT INTO Oddiy_test(user_id, test_kodi, jami_bali, xato_javoblar) VALUES (?, ?, ?, ?)"
        self.execute(sql, parameters=(id, kod, tuplagan_bal, xato_javoblari), commit=True)
    
    def add_javob_blok(self, id, kod, tuplagan_bal, xato_javoblari, jami):
        sql = "INSERT INTO Blok_test(user_id, test_kodi, bali, xato_javoblar, jami_bali) VALUES (?, ?, ?, ?, ?)"
        self.execute(sql, parameters=(id, kod, tuplagan_bal, xato_javoblari, jami), commit=True) 
        
    def select_all_javob_berganlar_by_test_kodi(self, test_kodi):
        sql = "SELECT * FROM Oddiy_test WHERE test_kodi = ?"
        oddiy_testga_javoblar = self.execute(sql=sql, parameters=(test_kodi,), fetchall=True)
        if oddiy_testga_javoblar == []:
            sql = "SELECT * FROM Blok_test WHERE test_kodi = ?"
            blok_testga_javoblar = self.execute(sql=sql, parameters=(test_kodi,), fetchall=True)
            return blok_testga_javoblar
        else:
            return oddiy_testga_javoblar
        
    def select_all_javob_berganlar_tartiblangan_oddiy(self):
        sql = "SELECT * FROM Oddiy_test ORDER BY jami_bali DESC"
        return self.execute(sql=sql, fetchall=True)
    
    def delete_answers_oddiy_by_test_kodi(self, test_kodi):
        sql = "DELETE FROM Oddiy_test WHERE test_kodi = ?"
        self.execute(sql, parameters=(test_kodi,), commit=True)
        
        
    def select_all_javob_berganlar_tartiblangan_blok(self):
        sql = "SELECT * FROM Blok_test ORDER BY jami_bali DESC"
        return self.execute(sql=sql, fetchall=True)
        
    def delete_answers_blok_by_test_kodi(self, test_kodi):
        sql = "DELETE FROM Blok_test WHERE test_kodi = ?"
        self.execute(sql, parameters=(test_kodi,), commit=True)
    
    








# def logger(statement):
#     print(f"""
# _____________________________________________________        
# Executing: 
# {statement}
# _____________________________________________________
# """)