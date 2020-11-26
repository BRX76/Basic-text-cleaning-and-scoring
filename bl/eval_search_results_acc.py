import logging
import pandas as pd

from config import LOGGER_NAME
from bl.score_search_result import naive_score_amazon_vs_alibaba

log = logging.getLogger(LOGGER_NAME)


def eval_naive_score(list_without_empty_amazon, clean_alibaba_results_list):
    log.info('Scoring alibaba results per amazon item')
    list_of_dfs = []
    for amazon_item, alibaba_result in zip(list_without_empty_amazon, clean_alibaba_results_list):
        scores_df = naive_score_amazon_vs_alibaba(amazon_item=amazon_item, alibaba_result=alibaba_result)
        scores_df = scores_df.sort_values('scores', ascending=False)
        list_of_dfs.append(scores_df)

    results_df = pd.concat(list_of_dfs).reset_index(drop=True)
    return results_df
