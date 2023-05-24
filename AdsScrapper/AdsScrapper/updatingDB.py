from pymongo import MongoClient
from bienImmobilier import BienImmobilier
import pandas as pd

#######Find All TA et TV
b=BienImmobilier()

print(b.Numberofdocs())
print("******************")
list=b.readAll_TA_TV()
df = pd.DataFrame(list)
print("1")

#######Find duplicates #######Delete dupilcates
counts = df.groupby(["code"]).size().reset_index(name="count")
counts_list = counts.to_dict("records")
number=len(counts_list)
deletedups=0
for group in counts_list:
    number=number-1
    #print(number)
    if group["count"] > 1:
        print(group, group["code"] )
        b.code=group["code"]
        b.website="tunisie-vente.com"
        x=b.deleteduplicate_Ta_TV()
        print(x)
        x1=b.deleteduplicate_Historisation()
        print(x1)
        deletedups=deletedups+1

print("deleted dups:",deletedups)
#######Delete date annonce > 3mois
Deleteitems=b.Delete_6months()
print("old items Deleted: ",Deleteitems)


import datetime

now = datetime.datetime.now()

from loadDW import LoadDW
from pymongo import MongoClient

if now.weekday() == 0 and now.hour < 12:
    print("______________")
    l=LoadDW()
    print("______________")
    l.createDB()
    print("______________")
    l.createTables()
    print("______________")
    l.LoadDimType()
    print("______________")
    l.LoadDimLocation()
    print("______________")
    l.LoadDimTime()
    print("______________")
    l.loadFact()

    client = MongoClient("mongodb+srv://lina:lina@cluster0.st42f.mongodb.net/test")
    db = client["AdsScrappers"]
    collection = db["AdsHistorisation"]

    collection.drop()
