
import pandas as pd
import re
from src.Document import Document, RedditDocument, ArxivDocument
from src.Author import Author

class Corpus:
    """Classe pour gérer un corpus complet de documents"""
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}      # nom -> Author
        self.id2doc = {}       # id -> Document
        self.ndoc = 0
        self.naut = 0
        self.full_text = ""    # texte combiné pour recherche rapide

    def add_document(self, doc):
        """Ajoute un document au corpus"""
        doc_id = self.ndoc
        self.id2doc[doc_id] = doc
        self.ndoc += 1

        # Ajout auteur
        if doc.auteur not in self.authors:
            self.authors[doc.auteur] = Author(doc.auteur)
            self.naut += 1
        self.authors[doc.auteur].add(doc_id, doc)

        # Mettre à jour le texte combine
        self.full_text += " " + doc.texte

    def save(self, filename):
        """Sauvegarde le corpus dans un CSV"""
        data = []
        for doc_id, doc in self.id2doc.items():
            data.append([doc_id, doc.titre, doc.auteur, doc.date, doc.url, doc.type, doc.texte])
        df = pd.DataFrame(data, columns=["id", "titre", "auteur", "date", "url", "type", "texte"])
        df.to_csv(filename, sep="\t", index=False)

    def load(self, filename):
        """Charge le corpus depuis un CSV"""
        df = pd.read_csv(filename, sep="\t")
        for _, row in df.iterrows():
            if row["type"] == "Reddit":
                doc = RedditDocument(row["titre"], row["auteur"], row["date"], row["url"], row["texte"])
            elif row["type"] == "Arxiv":
                auteurs = row["auteur"].split(", ")
                doc = ArxivDocument(row["titre"], auteurs, row["date"], row["url"], row["texte"])
            else:
                doc = Document(row["titre"], row["auteur"], row["date"], row["url"], row["texte"])
            self.add_document(doc)

    #TD6 : Analyse textuelle 
    def nettoyer_texte(self, texte):
        """Nettoyage basique : minuscules, suppression \n, ponctuation"""
        texte = texte.lower()
        texte = texte.replace("\n", " ")
        texte = re.sub(r"[^a-z\s]", " ", texte)
        return texte

    def vocabulaire(self):
        """Construit le vocabulaire et le freq (TF et DF)"""
        vocab = {}
        for doc_id, doc in self.id2doc.items():
            texte = self.nettoyer_texte(doc.texte)
            mots = texte.split()
            seen = set()
            for mot in mots:
                if mot not in vocab:
                    vocab[mot] = {"TF":0, "DF":0}
                vocab[mot]["TF"] += 1
                if mot not in seen:
                    vocab[mot]["DF"] += 1
                    seen.add(mot)
        return vocab
