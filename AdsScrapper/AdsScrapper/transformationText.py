import nltk
from nltk.corpus import stopwords
from collections import Counter
from nltk.tokenize import word_tokenize
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer
import os
import pandas as pd
import numpy as np
import re
from spellchecker import SpellChecker
from num2words import num2words
from nltk.corpus import wordnet as wn
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import unicodedata
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')

class TransformationTexte (BaseEstimator, TransformerMixin):
  
    
    
    def __init__(self, language='french'):
        
        self.spell = SpellChecker(language='fr')
        self.mots = "surface,chauffage,climatisation,ascenseur"
        self.liste_mots = self.mots.split(", ")
        self.nlp = spacy.load('fr_core_news_sm')
    
    def fit(self, X, y=None):
         pass
      
    def transform(self, X, y=None):pass
       

    def TransormRawText(self,text):
          text= text.lower()
          def number_to_words(match):
           number = int(match.group(1))
           if number==0:
            return ""
           else: return "sallon et {} chambres".format(num2words(number, lang='fr'))

    # Replace patterns of the form "s+number" with "sallon et the number in letters"
          text = re.sub(r"\s*\+\s*", "+", text)
          text = re.sub(r"s\+(\d+)", number_to_words, text)
          text = text.replace('éme', 'ème').replace(' ème', 'ème').replace('1er', '1ère').replace(' eme', 'ème').replace(' eau',' bain')
          pattern = re.compile(r'\b([1-2]?\d{1,2}|1[0-9])\s*(ème|éme|er?)\b|[^\w\s,]|[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', re.MULTILINE)
          text = pattern.sub(lambda match: num2words(int(match.group(1)), lang='fr') + match.group(2) if match.group(1) else ' ', text)
          text = re.sub(r'\b(3[1-9]|[4-9]\d|\d{3,})\b', '', text)
          text = re.sub(r'\b([0-9])\b', lambda match: ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf"][int(match.group(1))], text)
          text = re.sub(r'\b\w*\d+\w*\b', '', text)
          text = re.sub(r'\b(\d+)(ère|ème|er?)\b', lambda match: num2words(int(match.group(1)), lang='fr') + match.group(2), text)
          text = re.sub(r'\d+', ' ', text)
          text = text.replace('\n', ' ').replace('\r', ' ')
          misspelled = self.spell.unknown(text.split())
          for word in misspelled:
            corrected_word = self.spell.correction(word)
            if corrected_word:
                text = text.replace(word, corrected_word)
          for mot in self.liste_mots:
            target_word =mot
            doc = self.nlp(text)
            lemmas = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
            synsets = wn.synsets(target_word, lang='fra')
            synonyms = set()
            for synset in synsets:
                for lemma in synset.lemmas(lang='fra'):
                    synonyms.add(lemma.name())

                # Check if any of the lemmas match any of the synonyms
            detected_synonyms = set()
            for lemma in lemmas:
                if lemma in synonyms:
                    detected_synonyms.add(lemma)

                # Print the detected synonyms
            if len(detected_synonyms) > 0:
                for ds in detected_synonyms:
                    text=text.replace(ds,mot)
         
          return text

if __name__ == '__main__':
    pass