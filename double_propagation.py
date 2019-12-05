# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 13:17:06 2019

@author: Nayan
"""

"""
Double propagation for attribute-qualifier extraction
"""
class QualifierAttributeExtractor:
    
    def __init__(self,
                 Seed_Qualifiers = ["good", "bad","awsome","amazing","best","worst","better","ideal"],
                 Seed_Attributes = list(), 
                 Pattern_Dictionary = {"pattern_1" : "POS:ADJ POS:NOUN","pattern_2" : "POS:NOUN POS:VERB POS:ADJ"}):
        import spacy
        nlp = spacy.load("en_core_web_sm")
        
        self.seed_qualifiers = Seed_Qualifiers
        self.seed_attributes = Seed_Attributes
        self.pattern_dictionary = Pattern_Dictionary
        self.nlp = nlp
###############################################################################

    def extract_qualifier_attribute(self,text):
        import textacy
        import pandas as pd
        
        from spacy.lemmatizer import Lemmatizer
        from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
        lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
        
        nlp = self.nlp 
        seed_qualifiers = self.seed_qualifiers
        seed_attributes = self.seed_attributes
        pattern_dictionary = self.pattern_dictionary
        
        
        Qualifier_Attribute_List = []
        New_Qualifier_List, New_Attribute_List = [], []
        
        doc = nlp(text.replace("-",""))
        cleaned_text = " ".join(token.text for token in doc if token.pos_ != "DET" )
        doc = nlp(cleaned_text)
        
        for pattern_key in pattern_dictionary.keys():
            Qualifier_Attribute_Phrases = textacy.extract.matches(doc, pattern_dictionary.get(pattern_key))
            for chunk in Qualifier_Attribute_Phrases:
                chunk_doc = nlp(chunk.text)
                qualifiers = [token.text for token in chunk_doc if token.pos_ == "ADJ"]
                attributes = [lemmatizer(token.text, 'NOUN')[0] for token in chunk_doc if token.pos_ == "NOUN"]
                if len(qualifiers) != 0 and len(attributes) != 0:
                    #print(qualifier[0], attribute[0])
                    #print(Q_list)
                    if qualifiers[0] in seed_qualifiers or attributes[0] in seed_attributes:
                        
                        Qualifier_Attribute_List.append(chunk_doc.text)
                        New_Qualifier_List.append(qualifiers[0])
                        New_Attribute_List.append(attributes[0])
                    
        #print(len(Q_A_list), len(Q_list), len(A_list))
        #print(Q_A_list, Q_list, A_list)
        return pd.DataFrame({"phrase":Qualifier_Attribute_List, "qualifier":New_Qualifier_List, "attribute":New_Attribute_List})

###############################################################################
 
    def bulk_extract_qualifier(self,df,text_column_name):
        import pandas as pd
        
        lexicon = pd.DataFrame({"phrase":[], "qualifier":[], "attribute":[]})
        
        i = 0 #Number of iterastions 2
        while i<2:
            for text in list(df[text_column_name]):
                Qualifiers_Attributes = self.extract_qualifier_attribute(text = text.lower())
    
                if len(Qualifiers_Attributes) != 0:
                    lexicon = lexicon.append(Qualifiers_Attributes,ignore_index = True)
            i = i+1
    
        lexicon.drop_duplicates(subset ="phrase", inplace =True)
        Qualifier_df = lexicon[["qualifier","attribute"]].groupby(by=['qualifier'], 
                                                   as_index = False).count().sort_values(by=["attribute"],
                                                                                         ascending=False)
        Qualifier_df.columns = ['qualifiers','no_of_unique_attributes']
        return Qualifier_df

###############################################################################
    def bulk_extract_attribute(self,df,text_column_name):
        import pandas as pd
        
        lexicon = pd.DataFrame({"phrase":[], "qualifier":[], "attribute":[]})
        
        i = 0 #Number of iterastions 2
        while i<2:
            for text in list(df[text_column_name]):
                Qualifiers_Attributes = self.extract_qualifier_attribute(text = text.lower())
    
                if len(Qualifiers_Attributes) != 0:
                    lexicon = lexicon.append(Qualifiers_Attributes,ignore_index = True)
            i = i+1
    
        lexicon.drop_duplicates(subset ="phrase", inplace =True)
        
        Attribute_df = lexicon[["qualifier","attribute"]].groupby(by=['attribute'], 
                                                          as_index = False).count().sort_values(by=["qualifier"],
                                                                                                ascending=False)
        Attribute_df.columns = ['attributes','no_of_unique_qualifiers']
        return Attribute_df
###############################################################################

    def bulk_extract_phrases(self,df,text_column_name):
        import pandas as pd
        
        lexicon = pd.DataFrame({"phrase":[], "qualifier":[], "attribute":[]})
        
        i = 0 #Number of iterastions 2
        while i<2:
            for text in list(df[text_column_name]):
                Qualifiers_Attributes = self.extract_qualifier_attribute(text = text.lower())
    
                if len(Qualifiers_Attributes) != 0:
                    lexicon = lexicon.append(Qualifiers_Attributes,ignore_index = True)
            i = i+1
    
        lexicon.drop_duplicates(subset ="phrase", inplace =True)
        
        return lexicon
###############################################################################
