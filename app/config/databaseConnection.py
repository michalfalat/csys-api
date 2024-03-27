import os

def get_database_connection_string():
    database_connector = os.environ['DB_CONNECTOR']
    database_username = os.environ['DB_USER']
    database_password = os.environ['DB_PASSWORD']
    database_ip       = os.environ['DB_IP']
    database_name     = os.environ['DB_NAME']
    database_port     = os.environ['DB_PORT']
    return '{0}://{1}:{2}@{3}:{4}/{5}'.format(database_connector, database_username, database_password, database_ip, database_port, database_name)