import logging
import pandas as pd

from config import LOGGER_NAME, CLEANING_TECHNIQUES
from bl.text_cleanning import TextPrep

log = logging.getLogger(LOGGER_NAME)


def clean_alibaba_results(alibaba_results):
    log.info('Cleaning alibaba results')
    clean_alibaba_results_list = []
    for alibaba_result in alibaba_results:
        cleaning_class = TextPrep(items=alibaba_result, cleaning_techniques=CLEANING_TECHNIQUES)
        cleaning_class.prepare_texts()
        data = pd.DataFrame(cleaning_class.generic_to_dict())
        titles = list(data['title'])

        # filter by tf_idf scores
        final_list = cleaning_class.filter_by_tf_idf_score(items=titles)
        list_without_empty = []
        for original_title, tf_idf_title in zip(titles, final_list):
            if tf_idf_title == '':
                # handle these cases...the texts are super long
                list_without_empty.append(' '.join(original_title))
            else:
                list_without_empty.append(tf_idf_title)
        clean_alibaba_results_list.append(list_without_empty)
    return clean_alibaba_results_list
