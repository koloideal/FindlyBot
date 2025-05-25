from database.dao.initialize_database_dao import InitializeDatabaseDAO
from database.connect_to_database import DatabaseConnection
from utils.get_config import GetConfig


config: dict = GetConfig.get_database_config()
host: str = config["host"]
user: int = config["user"]
password: str = config["password"]
database: str = config["database"]
port: int = config["port"]


def initial_database_setup() -> None:
    InitializeDatabaseDAO.create_database(host=host,
                                          user=user,
                                          password=password,
                                          port=port)
    DatabaseConnection(host=host,
                       user=user,
                       password=password,
                       database=database,
                       port=port)
    InitializeDatabaseDAO().create_tables()

