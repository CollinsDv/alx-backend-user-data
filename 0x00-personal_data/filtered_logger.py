#!/usr/bin/env python3
"""module: filtered_logger
"""
import logging
import re
from typing import List
import mysql.connector
import os
# Write a function called filter_datum that returns the log message obfuscated:
#
#     Arguments:
#         fields: a list of strings representing all fields to obfuscate
#         redaction: a string representing by what the field will be obfuscated
#         message: a string representing the log line
#         separator: a string representing by which character is separating all
#            fields in the log line (message)
#         The function should use a regex to replace occurrences of certain
#            field values.
#         filter_datum should be less than 5 lines long and
#            use re.sub to perform
#            the substitution with a single regex.
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    pattern = rf"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, rf"\1={redaction}", message)


"""
Update the class to accept a list of strings fields constructor
argument.

Implement the format method to filter values in incoming log records
using filter_datum. Values for fields in fields should be filtered.

DO NOT extrapolate FORMAT manually. The format method should be less
than 5 lines long.
"""


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Redacting Formatter class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format function"""
        record.msg = filter_datum(
             self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super().format(record)


"""
Implement a get_logger function that takes no arguments and returns
a logging.Logger object.

The logger should be named "user_data" and only log up to logging.INFO
level. It should not propagate messages to other loggers. It should
have a StreamHandler with RedactingFormatter as formatter.

Create a tuple PII_FIELDS constant at the root of the module
containing the fields from user_data.csv that are considered PII.
PII_FIELDS can contain only 5 fields - choose the right list of
fields that can are considered as “important” PIIs or information
that you must hide in your logs. Use it to parameterize the formatter.
"""


def get_logger() -> logging.Logger:
    """ Get Logger function"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(handler)
    return logger


"""
Database credentials should NEVER be stored in code or checked
into version control. One secure option is to store them as
environment variable on the application server.

In this task, you will connect to a secure holberton database
to read a users table. The database is protected by a username
and password that are set as environment variables on the server
named PERSONAL_DATA_DB_USERNAME (set the default as “root”),
PERSONAL_DATA_DB_PASSWORD (set the default as an empty string)
and PERSONAL_DATA_DB_HOST (set the default as “localhost”).

The database name is stored in PERSONAL_DATA_DB_NAME.

Implement a get_db function that returns a connector to the database
(mysql.connector.connection.MySQLConnection object).

Use the os module to obtain credentials from the environment
Use the module mysql-connector-python to connect to the MySQL
database (pip3 install mysql-connector-python)
"""


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Get DB function"""
    try:
        host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
        user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
        password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
        database = os.getenv('PERSONAL_DATA_DB_NAME', '')

        connection = mysql.connector.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=database
        )
        return connection
    except Exception as e:
        raise e


"""
Implement a main function that takes no arguments and returns nothing.

The function will obtain a database connection using get_db and
retrieve all rows in the users table and display each row under a
filtered format like this:

[HOLBERTON] user_data INFO 2019-11-19 18:37:59,596: name=***;
email=***; phone=***; ssn=***; password=***;
ip=e848:e856:4e0b:a056:54ad:1e98:8110:ce1b;
last_login=2019-11-14T06:16:24;
user_agent=Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1;
WOW64; Trident/5.0; KTXN);

Filtered fields:

name
email
phone
ssn
password
Only your main function should run when the module is executed.
"""


def main():
    """main function"""
    db = get_db()
    logger = get_logger()
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            for row in cursor:
                message = "; ".join(
                    [f"{key}={value}" for key,
                     value in zip(cursor.column_names, row)]) + ";"
                logger.info(message)
    finally:
        db.close()


if __name__ == "__main__":
    main()
