import sqlite3


class SQLiteManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def delete_data(self, table_name, condition=None):
        try:
            select_query = f"DELETE FROM {table_name}"
            if condition:
                select_query += f" WHERE {condition}"
            self.cursor.execute(select_query)
            self.connection.commit()
        except Exception as e:
            print(f"Error selecting data: {e}")
            return None

    def create_table(self, table_name, columns):
        try:
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print(f"Table '{table_name}' created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")

    def insert_data(self, table_name, data, columns=None, user_id=False):
        if columns is None:
            columns = []
        try:
            if columns:
                # If columns are specified, exclude the auto-incrementing column
                columns = ', '.join(columns)
                placeholders = ', '.join(['?' for _ in range(len(data))])
                insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            else:
                # If columns are not specified, assume auto-incrementing column is present
                placeholders = ', '.join(['?' for _ in range(len(data))])
                insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"

            self.cursor.execute(insert_query, data)
            self.connection.commit()
            print("Data inserted successfully.")
            if user_id:
                user_id = db.select_data('users')[0][0]
                return user_id
            return True
        except Exception as e:
            print(f"Error inserting data: {e}")

    def select_data(self, table_name, condition=None):
        try:
            select_query = f"SELECT * FROM {table_name}"
            if condition:
                select_query += f" WHERE {condition}"
            self.cursor.execute(select_query)
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            print(f"Error selecting data: {e}")
            return None

    def update_data(self, table_name, column_to_update, new_value, condition=None):
        try:
            update_query = f"UPDATE {table_name} SET {column_to_update} = ?"
            if condition:
                update_query += f" WHERE {condition}"
            self.cursor.execute(update_query, (new_value,))

            # Commit the changes
            self.connection.commit()

            print("Data updated successfully.")

        except sqlite3.Error as e:
            print(f"Error updating data: {e}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")


db = SQLiteManager('db.sqlite')
db.create_table('users',
                'id INTEGER PRIMARY KEY AUTOINCREMENT, status string, username string, passwd string,'
                ' shoots string, prizes string')
db.create_table('ships', 'id INTEGER PRIMARY KEY AUTOINCREMENT, x integer, y integer, prize_id integer,'
                         'field_id integer')
db.create_table('prizes', 'id INTEGER PRIMARY KEY AUTOINCREMENT, name string, desc string, src string')
db.create_table('fields', 'id INTEGER PRIMARY KEY AUTOINCREMENT, n integer')
db.close_connection()
