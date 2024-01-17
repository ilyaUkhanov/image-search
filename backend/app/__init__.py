from dotenv import load_dotenv
import os

# Loads the environment variables defined in the .env file
load_dotenv()

# Defining the root directory environment variable
# @ref https://stackoverflow.com/questions/25389095/python-get-path-of-root-project-structure
os.environ["ROOT_DIR"] = os.path.dirname(os.path.abspath(__file__))