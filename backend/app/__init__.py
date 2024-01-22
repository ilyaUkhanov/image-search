from dotenv import load_dotenv
import os
import logging

# Loads the environment variables defined in the .env file
load_dotenv()

# Defining the root directory environment variable
# @ref https://stackoverflow.com/questions/25389095/python-get-path-of-root-project-structure
os.environ["ROOT_DIR"] = os.path.dirname(os.path.abspath(__file__))

# Configure the Global Logger
LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG, format=LOG_FORMAT)