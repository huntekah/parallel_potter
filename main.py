import torch
from tqdm import tqdm

from nlp import (compare_embeddings, get_embeddings, sentence_transformer,
                 split_to_sentences)


def match_sentences(ch_known, ch_learn):
    book = ""
    lg_known = "pl"
    lg_learn = "de"
    window_size = 3
    DIMINISH_FACTOR = 0.1

    f_name = "ch4depl.txt"
    with open(f_name, "w"):
        pass
    f_handle = open(f_name, "a+")

    print(len(ch_known), len(ch_learn))
    sents_learn = split_to_sentences(ch_learn[:], lg_learn)
    sents_known = split_to_sentences(ch_known[:], lg_known)

    embeddings_learn = get_embeddings(sents_learn)
    embeddings_known = get_embeddings(sents_known)
    print(f"{len(embeddings_learn)=}")
    print(f"{len(embeddings_known)=}")

    sims = compare_embeddings(embeddings_learn, embeddings_known)
    # print(sims)
    last_k = 0
    last_l = 0
    for l, sim in tqdm(enumerate(sims)):
        k_min = max(last_k - window_size, 0)
        k_max = min(last_k + window_size, len(sim) - 1)
        k_mid = (k_min + k_max) // 2
        # cause of that I dont need full nxn embeddings matrix. to be fixed later

        for k_diminish in list(range(k_min)) + list(range(k_max, len(sim))):
            sim[k_diminish] = sim[k_diminish] / (
                1 + abs(k_diminish - k_mid) * DIMINISH_FACTOR
            )
        # sim[:k_min] = 0
        # sim[k_max:] = 0
        # print(sim)
        k = torch.argmax(sim)
        if k > last_k:
            print("+", l, int(k))
            # print(f"{sim[k]}\n{l}:{repr(sents_learn[l])}\n{k}:{repr(sents_known[last_k:k+1])}\n\n")
            learn_sentences_to_print = "".join(sents_learn[last_l:l])
            known_sentences_to_print = "".join(sents_known[last_k:k])
            print(
                f"{last_l}-{l}[{lg_learn}]:{learn_sentences_to_print}\n{last_k}-{k}[{lg_known}]:{known_sentences_to_print}\n--",
                file=f_handle,
            )
            last_k = k
            last_l = l
        else:
            print(".", l, int(k))

    learn_sentences_to_print = "".join(sents_learn[last_l:])
    known_sentences_to_print = "".join(sents_known[last_k:])
    print(
        f"{last_l}-END[{lg_learn}]:{learn_sentences_to_print}\n{last_k}-END[{lg_known}]:{known_sentences_to_print}\n--",
        file=f_handle,
    )
    f_handle.close()


def main():
    ch4de = open("ch4de.txt", "r").read()
    ch4pl = open("ch4pl.txt", "r").read()
    ch4en = open("ch4en.txt", "r").read()
    match_sentences(ch4pl, ch4de)


if __name__ == "__main__":
    main()
