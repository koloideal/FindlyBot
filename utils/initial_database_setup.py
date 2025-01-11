from database.dao.initialize_database_dao import InitializeDatabaseDAO
from database.connect_to_database import DatabaseConnectionSingleton
from utils.get_config import GetConfig


config: dict = GetConfig.get_database_config()
host: str = config["host"]
user: int = config["user"]
password: str = config["password"]
database: str = config["database"]


def initial_database_setup() -> None:
    InitializeDatabaseDAO.create_database(host=host,
                                          user=user,
                                          password=password)
    DatabaseConnectionSingleton(host=host,
                                user=user,
                                password=password,
                                database=database)
    InitializeDatabaseDAO().create_tables()

