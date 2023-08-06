import random
from typing import List
from copy import deepcopy
from konlpy.tag import Mecab


class AEDA:
    def __init__(
        self,
        punc_ratio=0.3,
        random_punc=True,
        punc_list=[".", ",", ";", ":", "?", "!"],
    ):
        self.punc_ratio = punc_ratio
        self.random_punc = random_punc
        self.punc_list = punc_list

    def __call__(self, *args, **kwds):
        return self.aeda(*args, **kwds)

    def aeda(self, text: str) -> str:
        punc_ratio = self.punc_ratio

        morph_list = text.split()

        punc_num = (
            random.randint(1, int(punc_ratio * len(morph_list) + 1))
            if self.random_punc
            else int(punc_ratio * len(morph_list) + 1)
        )

        aug_word_index_list = random.sample(range(len(morph_list) + 1), punc_num)

        aug_word_index_list.sort(reverse=True)

        for index in aug_word_index_list:
            morph_list.insert(index, random.choice(self.punc_list))

        return " ".join(morph_list)


if __name__ == "__main__":
    text = "이 주변에 맛집이 어디 있나요? [SEP] 그 맛집은 맛있나요?"

    aeda = AEDA(punc_ratio=1)
    for i in range(10):
        print(aeda(text))
