from pymongo import MongoClient
from bienImmobilier import BienImmobilier
import pandas as pd

#######Find All TA et TV
b=BienImmobilier()
list=b.readAll_TA_TV()
df = pd.DataFrame(list)


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