import logging

LOGGER_NAME = "Compare_Alibaba_to_Amazon"

# create logger
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG)

# create console handler and set level to INFO
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)
logger.addHandler(ch)
