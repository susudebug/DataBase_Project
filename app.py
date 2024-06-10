"""
Connects to a SQL database using pyodbc
"""
import pyodbc
SERVER = 'MJY'
DATABASE = 'LibraryDB'
USERNAME = 'sa'
PASSWORD = '123456'
connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
conn = pyodbc.connect(connectionString)
