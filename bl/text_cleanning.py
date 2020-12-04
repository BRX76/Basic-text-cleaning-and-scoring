import string
import re
import nltk
import logging
import gensim

from gensim.models import TfidfModel
from nltk.corpus import stopwords  # Removing stopwords
from nltk import TreebankWordTokenizer  # specific tokenizer
from nltk.stem import PorterStemmer
from config import LOGGER_NAME, REMOVE_STRINGS_LEN

log = logging.getLogger(LOGGER_NAME)


class TextPrep:
    def __init__(self, items, cleaning_techniques, stop_words_list=None, regex_list=None):
        '''
        :param docs: The list of docs as full sentences
        :param stop_words_list: Any dedicated stop words to use while cleaning the docs? --defult is english
        :param cleaning_techniques: which cleanning steps should we use on the texts list?
        :param regex_list: regexes to remove from text, such as elastic log timestamp
        '''
        self.items = items
        self.stop_words_list = stop_words_list
        self.cleaning_techniques = cleaning_techniques
        self.regex_list = regex_list
        self.class_properties = [a for a in dir(items[0]) if not a.startswith('__')]

    def generic_to_dict(self):
        temp_list = []
        for item in self.items:
            temp_list.append(vars(item))
        return temp_list

    def auto_detect_stopwords(self):
        pass

    @staticmethod
    def tokenizer_text(text, tokenizer):
        if text:
            return tokenizer.tokenize(text)
        return ''

    def to_lower(self, item):
        tokenizer = TreebankWordTokenizer()
        for field in self.class_properties:
            current_field_value = getattr(item, field)
            setattr(item, field, [w.lower() for w in self.tokenizer_text(current_field_value, tokenizer)])
        return item

    def lower_and_tokenize(self):
        for counter, item in enumerate(self.items):
            self.items[counter] = self.to_lower(item)

    def remove_digits_and_punct(self):
        for item in self.items:
            for field in self.class_properties:
                temp_list = []
                current_field_value = getattr(item, field)
                for word in current_field_value:
                    result = word.translate(str.maketrans('', '', string.punctuation))
                    if result not in ['', ' '] and not result.isdigit():
                        temp_list.append(''.join(i for i in word if not i.isdigit()))
                setattr(item, field, temp_list)

    def remove_stop_words(self):
        all_stopwords = nltk.corpus.stopwords.words('english')
        if self.stop_words_list:
            stopwords.extend(self.stop_words_list)
        for item in self.items:
            for field in self.class_properties:
                current_field_value = getattr(item, field)
                setattr(item, field, [word for word in current_field_value if word not in all_stopwords])

    def remove_by_regex(self):
        # It is possible to run all the regexes and only then update the original doc
        # To be done if needed
        for regex in self.regex_list:
            regex = re.compile(regex)
            for item in self.items:
                for field in self.class_properties:
                    current_field_value = getattr(item, field)
                    filtered = [i for i in current_field_value if not regex.search(i)]
                    setattr(item, field, ' '.join(filtered))

    def split_by_all_punct(self):
        for item in self.items:
            for field in self.class_properties:
                current_field_value = getattr(item, field)
                if current_field_value:
                    no_punct = re.split("[" + string.punctuation + "]+", current_field_value)
                    no_punct = ' '.join(no_punct)
                    # remove multiple spaces
                    setattr(item, field, re.sub(' +', ' ', no_punct))

    def remove_single_strings(self):
        for item in self.items:
            for field in self.class_properties:
                current_field_value = getattr(item, field)
                if current_field_value:
                    setattr(item, field, [string_x for string_x in
                                          current_field_value if len(string_x) > REMOVE_STRINGS_LEN])

    def stem_words(self):
        ps = PorterStemmer()
        for item in self.items:
            for field in self.class_properties:
                current_field_value = getattr(item, field)
                if current_field_value:
                    setattr(item, field, [ps.stem(word) for word in current_field_value])

    def prepare_texts(self):
        for technique in self.cleaning_techniques:
            if technique == 'split_by_all_punct':
                log.info('Got into split_by_all_punct')
                self.split_by_all_punct()

            elif technique == 'lower_and_tokenize':
                log.info('Got into lower_and_tokenize')
                self.lower_and_tokenize()

            elif technique == 'remove_digits_and_punct':
                log.info('Got into remove_digits_and_punct')
                self.remove_digits_and_punct()

            elif technique == 'remove_stop_words':
                log.info('Got into remove_stop_words')
                self.remove_stop_words()

            elif technique == 'remove_by_regex':
                log.info('Got into remove_by_regex')
                if self.regex_list:
                    self.remove_by_regex()

            elif technique == 'remove_single_strings':
                log.info('remove_single_strings')
                self.remove_single_strings()

            elif technique == 'stem_words':
                self.stem_words()

    def transform_list_to_str(self):
        for item in self.items:
            for field in self.class_properties:
                current_field_value = getattr(item, field)
                setattr(item, field, ' '.join(current_field_value))

    def filter_by_tf_idf_score(self, items):
        dictionary = gensim.corpora.Dictionary(items)  # docs is a list of text documents
        corpus = [dictionary.doc2bow(doc) for doc in items]
        tfidf = TfidfModel(corpus, id2word=dictionary)
        low_value = 0.2
        low_value_words = []
        for bow in corpus:
            low_value_words += [id for id, value in tfidf[bow] if value < low_value]
        dictionary.filter_tokens(bad_ids=low_value_words)
        new_corpus = [dictionary.doc2bow(doc) for doc in items]
        final_list = self.get_filtered_docs(dictionary, new_corpus)
        return final_list
    @staticmethod
    def get_filtered_docs(dictionary, corpus):
        final_list = []
        for item in corpus:
            temp_list = []
            for word in item:
                for word_actual_name in dictionary.token2id.keys():
                    if dictionary.token2id[word_actual_name] == word[0]:
                        temp_list.append(word_actual_name)
            final_list.append(' '.join(temp_list))
        return final_list
