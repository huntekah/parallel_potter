import spacy
from typing import List
from sentence_transformers import SentenceTransformer, util

nlp = {}
nlp['en'] = spacy.load("en_core_web_sm")
nlp['pl'] = spacy.load("pl_core_news_sm")
nlp['de'] = spacy.load("de_core_news_sm")
sentence_transformer = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


def split_to_sentences(text, lang) -> List[str]:
    doc = nlp[lang](text)
    return list(map(str,doc.sents))
# doc = nlp('This is the first sentence. This is the second sentence.')
# for sent in doc.sents:
#     print(sent)

def compare_embeddings(emb1, emb2):
    return util.cos_sim(emb1, emb2)
def get_embeddings(texts: List[str]):
    return sentence_transformer.encode(texts)