from nlp import split_to_sentences, get_embeddings, sentence_transformer, compare_embeddings
import torch
from tqdm import tqdm

def match_sentences(ch_known, ch_learn):
    book = ""
    lg_known = 'pl'
    lg_learn = 'de'
    print(len(ch_known), len(ch_learn))
    sents_learn = split_to_sentences(ch_learn[:], lg_learn)
    sents_known = split_to_sentences(ch_known[:], lg_known)

    embeddings_learn = get_embeddings(sents_learn)
    embeddings_known = get_embeddings(sents_known)
    print(f"{len(embeddings_learn)=}")
    print(f"{len(embeddings_known)=}")

    sims = compare_embeddings(embeddings_learn, embeddings_known)
    # print(sims)

    for l,sim in tqdm(enumerate(sims)):
        k = torch.argmax(sim)
        # print(f"{sim[k]}\n{l}:{repr(sents_learn[l])}\n{k}:{repr(sents_known[k])}\n\n")
        print(f"{l}[{lg_learn}]:{sents_learn[l]}\n{k}[{lg_known}]:{sents_known[k]}\n", file=open("ch4depl.txt","a+"))


def main():
    ch4de = open("ch4de.txt", "r").read()
    ch4pl = open("ch4pl.txt", "r").read()
    ch4en = open("ch4en.txt", "r").read()
    match_sentences(ch4pl,ch4de)

if __name__ == "__main__":
    main()