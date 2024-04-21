import aiomysql
from env_data import db_name, db_user, db_password
import logging


class DataBase:
    def __init__(self):
        self.host = "localhost"
        self.user = db_user
        self.password = db_password
        self.name = db_name
        self.connection = None

    async def connect_to_db(self):
        try:
            self.connection = await aiomysql.connect(
                host='localhost',
                user=self.user,
                password=self.password,
                db=self.name,
                autocommit=True,
                local_infile=True,
                init_command="SET sql_mode = 'NO_ENGINE_SUBSTITUTION'"
            )
        except aiomysql.MySQLError as e:
            logging.log(logging.ERROR, "Can't connect to mysql database")

    # execute SQL code without output
    async def execute_sql(self, sql, args=None):
        async with self.connection.cursor() as cursor:
            if args is not None:
                await cursor.execute(sql, args)
            else:
                await cursor.execute(sql)

    # execute SQL code with output
    async def fetch_sql(self, sql, args=None):
        async with self.connection.cursor() as cursor:
            if args is not None:
                await cursor.execute(sql, args)
                return await cursor.fetchall()
            else:
                await cursor.execute(sql)
                return await cursor.fetchall()

    async def close_connection(self):
        if self.connection is not None:
            self.connection.close()

    async def show_modules_by_id(self, user_id):
        sql = f"SELECT * FROM Modules WHERE user_id={user_id}"
        modules = await self.fetch_sql(sql)
        cleaned_modules = []
        for module in modules:
            module_dict = {
                "id": module[0],
                "name": module[2]
            }
            if module[3] is not None:
                module_dict["description"] = module[3]
            cleaned_modules.append(module_dict)
        if len(cleaned_modules) > 0:
            return cleaned_modules
        return None

    @staticmethod
    async def write_txt_file(file):
        pass

    @staticmethod
    async def write_xlsx_file(file):
        pass

