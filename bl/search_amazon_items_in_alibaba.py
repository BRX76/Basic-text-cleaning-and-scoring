import logging

from config import LOGGER_NAME
from bl.get_data import alibaba_get_search_result_titles, parse_alibaba_search_result

log = logging.getLogger(LOGGER_NAME)


def handle_alibaba_search(list_without_empty_amazon):
    log.info('Getting results from alibaba, this may take some time.')
    alibaba_results = []
    results_counter = 1
    for item in list_without_empty_amazon:
        # TODO: some of the strings are still longer then 50 chars - fix it.
        try:
            # TODO: Use multi threading for the io operation
            search_result = alibaba_get_search_result_titles(search_string=item)
            log.info('Got result {} from alibaba! ONly {} to go'.
                     format(str(results_counter), str(len(list_without_empty_amazon)-results_counter)))

            parsed_search_result = parse_alibaba_search_result(search_result)
            alibaba_results.append(parsed_search_result)
            results_counter += 1
        except Exception as e:
            log.info("Couldn't get a search result from Ali! This is the exception: {}".format(e))
            pass
    return alibaba_results
