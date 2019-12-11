"""
Labour work #3
 Building an own N-gram model
"""

import math

REFERENCE_TEXT = ''
if __name__ == '__main__':
    with open('not_so_big_reference_text.txt', 'r') as f:
        REFERENCE_TEXT = f.read()


class WordStorage:
    def __init__(self):
        self.storage = {}

    def put(self, word: str) -> int:
        if isinstance(word, str) and word not in self.storage:
            self.storage[word] = hash(word)
        return hash(word)

    def get_id_of(self, word: str) -> int:
        if isinstance(word, str) and word in self.storage:
            return self.storage.get(word)
        return -1

    def get_original_by(self, id: int) -> str:
        if isinstance(id, int):
            for key, value in self.storage.items():
                if value == id:
                    return key
        return 'UNK'

    def from_corpus(self, corpus: tuple):
        if isinstance(corpus, tuple):
            for word in corpus:
                self.put(word)
        return {}


class NGramTrie:
    def __init__(self, n):
        self.size = n
        self.gram_frequencies = {}
        self.gram_log_probabilities = {}

    def fill_from_sentence(self, sentence: tuple) -> str:
        if not isinstance(sentence, tuple) or sentence == () or self.size > len(sentence):
            return 'ERROR'
        all_of_grams_list = []
        temp_n = self.size
        number = temp_n - 1
        for i in range(len(sentence) - number):
            all_of_grams_list.append(sentence[i:temp_n])
            temp_n += 1
        all_of_grams_tuple = tuple(all_of_grams_list)
        for element in all_of_grams_tuple:
            if element not in self.gram_frequencies.keys():
                self.gram_frequencies[element] = 1
            elif element in self.gram_frequencies.keys():
                self.gram_frequencies[element] += 1
        return 'OK'

    def calculate_log_probabilities(self):
        for gram in self.gram_frequencies:
            sum_grams = 0
            for gram_i in self.gram_frequencies:
                if gram[:-1] == gram_i[:-1]:
                    sum_grams += self.gram_frequencies[gram_i]
            self.gram_log_probabilities[gram] = math.log(self.gram_frequencies[gram] / sum_grams)
        return self.gram_log_probabilities

    def predict_next_sentence(self, prefix: tuple) -> list:
        future_word = []
        if not isinstance(prefix, tuple) or len(prefix) != self.size - 1:
            return []
        predicted_sentence = list(prefix)
        flag = True
        while flag:
            probabilities_list = []
            for gram in list(self.gram_log_probabilities.keys()):
                if gram[:-1] == prefix:
                    probabilities_list.append(self.gram_log_probabilities[gram])
            if not probabilities_list:
                break
            probabilities_list.sort(reverse=True)
            big_probability = probabilities_list[0]
            for gram, probability in list(self.gram_log_probabilities.items()):
                if big_probability == probability:
                    future_word = gram[-1]
            predicted_sentence.append(future_word)
            new_prefix = list(prefix[1:])
            new_prefix.append(future_word)
            prefix = tuple(new_prefix)
        return predicted_sentence


def encode(storage_instance, corpus) -> list:
    full_text_coded = []
    for sentence in corpus:
        sentence_coded = []
        for word in sentence:
            word = storage_instance.get_id_of(word)
            sentence_coded.append(word)
        full_text_coded.append(sentence_coded)
    return full_text_coded


def split_by_sentence(text: str) -> list:
    if not isinstance(text, str) or len(list(text)) < 2:
        return []
    else:
        text = text.replace('\n', ' ')
        text = text.replace('!', '.')
        text = text.replace('?', '.')
        text = text.replace('...', '.')
        text = text.replace('  ', ' ')
        if '.' not in text:
            return []
        elif '.' in text:
            string_text = ''
            for symbol in text:
                symbol = symbol.lower()
                if symbol.isalpha() or symbol == ' ' or symbol == '.':
                    string_text += symbol
    all_sentences = string_text.split('.')
    list_text = []
    for sentence in all_sentences:
        if sentence != '':
            sentence = sentence.split()
            sentence.insert(0, '<s>')
            sentence.append('</s>')
            list_text.append(sentence)
    return list_text


def running(size_n, text, pref):
    storage_ex = WordStorage()
    ngram_ex = NGramTrie(size_n)
    corpus = split_by_sentence(text)
    for sent in corpus:
        storage_ex.from_corpus(tuple(sent))
    encoded_corpus = encode(storage_ex, corpus)
    for sentence in encoded_corpus:
        ngram_ex.fill_from_sentence(tuple(sentence))
    ngram_ex.calculate_log_probabilities()
    pref_ids = []
    for word in pref:
        pref_ids.append(storage_ex.get_id_of(word))
    predict_sentence = ngram_ex.predict_next_sentence(tuple(pref_ids))
    # predict_sentence_coded = ngram_ex.predict_next_sentence(pref)
    # print(predict_sentence_coded)
    list_of_predict_words = []
    for word in predict_sentence:
        word = storage_ex.get_original_by(word)
        list_of_predict_words.append(word)
    print(list_of_predict_words)


