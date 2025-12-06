
from datetime import datetime

class Document:
    """Classe de base pour représenter un document générique"""
    def __init__(self, titre, auteur, date, url, texte):
        self.titre = titre
        self.auteur = auteur
        self.date = date  # on peut garder comme string ou convertir en datetime
        self.url = url
        self.texte = texte
        self.type = "Document"

    def __str__(self):
        return f"{self.titre} ({self.type})"

class RedditDocument(Document):
    """Document provenant de Reddit, avec le nombre de commentaires"""
    def __init__(self, titre, auteur, date, url, texte, comments=0):
        super().__init__(titre, auteur, date, url, texte)
        self.comments = comments
        self.type = "Reddit"

class ArxivDocument(Document):
    """Document provenant d'Arxiv, avec liste d'auteurs"""
    def __init__(self, titre, auteurs, date, url, texte):
        super().__init__(titre, ", ".join(auteurs), date, url, texte)
        self.auteurs_list = auteurs
        self.type = "Arxiv"
