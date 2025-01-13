import mysql.connector
from mysql.connector.errors import DatabaseError
from mysql.connector.errors import ProgrammingError
from logging import getLogger, Logger


main_logger: Logger = getLogger('root')


class DatabaseConnectionSingleton:
    _kwargs = None
    _instance = None

    def __new__(cls, **kwargs):

        if cls._instance is None:
            if not all(kwargs.values()) or (len(set(kwargs.keys()) - {'host', 'password', 'user', 'database', 'port'}) > 0):
                raise TypeError("Incorrect arguments in initializing")
            else:
                cls._kwargs = kwargs

            try:
                mysql.connector.connect(**DatabaseConnectionSingleton._kwargs)
            except ProgrammingError as e:
                main_logger.error(f"Error connecting to database: {e}")
                raise
            except DatabaseError as e:
                main_logger.error(f"Error connecting to database: {e}")
                raise
            else:
                cls._instance = super(DatabaseConnectionSingleton, cls).__new__(cls)

        return cls._instance

    def __enter__(self):
        self.connection = mysql.connector.connect(**DatabaseConnectionSingleton._kwargs)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()

    @classmethod
    def __del__(cls):
        if cls._instance:
            main_logger.critical("Delete DatabaseConnectionSingleton instance")
            cls._instance = None
            cls._kwargs = None

