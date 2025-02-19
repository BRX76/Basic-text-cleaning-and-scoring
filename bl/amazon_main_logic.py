import logging
import pandas as pd

from config import LOGGER_NAME, CLEANING_TECHNIQUES
from bl.get_data import enum_amazon_items
from bl.text_cleanning import TextPrep

log = logging.getLogger(LOGGER_NAME)


def handle_amazon_logic():
    amazon_items = enum_amazon_items(items_file_path=r'common/amazon_items.json')
    # clean the data
    cleaning_class = TextPrep(items=amazon_items, cleaning_techniques=CLEANING_TECHNIQUES)
    cleaned_data = cleaning_class.prepare_texts()
    data = pd.DataFrame(cleaning_class.generic_to_dict())
    # for later usage - searching the whole string...
    data['full_text'] = data.title + data.description + \
                        data.catagories + data.details

    titles = list(data['title'])

    # filter by tf_idf scores
    log.info('filtering amazon items by tf_idf')
    final_list=cleaning_class.filter_by_tf_idf_score(items=titles)
    list_without_empty_amazon = []
    for original_title, tf_idf_title in zip(titles, final_list):
        if tf_idf_title == '':
            # handle these cases...the texts are super long
            list_without_empty_amazon.append(' '.join(original_title))
        else:
            list_without_empty_amazon.append(tf_idf_title)
    return list_without_empty_amazon
