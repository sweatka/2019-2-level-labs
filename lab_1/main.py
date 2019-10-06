"""
Labour work #1
Count frequencies dictionary by the given arbitrary text
"""


def calculate_frequencies(text):
    if type(text) != str:
        return {}
    else:
        text = text.lower()
        symbols = [',', '.', '!', '?', ';', ':', '-', '(', ')', '%', '^', '@', '$', '*', '#', '"', "'", '&']
        digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for i in text:
            if i in symbols:
                text = text.replace(i, '')
            elif i in digits:
                text = text.replace(i, '')
        count_the_word = {}
        text_list = text.split()
        for n in text_list:
            if n not in count_the_word:
                count_the_word[n] = 1
            else:
                count_the_word[n] += 1
        return count_the_word


def filter_stop_words(d, stop_words):
    digits = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    if stop_words is None:
        return {}
    elif d is None:
        return {}
    else:
        keys = [k for k, v in d.items() if k in digits]
        for n in keys:
            del d[n]
        keys2 = [k for k, v in d.items() if k in stop_words]
        for i in keys2:
            del d[i]
        return d


def get_top_n(d, number):
    if number < 0:
        return ()
    else:
        top_words = sorted(d, key=d.get, reverse=True)
        top_words_tpl = tuple(top_words[:number])
        return top_words_tpl

