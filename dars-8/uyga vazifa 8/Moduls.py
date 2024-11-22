import pymysql


def searchdatabase(databasename):
    try:
        conn=pymysql.connect(
            host='localhost',
            user='root',
            password='',
            port=3306
        )
        cursor = conn.cursor()
        cursor.execute('show databases;')
        databases=[row[0] for row in cursor.fetchall()]
        if databasename in databases:
            return True
        else:
            return False
    except:
        print("namadadur xatolik")



class Database:
    def __init__(self):
        self.conn=pymysql.connect(
            host='localhost',
            user='root',
            password='',
            port=3306
        )
        self.cursor = self.conn.cursor()
        print("tarmoqqa ulanildi")


# Ma’lumotlarlar bazasini turli parametrlar asosida yaratuvchi funksiya 
    def createdatabase(self, databasename):
        try:
            self.cursor.execute(f'create database {databasename};')
        except:
            print("Bunday database nomi mavjud!!!")
        self.conn.commit()

# Ma’lumotlarlar bazasida turli parametrlar asosida ustunlar yaratuvchi funksiya 
    def createtable(self, databasename: str, tablename: str, column: str):
        try:
            if searchdatabase(databasename):
                self.cursor.execute(f'use {databasename};')
                query = f'create table {tablename} ({column});'
                self.cursor.execute(query)
                self.conn.commit()
                print("jadval yaratildi")
            else:
                print("Database nomi topilmadi")
        except pymysql.MySQLError as e:
            print(f"Jadval mavjud: {e}")

# Jadval malumotlarini chiqarish
    def describe(self, databasename, tablename):
        try:
            if searchdatabase(databasename):
                self.cursor.execute(f'use {databasename}')
                self.cursor.execute(f'describe {tablename}')

                return self.cursor.fetchall()
            else:
                print("Database nomi topilmadi")
        except pymysql.MySQLError as e:
            print(f'xatolik: {e}')
    
# Malumotlar bazasida jadvalning ustunini o'chiruvchi funksiya
    def reneme_column(self, databasename:str, tablename: str, column_name:str):
        try:
            if searchdatabase(databasename):
                self.cursor.execute(f'use {databasename}')
                self.cursor.execute(f"ALTER TABLE {tablename} DROP COLUMN {column_name}")
                self.conn.commit()
            else:
                print("Database nomi topilmadi")
        except pymysql.MySQLError as a:
            print(f'xatolik: {a}')

# Malumotlar bazasida jadvalga ustun qo'shuvchi funksiya
    def add_column(self, databasename:str, tablename: str, column_name:str):
        try:
            if searchdatabase(databasename):
                self.cursor.execute(f'use {databasename}')
                self.cursor.execute(f"ALTER TABLE {tablename} ADD COLUMN {column_name}")
                self.conn.commit()
            else:
                print("Database nomi topilmadi")
        except pymysql.MySQLError as a:
            print(f'xatolik: {a}')

#Ma’lumotlarlar bazasidan ixtiyoriy jadvalga yangi ma’lumotlarni joylovchi funksiya 
    def insertinto(self, databasename: str, tablename: str, placeholders: tuple):
        try:
            if searchdatabase(databasename):  # Databazani tekshirish
                self.cursor.execute(f'USE {databasename}')
                
                # # Ustun nomlarini olish
                self.info = self.describe(databasename, tablename)
                self.ls = [col[0] for col in self.info]  # Ustun nomlari
                
                # # Ustun nomlarini vergul bilan birlashtirish
                columns = ', '.join(self.ls)  
                
                # # VALUES uchun parametrlar yaratish
                # placeholders = ', '.join(['%s'] * len(values))  
                
                # To'g'ri SQL so'rovi
                query = f"INSERT INTO {tablename} ({columns}) VALUES ({', '.join(['%s'] * len(columns.split(',')))})"
                # SQL so'rovini bajarish
                self.cursor.executemany(query, placeholders)
                self.conn.commit()
                print("Ma'lumotlar muvaffaqiyatli qo'shildi.")
            else:
                print("Database nomi topilmadi")
        except pymysql.MySQLError as e:
            print(f"Bunday id lar mavjud: {e}")

# Ma’lumotlarlar bazasidan ixtiyoriy jadvaldagi ma’lumotlarni o‘chiruvchi funksiya 
    def delete_info(self, databasename: str, tablename: str, conditional:str):
        try:
            if searchdatabase(databasename):
                self.cursor.execute(f'use {databasename}')
                self.cursor.execute(f"DELETE FROM {tablename} WHERE {conditional}")
                self.conn.commit()
                print('Malumot muvaffaqiyatli ochirildi')
            else:
                print("Database nomi topilmadi")
        except pymysql.MySQLError as a:
            print(f'xatolik: {a}')

# Ma’lumotlarlar bazasidan ixtiyoriy jadvaldagi ma’lumotlarni chiqaruvchi funksiya 
    def select_info(self, databasename:str, tablename: str):
        try:
            if searchdatabase(databasename):
                self.cursor.execute(f'use {databasename}')
                self.cursor.execute(f'select * from {tablename}')
                return self.cursor.fetchall()
            else:
                print("Database nomi topilmadi")
        except pymysql.MySQLError as e:
            print(f'xatolik: {e}')

# Ma’lumotlarlar bazasidan ixtiyoriy jadvaldagi ma’lumotlarni qidiruvchi funksiya
    def search_info(self, databasename: str, tablename: str, search_info: str):
        try:
            if searchdatabase(databasename):
                self.cursor.execute(f'use {databasename}')
                self.cursor.execute(f'select * from {tablename} where {search_info}')
                return self.cursor.fetchall()
                
            else:
                print("Database nomi topilmadi")
        except pymysql.MySQLError as e:
            print(f'xatolik: {e}')

# Ma’lumotlarlar bazasidan ixtiyoriy jadvaldagi ma’lumotlarni yangilovchi funksiya
    def update_table(self, databasename:str, conditional:str):
        try:
            if searchdatabase(databasename):
                self.cursor.execute(f'use {databasename}')
                self.cursor.execute(conditional)
                self.conn.commit()
            else:
                print("Database nomi topilmadi")
        except pymysql.MySQLError as e:
            print(f'xatolik: {e}')
    
    def filter(self, databasename:str, conditional:str):
        try:
            if searchdatabase(databasename):
                self.cursor.execute(f'use {databasename}')
                self.cursor.execute(conditional)
                for i in self.cursor.fetchall():
                    print(i)
            else:
                print("Database nomi topilmadi")
        except pymysql.MySQLError as e:
            print(f'xatolik: {e}')



# db=Database()
# db.createdatabase("university")
# db.createtable("university","talaba",'id integer primary key auto_increment, name varchar(20), kursi integer, stipen float')
# db.add_column('university', 'talaba', 'ismi varchar(20)')
# db.describe('university', 'talaba')
# db.reneme_column('university', 'talaba', 'name')

# db.inserinto('university', 'talaba',(2,2,650000,'Abbos'))
# db.delete_info('university','talaba','id=1')
# db.select_info('university', 'talaba')
# print(db.search_info('university', 'talaba','ismi="Davlat"'))
# db.update_table('university', 'talaba', 'update talaba set ismi="Timur" where id=2')