
import pandas as pd
from math import sqrt

class SearchEngine:
    """Moteur de recherche base sur TF"""
     def __init__(self, corpus):
        self.corpus = corpus
        self.vocab = corpus.vocabulaire()
        self.doc_ids = list(corpus.id2doc.keys())
         
    def vector_doc(self, doc):
        """Transforme un document en vecteur TF"""
        texte = self.corpus.nettoyer_texte(doc.texte)
        vect = []
        for mot in self.vocab:
            
            vect.append(texte.split().count(mot))
        return vect

    def vector_query(self, query):
        """Transforme une requete en vecteur TF"""
        query = self.corpus.nettoyer_texte(query)
        vect = []
        for mot in self.vocab:
            vect.append(query.split().count(mot))
        return vect

    def cosine_similarity(self, v1, v2):
        """Calcule la similarite cosinus"""
        dot = sum(a*b for a,b in zip(v1,v2))
        norm1 = sqrt(sum(a*a for a in v1))
        norm2 = sqrt(sum(a*a for a in v2))
        if norm1==0 or norm2==0:
            return 0
        return dot/(norm1*norm2)

    def search(self, query, top_n=5):
        """recherche les documents les plus pertinents , jai utlise ai dans cette fonctionans cette fonction pour mesurer
        la similarite entre la requete et les documents a laide de la representation vectorielle et de la similarite cosinus,
        ce qui permet didentifier automatiquement les documents les plus pertinents """
        q_vect = self.vector_query(query)
        scores = []
        for doc_id in self.doc_ids:
            doc_vect = self.vector_doc(self.corpus.id2doc[doc_id])
            score = self.cosine_similarity(q_vect, doc_vect)
            scores.append((doc_id, score))
        scores.sort(key=lambda x:x[1], reverse=True)
        results = [(self.corpus.id2doc[doc_id], score) for doc_id, score in scores[:top_n]]
        df = pd.DataFrame([(doc.titre, doc.auteur, doc.type, score) for doc, score in results],
                          columns=["Titre","Auteur","Type","Score"])
        return df
