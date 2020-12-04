import requests
import json
import logging

import json

from config import LOGGER_NAME
from common.utils.helpful_objects import AmazonItem, AlibabaItem

log = logging.getLogger(LOGGER_NAME)


def alibaba_get_search_result_titles(search_string):
    # Alibaba string search is limited to 50 char max
    search_text = search_string.replace(" ", "+")[:50]
    url = f"https://open-s.alibaba.com/openservice/" \
        f"galleryProductOfferResultViewService?appName=" \
        f"magellan&appKey=a5m1ismomeptugvfmkkjnwwqnwyrhpb1&" \
        f"searchweb=Y&fsb=y&IndexArea=product_en&CatId=&SearchText={search_text}"
    response = requests.get(url=url)
    if response.status_code == 200:
        try:
            response_json = json.loads(response.text)
            log.info("got the following response: ".format(json.dumps(response_json)))
            return {str(x['information']['id']): x['information']['puretitle']
                    for x in response_json['data']['offerList']}
        except Exception as e:
            log.error('error while getting data from Alibaba! This is the error : {}'.format(e))
            pass


def parse_alibaba_search_result(result):
    list_of_items = []
    for item in result:
        list_of_items.append(AlibabaItem(title=result[item]))
    return list_of_items


def enum_amazon_items(items_file_path):
    log.info('Getting amazon items')
    with open(items_file_path, "r", encoding='utf-8') as f:
        items_dict = json.load(f)
        parsed_items = []
        for item in items_dict.items():
            try:
                current_item = parse_amazon_item(item)
                parsed_items.append(current_item)
            except Exception as e:
                log.error('Something went wrong while parsing the amazon item! This is the item '
                          '{} and this is the error {}'.format(str(item[0]), e))
                pass
    return parsed_items


def parse_amazon_item(item):
    current_item = AmazonItem(title=item[1]['title'],
                              description=item[1]['description'],
                              catagories=concat_list_values_to_string(item[1]['catagories']),
                              details=concat_dict_values_to_string(item[1]['details']))
    return current_item


def concat_dict_values_to_string(x):
    temp_list = []
    for value in x.values():
        temp_list.append(value)
    return concat_list_values_to_string(temp_list)


def concat_list_values_to_string(x):
    return ' '.join(x)
