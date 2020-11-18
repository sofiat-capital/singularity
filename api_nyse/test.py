import mysql.connector
from mysql.connector import Error

#try:
connection = mysql.connector.connect(host='localhost',
database='stockportfolio',
user='root',
password='Th3T3chBoy$')

mySql_Create_Table_Query = """CREATE TABLE DaveAustinTable(
idAsset_Category int(11) NOT NULL AUTO_INCREMENT,
name varchar(250) NULL,
ENTRY_DATE date,
PRIMARY KEY (idAsset_Category)) """

cursor = connection.cursor()
result = cursor.execute(mySql_Create_Table_Query)
print("Table created successfully ")


'''
except mysql.connector.Error as error:
    print("Failed to create table in MySQL: {}".format(error))
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
'''
