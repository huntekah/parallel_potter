from typing import List, Tuple
import torch
from tqdm import tqdm
import textwrap

from nlp import (compare_embeddings, get_embeddings, sentence_transformer,
                 split_to_sentences)
from algorithms import longest_increasing_subsequence, prefect_match, fill_in_gaps
from get_chapter import get_german_chapter, get_polish_chapter

# chapter_n = 9
def match_by_sim_score(embeddings_learn, embeddings_known) -> List[Tuple[int,int]]:
    sims = compare_embeddings(embeddings_learn, embeddings_known)
    # sims[l][k]
    # sims[l][?] -> how l matches each of sentences from k
    # sims[?][k] -> how known sentence k matches any of the learn sentences
    # TODO MAY Switch dim 0 and dim 1, not sure if correct.
    best_k_matches = list(map(int,torch.argmax(sims,dim=1))) # best k matches for each of l. max for each row
    best_l_matches = list(map(int,torch.argmax(sims,dim=0))) # max for each column

    increasing_subsequence_k = longest_increasing_subsequence([int(k_match) for k_match in best_k_matches])
    increasing_subsequence_l = longest_increasing_subsequence([int(l_match) for l_match in best_l_matches])

    print(f"{increasing_subsequence_k=}")
    print(f"{increasing_subsequence_l=}")

    print(f"{len(best_l_matches)=}")
    print(f"{len(best_k_matches)=}")
    print(f"{len(increasing_subsequence_l)=}")
    print(f"{len(increasing_subsequence_k)=}")
    # now we have two sets of sentences, which should (in theory) have best matches over the langs. what to do now?
    # [-1, 2, 3, 7, 9, 10]
    # [0, 3, 4, 5, 7, 9, 10]
    perfect_matches = prefect_match(increasing_subsequence_l,
                                    increasing_subsequence_k,
                                    best_l_matches,
                                    best_k_matches)
    # all_matches = fill_in_gaps(perfect_matches, sims)
    print(f"{perfect_matches=}")
    return perfect_matches

def print_perfect_matches(f_handle, perfect_matches, sents_learn, sents_known, lg_learn, lg_known):
    next_l = 0
    next_k = 0
    for k,l in perfect_matches:
        # print(f"{k=},{l=},{next_k=},{next_l=}")
        if k == next_k and l == next_l:
            learn_sentences_to_print = sents_learn[l]
            known_sentences_to_print = sents_known[k]
            # print(learn_sentences_to_print)
            printable_sents = textwrap.dedent(f"""\
            {k}[{lg_known}]:{known_sentences_to_print}
            {l}[{lg_learn}]:{learn_sentences_to_print}
            --""")
            next_k += 1
            next_l += 1
        else:
            printable_sents = "" # prefix on top of section
            if next_k < k:
                known_sentences_to_print = f"\n[{lg_known}] ".join(sents_known[next_k:k])
                printable_sents += f"{next_k}-{k}[{lg_known}]:{known_sentences_to_print}\n"
                next_k = k
            if next_l < l:
                learn_sentences_to_print = f"\n[{lg_learn}] ".join(sents_learn[next_l:l])
                printable_sents += f"{next_l}-{l}[{lg_learn}]:{learn_sentences_to_print}\n"
                next_l = l
            printable_sents += "~^" # suffix on bottom of section
        print(printable_sents, file=f_handle)
    if next_k < len(sents_known):
        known_sentences_to_print = f"\n[{lg_known}] ".join(sents_known[next_k:])
        printable_sents = f"{next_k}-{len(sents_known)}[{lg_known}]:{known_sentences_to_print}\n"
        print(printable_sents, file=f_handle)
    if next_l < len(sents_learn):
        learn_sentences_to_print = f"\n[{lg_learn}] ".join(sents_learn[next_l:])
        printable_sents = f"{next_l}-{len(sents_learn)}[{lg_learn}]:{learn_sentences_to_print}\n"
        print(printable_sents, file=f_handle)


def prepare_file(chapter_n, lg_know, lg_learn):
    f_name = f"chapters/ch{chapter_n}{lg_know}{lg_learn}.txt"
    return open(f_name, "w")


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
        print(f"{len(sents_learn)=}\n{len(sents_known)=}")

        embeddings_learn = get_embeddings(sents_learn)
        embeddings_known = get_embeddings(sents_known)

        matches = match_by_sim_score(embeddings_learn,embeddings_known)
        # matches = calculate_similarity(embeddings_learn, embeddings_known, window_size, DIMINISH_FACTOR)

        # print_matches(f_handle, matches, sents_learn, sents_known, lg_learn, lg_known)
        print_perfect_matches(f_handle, matches, sents_learn, sents_known, lg_learn, lg_known)


def main():
    chapter_n = 13
    ch_de = get_german_chapter(chapter_n).replace("\n"," ")
    ch_pl = get_polish_chapter(chapter_n).replace("\n"," ")
    print(f"{len(ch_pl)=},{len(ch_de)=}")
    # ch_de = open("chapters/ch7de.txt", "r").read().replace("\n", " ").replace("\r", "")
    # ch_pl = open("chapters/ch7pl.txt", "r").read()#.replace("\n", ". ").replace("\r", "")
    # ch_en = open("chapters/ch5en.txt", "r").read()#.replace("\n", ". ").replace("\r", "")
    match_sentences(ch_pl, ch_de,chapter_n)


if __name__ == "__main__":
    main()
