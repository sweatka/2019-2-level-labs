import math


REFERENCE_TEXTS = []


def clean_tokenize_corpus(texts: list) -> list:
    if not texts or not isinstance(texts, list):
        return []
    corpus = []
    for text_i in texts:
        if not isinstance(text_i, str):
            continue
        new_text = ''
        text_i = text_i.lower()
        text_i = text_i.replace('\n', ' ')
        text_i = text_i.replace('<br />', ' ')
        text_i = text_i.replace('  ', ' ')
        for symbol in text_i:
            if symbol == ' ' or symbol.isalpha():
                new_text += symbol
        new_text = new_text.split()
        corpus.append(new_text)
    return corpus


class TfIdfCalculator:
    def __init__(self, corpus):
        self.corpus = corpus
        self.tf_values = []
        self.idf_values = {}
        self.tf_idf_values = []

    def calculate_tf(self):
        if isinstance(self.corpus, list):
            for text_i in self.corpus:
                tf_for_words_in_one_text = {}
                if text_i:
                    all_words_number = len(text_i)
                    for word in text_i:
                        if not isinstance(word, str):
                            all_words_number -= 1
                elif not text_i:
                    continue
                for word in text_i:
                    if isinstance(word, str) and word not in tf_for_words_in_one_text:
                        word_number = text_i.count(word)
                        tf = word_number / all_words_number
                        tf_for_words_in_one_text[word] = tf
                if tf_for_words_in_one_text:
                    self.tf_values.append(tf_for_words_in_one_text)
        return self.tf_values


    def calculate_idf(self):
        if isinstance(self.corpus, list):
            for text_i in self.corpus:
                if isinstance(text_i, list) or text_i is not None:
                    for word in text_i:
                        if isinstance(word, str) and word not in self.idf_values:
                            number_in_one_text = 0
                            number_in_all_texts = len(self.corpus)
                            for text_j in self.corpus:
                                if isinstance(text_j, list) and word in text_j:
                                    number_in_one_text += 1
                                elif not isinstance(text_j, list) or text_j is None:
                                    number_in_all_texts -= 1
                            div = number_in_all_texts / number_in_one_text
                            self.idf_values[word] = math.log(div)


    def calculate(self):
        if self.idf_values and self.tf_values:
            for text_i in self.tf_values:
                tf_idf_dict = {}
                for word, tf in text_i.items():
                    tf_idf_dict[word] = tf * self.idf_values[word]
                self.tf_idf_values.append(tf_idf_dict)
        return self.tf_idf_values


    def report_on(self, word, document_index):
        if document_index >= len(self.corpus) or not self.tf_idf_values:
            return ()
        tf_idf_for_document = self.tf_idf_values[document_index]
        if word in tf_idf_for_document:
            document_tf_idf_keys = tf_idf_for_document.get
            tf_idf_rated = sorted(tf_idf_for_document, key=document_tf_idf_keys, reverse=True)
            rating = tf_idf_rated.index(word)
            return tf_idf_for_document[word], rating


if __name__ == '__main__':
    texts = ['5_7.txt', '15_2.txt', '10547_3.txt', '12230_7.txt']
    for text in texts:
        with open(text, 'r') as f:
            REFERENCE_TEXTS.append(f.read())
    # scenario to check your work
    test_texts = clean_tokenize_corpus(REFERENCE_TEXTS)
    tf_idf = TfIdfCalculator(test_texts)
    tf_idf.calculate_tf()
    tf_idf.calculate_idf()
    tf_idf.calculate()
    print(tf_idf.report_on('good', 0))
    print(tf_idf.report_on('and', 1))


