import logging

BASE_DOMAIN = "https://starwars.fandom.com"
BASE_DOMAIN_FORMAT = BASE_DOMAIN + "{}"
START_PAGE = f"{BASE_DOMAIN}/ru/wiki/Служебная:Все_страницы"
CREATOR_REQUEST_PARAM = "?action=history&limit=1&dir=prev"
ARTICLES_DIR_PATH = "articles"
NUM_CPU = 64
LOG_LEVEL = logging.INFO
