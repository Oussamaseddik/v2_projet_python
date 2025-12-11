class SearchEngine:
            # Initialise le moteur 
    def __init__(self, corpus):
        self.corpus = corpus
  # Cherche les documents correspondant à la requete et limite le nombre si demande
    def search(self, query, limit=None):
        res = self.corpus.search(query)
        if limit:
            return res[:limit]
        return res
