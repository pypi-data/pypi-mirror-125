"""CLI (Command Line Interface) module."""

import sys
from typing import Optional

from click import option
from flask import Flask
from flask.cli import AppGroup

from notelist.tools import get_uuid, get_hash
from notelist.schemas.users import UserSchema
from notelist.db import db


# Option descriptions
des_username = "Username."
des_password_1 = "Password."
des_password_2 = "Repeat password."
des_admin = "Whether the user is an administrator or not."
des_enabled = "Whether the user is enabled or not."
des_name = "Name."
des_email = "E-mail address."

# CLI objects
db_cli = AppGroup("db")
user_cli = AppGroup("user")

# Schemas
schema = UserSchema()


@db_cli.command("setup")
def setup_db():
    """Initialize the database."""
    try:
        db.setup()
    except Exception as e:
        sys.exit(f"Error: {e}")


@user_cli.command("create")
@option("--username", required=True, help=des_username)
@option(
    "--password", prompt=True, confirmation_prompt=des_password_2,
    hide_input=True, help=des_password_1
)
@option("--admin", default=False, help=des_admin)
@option("--enabled", default=False, help=des_enabled)
@option("--name", help=des_name)
@option("--email", help=des_email)
def create_user(
    username: str, password: str, admin: bool, enabled: bool,
    name: Optional[str], email: Optional[str]
):
    """Create a user."""
    if db.users.get_by_username(username):
        sys.exit("Error: User already exists.")

    user = {
        "id": get_uuid(),
        "username": username,
        "password": password,
        "admin": admin,
        "enabled": enabled
    }

    if name is not None:
        user["name"] = name

    if email is not None:
        user["email"] = email

    try:
        user = schema.load(user)
        user["password"] = get_hash(password)
        db.users.put(user)
    except Exception as e:
        sys.exit(f"Error: {e}")

    print("User created")


def add_commands(app: Flask):
    """Add the Flask commands.

    :param app: Flask application object.
    """
    app.cli.add_command(db_cli)
    app.cli.add_command(user_cli)
