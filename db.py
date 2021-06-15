import pyodbc
import pandas as pd
from flask import session
# from tools import Verbose

""" Documentation: Connection
   Description:
       a class used to connect to database using pyodbc package.
   Parameters:
     driver: database driver
     server: database server name
     database: database name
     userid: database user name/id
     password: user password
   Returns:
     object: connection object so you can execute sql queries to the provided database.
"""


class Connection:
    def __init__(self, driver, server, database, userid, password):
        self.error = None
        self.driver = driver if driver else "{ODBC Driver 17 for SQL Server}"
        self.server = server
        self.database = database
        self.UserId = userid
        self.password = password
        self.connection_string = f'DRIVER={self.driver};' \
                                 f'SERVER={server};' \
                                 f'DATABASE={database};' \
                                 f'UID={userid};' \
                                 f'PWD={password}'
        self.conn = self.connect()


    """ Documentation: connect
       Description:
           used to connect to database using pyodbc package.
       Returns:
         object: connection object so you can execute sql queries to the provided database.
    """
    def connect(self):
        try:
            conn = pyodbc.connect(self.connection_string)
            print('Connected to the database successfully!')
            # Verbose.print_ln('Connected to the database successfully!')
            return conn
            
        except Exception as err:
            conn = None
            print(f'\nFailed to connect to the database! \nError: {str(err)}')
            print(self.connection_string)
            #Verbose.print_ln(f'\nFailed to connect to the database! \nError: {str(err)}')
            # Verbose.print_ln(self.connection_string)
            self.error = str(err)
            return conn


    """ Documentation: run
    Description:
        a public method, execute select query using pandas and return the dataframe.
    
    Parameters:
        sql_query (string): string representing select SQL query.
    Returns:
        object(dataframe): result select query from the database as a dataframe.
    """
    def run(self, sql_query):
        result = None

        if self.conn:
            try:
                result = pd.read_sql(sql_query, self.conn)
                print(f'Connected to the database {self.database}')
                return result
            except Exception as err:
                print("Was not able to run the query", sql_query)
                print("Error:", str(err))
                #Verbose.print_ln("Was not able to run the query", sql_query)
                #Verbose.print_ln("Error:", str(err))
                return str(err)
        else:
            Verbose.print_ln("Something wrong happened, not connected!")
            print("Something wrong happened, not connected!")

        return result

    """ Documentation: run_via_cursor
     Description:
         a public method, execute select query using cursor of pyodbc and return the object result.
     Parameters:
         sql_query (string): string representing select SQL query.
     Returns:
         object: result select query from the database as a object.
     """
    def run_via_cursor(self, sql_query):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(sql_query)

                # for row in cursor:
                #     print(row)

                return cursor
            except Exception as err:
                print("Was not able to execute the query via the cursor")
                print("Error:", str(err))
                return str(err)
        else:
            print("Something wrong happened, not connected!")
            return "Seomthing wrong happend, not connected!"
    """ Documentation: create
      Description:
          a public method, execute select query using cursor of pyodbc and create new structure in the database
          table, view, ... etc, you can execute select queries here but won't return anything.
      Parameters:
          sql_query (string): string representing DDL SQL query.
    """
    def create(self, sql_query):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(sql_query)
                self.conn.commit()
            except Exception as err:
                print('Was not able to create view', sql_query)
                print("Error:", str(err))
                return str(err)
        else:
            print("Something wrong happened, not connected!")
            return "Something wrong happened, not connected!"








def connect_db(server="", db="", username="", password="", driver=""):
    #if 'db' not in session:
    conn = Connection(driver, server, db, username, password)
    session["driver"] = driver
    session["server"] = server
    session["db"] = db
    session["username"] = username
    session["password"] = password
    return conn


def get_db():
    # if no session return none
    conn = Connection(session["driver"], session["server"], session["db"], session["username"], session["password"]) 
    return conn


def close_db(e=None):
    db = session.pop('db', None)

    if db is not None:
        db.close()