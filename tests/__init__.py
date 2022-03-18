import logging
import logging.config
from app.log import LOGGING
logging.config.dictConfig(LOGGING)

# python -m pytest --cov=. tests/ --cov-report term
