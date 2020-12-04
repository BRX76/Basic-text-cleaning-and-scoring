import logging

from config import LOGGER_NAME, NUMBER_OF_ITEMS
from bl.get_data import alibaba_get_search_result_titles, parse_alibaba_search_result

log = logging.getLogger(LOGGER_NAME)


def handle_alibaba_search(list_without_empty_amazon):
    log.info('Getting results from alibaba, this may take some time.')
    alibaba_results = []
    number_of_items = min(len(list_without_empty_amazon), NUMBER_OF_ITEMS)

    log.info('Getting results from alibaba')
    for item in list_without_empty_amazon[:number_of_items]:
        # Add the task to our list of things to do via async
        try:
            search_result = alibaba_get_search_result_titles(search_string=item)
            alibaba_results.append(search_result)

        except Exception as e:
            log.info("Couldn't get a search result from Ali! This is the exception: {}".format(e))
            pass

    parsed_search_result = []
    for result in alibaba_results:
        try:
            parsed_search_result.append(parse_alibaba_search_result(result))
        except Exception as e:
            log.error("Couldnt parse the results with this error: {)".format(e))

    return parsed_search_result
