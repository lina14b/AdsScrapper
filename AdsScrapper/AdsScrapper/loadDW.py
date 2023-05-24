import mysql.connector
from pymongo import MongoClient
import pandas as pd
class LoadDW:

  def __init__(self):
    self.host = 'localhost'
    self.user = 'root'
    self.password = ''
    self.database = 'AdsScrapperDw'
    self.AdsHist=self.loadAdsHist() 

  def loadAdsHist(self):
    client = MongoClient("mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/test")
    db = client["AdsScrappers"]
    collection = db["AdsHistorisation"]
    cursor = collection.find({})
    datas = list(cursor)
    df = pd.DataFrame(datas)
    df['number']=1
    df.drop(columns=["tokens", "code"], inplace=True)
    df_cleaned = df.dropna()
    return df_cleaned
 
  def createDB(self):
    create=False
    try:
        connection = mysql.connector.connect(host=self.host,user=self.user,password=self.password)
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()

        db_exists = False
        for db in databases:
            if db[0] == self.database:
                db_exists = True
                break

        if not db_exists:
            cursor.execute(f"CREATE DATABASE {self.database}")
            create=True
        else:
           create=db_exists

        # Close the cursor and connection
        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        print("Error while connecting to MySQL server", error)
    return create
  def createTables(self):
    table_queries = [
    '''
    CREATE TABLE IF NOT EXISTS dim_location (
        idlocation INT AUTO_INCREMENT PRIMARY KEY,
        ville VARCHAR(255),
        state VARCHAR(255),
        country VARCHAR(255)
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS dim_Type (
        idtype INT AUTO_INCREMENT PRIMARY KEY,
        Type VARCHAR(255)
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS dim_date (
        iddate DATE PRIMARY KEY,
        day INT,
        month INT,
        monthname VARCHAR(255), 
        year INT
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS fact_ads (
        idfact INT AUTO_INCREMENT PRIMARY KEY,
        idad VARCHAR(255),
        idtype  VARCHAR(255),
        idlocation INT,
        iddate DATE,
        price DECIMAL(10, 2),
        surface DECIMAL(10, 2),
        prixM2 DECIMAL(10, 2),
        number INT,
        FOREIGN KEY (idlocation) REFERENCES dim_location (idlocation),
        FOREIGN KEY (iddate) REFERENCES dim_date (iddate)
    )
    '''
    ]

    try:
        connection = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database)

        cursor = connection.cursor()
        for query in table_queries:
            cursor.execute(query)

        print("Tables created successfully or already exist")

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        print("Error while connecting to MySQL server", error)
  def LoadDimLocation(self):
    dfLocation=self.AdsHist[['country', 'state', 'ville']]
    subset_columns = ['country', 'state', 'ville']
    distinct_values = dfLocation.drop_duplicates(subset=subset_columns)
    print(distinct_values)
    connection = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database)
    cursor = connection.cursor()

    select_query = "SELECT 1 FROM dim_location WHERE ville = %s AND state = %s"
    insert_query = "INSERT INTO dim_location (ville, state, country) VALUES (%s, %s, %s)"

    for index, row in distinct_values.iterrows():
        data = (row['ville'], row['state'], row['country'])
        # cursor.execute(insert_query, data)
        # connection.commit()
        cursor.execute(select_query, (data[0], data[1]))

        if cursor.fetchone() is None:
            cursor.execute(insert_query, data)
            connection.commit()
            print("Row inserted.")
        else:
            print("Combination of 'ville' and 'state' already exists.")

    cursor.close()
    connection.close()
  def getDimLocationId(self,ville,state):
    
    connection = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database)
    cursor = connection.cursor()
    select_query = "SELECT idlocation FROM dim_location WHERE ville = %s AND state = %s"
    cursor.execute(select_query, (ville, state))
    result = cursor.fetchone()
    idlocation = result[0] if result else None
    cursor.close()
    connection.close()
    return idlocation
  def getDimtypeId(self,type):
    connection = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database)
    cursor = connection.cursor()
    select_query = "SELECT idtype FROM dim_type WHERE type = %s"
    cursor.execute(select_query, [type])
    result = cursor.fetchone()
    idlocation = result[0] if result else None
    cursor.close()
    connection.close()
    return idlocation     
  def LoadDimType(self):
    
    subset_columns = self.AdsHist['type']
    distinct_values = subset_columns.drop_duplicates()
    print(distinct_values)
    connection = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database)
    cursor = connection.cursor()

    select_query = "SELECT 1 FROM dim_type WHERE type = %s"
    insert_query = "INSERT INTO dim_type(type) VALUES (%s)"
    

    for  row in distinct_values:
        print(type(row))
        # cursor.execute(insert_query, data)
        # connection.commit()
        cursor.execute(select_query, [row])

        if cursor.fetchone() is None:
            cursor.execute(insert_query, [row])
            connection.commit()
            print("Row inserted.")
        else:
            print("exists.")

    cursor.close()
    connection.close()
  def LoadDimTime(self):
    min_date = self.AdsHist['dateinstered'].min()
    max_date = self.AdsHist['dateinstered'].max()
    date_range = pd.date_range(start=min_date.date(), end=max_date.date(), freq='D')
    connection = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database)
    cursor = connection.cursor()

    insert_statements = []
    for date_obj in date_range:
        date_str = date_obj.strftime('%Y-%m-%d')
        day = date_obj.day
        month = date_obj.month
        monthname = date_obj.strftime('%B')
        year = date_obj.year
        
        insert_statement = f"INSERT IGNORE INTO dim_date (iddate, day, month, monthname, year) VALUES ('{date_str}', {day}, {month}, '{monthname}', {year})"
        insert_statements.append(insert_statement)

    for statement in insert_statements:
        print(cursor.execute(statement))

    connection.commit()

    cursor.close()
    connection.close()
  def loadFact(self):
    
    connection = mysql.connector.connect(host=self.host,user=self.user,password=self.password,database=self.database    )
    cursor = connection.cursor()


    insert_query = "INSERT INTO fact_ads (idad, idtype,idlocation, iddate, price, surface, prixM2, number) VALUES (%s,%s, %s, %s, %s, %s, %s,%s)"
    j=0
    for index, row in self.AdsHist.iterrows():
        j+=1

        idlocation=self.getDimLocationId(row['ville'],row['state'])
        idtype=self.getDimtypeId(row['type'])
        date_obj=row['dateinstered']
        date_str = date_obj.strftime('%Y-%m-%d')
        if row['price']<1000:
           row['price']=row['price']*10
        if row['price']<0:
           row['price']=row['price']*-1
        if row['price']>10000000:
           row['price']=row['price']/1000
           
        data = (str(row['_id']),idtype,idlocation,date_str,row['price'], row['surfaceTotale'],row['price']/row['surfaceTotale'], row['number'])
        print(j,data)
        cursor.execute(insert_query, data)
        connection.commit()

    cursor.close()
    connection.close()