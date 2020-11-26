import logging
import pandas as pd

from config import LOGGER_NAME

log = logging.getLogger(LOGGER_NAME)


def naive_score_amazon_vs_alibaba(amazon_item, alibaba_result):
    try:
        amazon_word_list = amazon_item.split(' ')
        naive_scores = []
        naive_percent = []
        for alibaba_item in alibaba_result:
            counter=0
            for word in amazon_word_list:
                splitted_alibaba = alibaba_item.split(' ')
                if word in splitted_alibaba:
                    counter += 1
            naive_scores.append(counter)
            naive_percent.append(counter/len(amazon_word_list) * 100)
        df = pd.DataFrame(data={'scores': naive_scores,
                                'amazon_item': amazon_item,
                                'alibaba_item': alibaba_result,
                                'perc_scores': naive_percent})

        return df
    except Exception as e:
        log.error(e)
