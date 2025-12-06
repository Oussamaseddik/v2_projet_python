class Author:
    """Classe pour représenter un auteur et sa production"""
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = {}  # dictionnaire id_doc : Document

    def add(self, doc_id, doc):
        self.production[doc_id] = doc
        self.ndoc += 1

    def __str__(self):
        return f"{self.name} ({self.ndoc} documents)"
