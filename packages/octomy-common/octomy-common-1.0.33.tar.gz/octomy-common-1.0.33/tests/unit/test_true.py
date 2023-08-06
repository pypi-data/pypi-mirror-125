import pprint
import logging
import os

from fk.db.DatabaseConnection import DatabaseConnection

logger = logging.getLogger(__name__)


def test_true():
    logger.info("Dummy unit test")
    return True


def test_db_get_config_has():
    configs = {"empty:": ({}, ""), "hello:": ({"db-hostname": "hello.com", "db-port": "1234", "db-username": "arnold", "db-password": "secret123", "db-database": "mydb"}, "F12F52B73358C297F47A80768ABDFADF20D021F6A20E9929178908F981B75FA1")}
    for name, pack in configs.items():
        logger.info(f"NAME:{name}")
        config, expected = pack
        logger.info(f"config:{config}")
        logger.info(f"expected:{expected}")
        actual = DatabaseConnection.get_config_hash(config)
        logger.info(f"actual:{actual}")
        assert actual == expected


def _test_db_get_same_twice():
    config = {"db-hostname": "hello.com", "db-port": "1234", "db-username": "arnold", "db-password": "secret123", "db-database": "mydb"}
    db1 = DatabaseConnection.get_connection(config)
    db2 = DatabaseConnection.get_connection(config)
    assert db1 == db2
