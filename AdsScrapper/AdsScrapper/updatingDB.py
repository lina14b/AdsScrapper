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
for group in counts_list:
    if group["count"] > 1:
        print(group, group["code"] )
        b.code=group["code"]
        b.website="tunisie-annonce.com"
        x=b.deleteduplicate_Ta_TV()
        print(x)
        x1=b.deleteduplicate_Historisation()
        print(x1)


#######Delete date annonce > 3mois
Deleteitems=b.Delete_6months()
print(Deleteitems)