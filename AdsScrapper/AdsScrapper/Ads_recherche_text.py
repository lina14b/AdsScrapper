from bienImmobilier import BienImmobilier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_distances
from transformationText import TransformationTexte
import pandas as pd
class Recherche:
    def __init__(self):
        b=BienImmobilier()
        self.data = b.readAll()
        self.list2=self.data[1:1000]
        self.t=TransformationTexte()
        self.vectors=self.t.fit(self.list2)

    
    def search_text(self, text):
        
        new_tokens =self.t.transform(text)
        new_description = ' '.join(new_tokens)
        new_vector = self.t.cv.transform([new_description])
        distances = cosine_distances(new_vector, self.vectors)
        lst = distances.tolist()
        flat_list = [elem for sublist in lst for elem in sublist]
        df = pd.DataFrame(self.list2)
        df['distances']=flat_list
        df_sorted = df.sort_values('distances', ascending=True)
        return df_sorted
    
    # def search_price(self, min_price, max_price):
    #     return [d for d in self.data if min_price <= d['price'] <= max_price]
    
    # def search_location(self, location):
    #     return [d for d in self.data if location in d['location']]
    
    # def search_surface(self, min_surface, max_surface):
    #     return [d for d in self.data if min_surface <= d['surface'] <= max_surface]
    
    # def search_all(self, text=None, min_price=None, max_price=None, location=None, min_surface=None, max_surface=None):
    #     results = self.data
    #     if text:
    #         results = self.search_text(text)
    #     if min_price and max_price:
    #         results = self.search_price(min_price, max_price)
    #     if location:
    #         results = self.search_location(location)
    #     if min_surface and max_surface:
    #         results = self.search_surface(min_surface, max_surface)
    #     return results

if __name__ == '__main__':
    r=Recherche()
    df=r.search_text("Maison a Hammamet a vendre vu sur mer")
    print(df["url"])