import mysql.connector 
import pymongo

def migrate_all(mysqldb_dict,mongodb_host,mongodb_dbname):
    mysqldb = mysql.connector.connect(host= mysqldb_dict["mysql_host"],database= mysqldb_dict["mysql_database"],user= mysqldb_dict["mysql_user"],password= mysqldb_dict["mysql_password"])
    table_list_cursor = mysqldb.cursor()
    table_list_cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = %s ORDER BY table_name;", (mysqldb_dict["mysql_database"],))
    tables = table_list_cursor.fetchall()
    myclient = pymongo.MongoClient(mongodb_host)
    mydb = myclient[mongodb_dbname]

    def migrate(db,col):
        mycursor = db.cursor(dictionary=True) 
        mycursor.execute("SELECT * from "+col+";") 
        myresult = mycursor.fetchall()
        # print(myresult)
        print("Table name : "+ col)
        mycol = mydb[col]
        if len(myresult) > 0:
            x = mycol.insert_many(myresult)
            return len(x.inserted_ids)
        else:
            return 0

    for table in tables:
        x = migrate(mysqldb,table[0])
        print("Total inserted rows : " + str(x))


def migrate_single(mysqldb_dict,mongodb_host,mongodb_dbname,table):
    mysqldb = mysql.connector.connect(host= mysqldb_dict["mysql_host"],database= mysqldb_dict["mysql_database"],user= mysqldb_dict["mysql_user"],password= mysqldb_dict["mysql_password"])
    mycursor = mysqldb.cursor(dictionary=True) 
    mycursor.execute("SELECT * from "+table+";") 
    myresult = mycursor.fetchall()

    myclient = pymongo.MongoClient(mongodb_host)
    mydb = myclient[mongodb_dbname]
    mycol = mydb[table]
    if len(myresult) > 0:
        x = mycol.insert_many(myresult)
        print(len(x.inserted_ids))
    else:
        print(0)







