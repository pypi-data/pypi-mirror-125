"""DynamoDB package."""

from typing import Optional

import boto3

from notelist.db.base import DbManager
from notelist.db.dynamodb.users import DynamoDbUserManager
from notelist.db.dynamodb.notebooks import DynamoDbNotebookManager
from notelist.db.dynamodb.notes import DynamoDbNoteManager
from notelist.db.dynamodb.blocklist import DynamoDbBlockListManager


class DynamoDbManager(DbManager):
    """DynamoDB manager."""

    def __init__(
        self, us_tab: str, nb_tab: str, no_tab: str, bl_tab: str,
        ep: Optional[str] = None, reg: Optional[str] = None,
        aki: Optional[str] = None, sak: Optional[str] = None,
        st: Optional[str] = None
    ):
        """Initialize instance.

        :param us_tab: DynamoDB users table name. E.g. "users".
        :param nb_tab: DynamoDB notebooks table name. E.g. "notebook".
        :param no_tab: DynamoDB notes table name. E.g. "notes".
        :param bl_tab: DynamoDB block list table name. E.g. "blocklist".
        :param ep: AWS endpoint URL.
        :param reg: AWS region name.
        :param aki: AWS Acess Key ID.
        :param sak: AWS Secret Access Key.
        :param st: AWS Session Token.
        """
        options = {}

        if ep is not None:
            options["endpoint_url"] = ep

        if reg is not None:
            options["region_name"] = reg

        if aki is not None:
            options["aws_access_key_id"] = aki

        if sak is not None:
            options["aws_secret_access_key"] = sak

        if st is not None:
            options["aws_session_token"] = st

        # AWS interfaces
        client = boto3.client("dynamodb", **options)
        res = boto3.resource("dynamodb", **options)

        # Managers
        self._users = DynamoDbUserManager(self, client, res, us_tab)
        self._notebooks = DynamoDbNotebookManager(self, client, res, nb_tab)
        self._notes = DynamoDbNoteManager(self, client, res, no_tab)
        self._blocklist = DynamoDbBlockListManager(self, client, res, bl_tab)

    def setup(self):
        """Initialize the database."""
        print("Creating DynamoDB tables...")

        self._users.setup()
        self._notebooks.setup()
        self._notes.setup()
        self._blocklist.setup()

        print("Done")

    @property
    def users(self) -> DynamoDbUserManager:
        """Return the user data manager.

        :return: `DynamoDbUserManager` instance.
        """
        return self._users

    @property
    def notebooks(self) -> DynamoDbNotebookManager:
        """Return the notebook data manager.

        :return: `DynamoDbNotebookManager` instance.
        """
        return self._notebooks

    @property
    def notes(self) -> DynamoDbNoteManager:
        """Return the note data manager.

        :return: `DynamoDbNoteManager` instance.
        """
        return self._notes

    @property
    def blocklist(self) -> DynamoDbBlockListManager:
        """Return the block list manager.

        :return: `DynamoDbBlockListManager` instance.
        """
        return self._blocklist
