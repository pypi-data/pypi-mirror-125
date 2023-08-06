A Simple python Script to migrate data from MySQL to MongoDB 

-------------------------------------------------------------------------
            Author: ArJun Gawali (arjungawali111@gmail.com)
            Date: 27 Oct, 2021
            Version: 1.0.1
            Purpose: Migrate Data from MySQL to Mongo
-------------------------------------------------------------------------

Functions :

1. migrate_all  --> Migrate all tables from mysql to mongodb

    Parameters : 
        1. mysqldb_dict ==> A Python dictionary of your mysql database details 
                        Ex : 
                            mysqldb_dict = {
                                "mysql_host" :"localhost",
                                "mysql_database" : "sample_database",
                                "mysql_user" : "root",
                                "mysql_password" : "*******",
                            }
        2. mongodb_host ==> Your MongoDb hostname/Url
        3. mongodb_dbname ==> Choose the name of Database in which the data has to migrate.

2. migrate_single  --> Migrate specified table 

    Parameters : 
        1. mysqldb_dict ==> A Python dictionary of your mysql database details 
                        Ex : 
                            mysqldb_dict = {
                                "mysql_host" :"localhost",
                                "mysql_database" : "sample_database",
                                "mysql_user" : "root",
                                "mysql_password" : "*******",
                            }
        2. mongodb_host ==> Your MongoDb hostname/Url
        3. mongodb_dbname ==> Choose the name of Database in which the data has to migrate.
        4. table ==> Specific table which has to migrate 
        
