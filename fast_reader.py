import time
import argparse
from dataclasses import dataclass
import dataclasses

@dataclass
class WordsPerMinute:
    wpm: int

    def __post_init__(self):
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if not isinstance(value, field.type):
                setattr(self, field.name, field.type(value))

    def delay(self):
        return 60/self.wpm

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="fast-reader")
    parser.add_argument('--file',default="ch5pl.txt")
    parser.add_argument('--wpm', default = WordsPerMinute(287), type=WordsPerMinute)
    return parser.parse_args()

def load_text(f_name) ->str:
    with open(f_name, "r") as f_handle:
        text = f_handle.read()
        return text

def show_text(text:str,wpm: WordsPerMinute) -> None:
    n_words = 2
    words = text.split()
    for i in range(0,len(words),n_words):
        line = " ".join(words[i:i+n_words])
        # print(i,i+n_words)
        print(f"\r{repr(line):_^40}", end="", flush=True)
        time.sleep(wpm.delay())


if __name__ == "__main__":
    args = parse_args()
    text = load_text(args.file)
    show_text(text, args.wpm)
