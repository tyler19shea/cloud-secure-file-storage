import logging

logging.basicConfig(filename='access.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def log_access(user, filename):
    logging.info(f'User {user} accessed file {filename}')

def log_error(message):
    logging.error(message)