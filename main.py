from typing import List, Tuple
import torch
from tqdm import tqdm

from nlp import (compare_embeddings, get_embeddings, sentence_transformer,
                 split_to_sentences)
from get_chapter import get_german_chapter, get_polish_chapter

chapter_n = 9
def match_by_sim_score() -> List[Tuple[int,int]]:
    pass
    # Match by sim score, and then locate non-sequential


def prepare_file(chapter_n, lg_know, lg_learn):
    f_name = f"chapters/ch{chapter_n}{lg_know}{lg_learn}.txt"
    return open(f_name, "a+")


def process_sentences(ch_text, lg_text):
    return split_to_sentences(ch_text[:], lg_text)


def calculate_similarity(embeddings_learn, embeddings_known, window_size, DIMINISH_FACTOR):
    sims = compare_embeddings(embeddings_learn, embeddings_known)
    last_k = 0
    last_l = 0
    matches = []
    for l, sim in tqdm(enumerate(sims)):
        k_min = max(last_k - window_size, 0)
        k_max = min(last_k + window_size, len(sim) - 1)
        k_mid = (k_min + k_max) // 2

        for k_diminish in list(range(k_min)) + list(range(k_max, len(sim))):
            sim[k_diminish] = sim[k_diminish] / (1 + abs(k_diminish - k_mid) * DIMINISH_FACTOR)

        k = torch.argmax(sim)
        if k > last_k:
            matches.append((last_l, l, last_k, k))
            last_k = k
            last_l = l
    matches.append((last_l, len(sims), last_k, len(sim)))
    return matches


def print_matches(f_handle, matches, sents_learn, sents_known, lg_learn, lg_known):
    for last_l, l, last_k, k in matches:
        learn_sentences_to_print = f"\n[{lg_learn}] ".join(sents_learn[last_l:l])
        known_sentences_to_print = f"\n[{lg_known}] ".join(sents_known[last_k:k])
        printable_sents = f"{last_k}-{k}[{lg_known}]:{known_sentences_to_print}\n{last_l}-{l}[{lg_learn}]:{learn_sentences_to_print}\n--"
        print(printable_sents, file=f_handle)


def match_sentences(ch_known, ch_learn, chapter_n):
    lg_known = "pl"
    lg_learn = "de"
    window_size = 3
    DIMINISH_FACTOR = 0.1

    with prepare_file(chapter_n,lg_know=lg_known,lg_learn=lg_learn) as f_handle:
        sents_learn = split_to_sentences(ch_learn, lg_learn)
        sents_known = split_to_sentences(ch_known, lg_known)

        embeddings_learn = get_embeddings(sents_learn)
        embeddings_known = get_embeddings(sents_known)

        matches = calculate_similarity(embeddings_learn, embeddings_known, window_size, DIMINISH_FACTOR)

        print_matches(f_handle, matches, sents_learn, sents_known, lg_learn, lg_known)



def main():
    ch_de = get_german_chapter(chapter_n).replace("\n"," ")
    ch_pl = get_polish_chapter(chapter_n).replace("\n"," ")
    print(f"{len(ch_pl)=},{len(ch_de)=}")
    # ch_de = open("chapters/ch7de.txt", "r").read().replace("\n", " ").replace("\r", "")
    # ch_pl = open("chapters/ch7pl.txt", "r").read()#.replace("\n", ". ").replace("\r", "")
    # ch_en = open("chapters/ch5en.txt", "r").read()#.replace("\n", ". ").replace("\r", "")
    match_sentences(ch_pl, ch_de)


if __name__ == "__main__":
    main()
