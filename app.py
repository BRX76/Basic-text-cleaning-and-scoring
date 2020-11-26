import logging
import pandas as pd

from config import LOGGER_NAME
from bl.amazon_main_logic import handle_amazon_logic
from bl.search_amazon_items_in_alibaba import handle_alibaba_search
from bl.alibaba_results_handler import clean_alibaba_results
from bl.eval_search_results_acc import eval_naive_score



log = logging.getLogger(LOGGER_NAME)
# TODO: fix the logger so it will print to console!!!

if __name__ == '__main__':
    log.info('Starting the text comparison service')
    try:
        # get amazon data and clean it
        list_without_empty_amazon = handle_amazon_logic()
        # search the items in alibaba
        alibaba_results = handle_alibaba_search(list_without_empty_amazon)
        # clean the search results before acc eval
        clean_alibaba_results_list = clean_alibaba_results(alibaba_results)
        # eval acc
        results_df = eval_naive_score(list_without_empty_amazon, clean_alibaba_results_list)
        # save results
        results_df.to_csv('results.csv', sep=',', index=False)
    except Exception as e:
        log.error(e)
