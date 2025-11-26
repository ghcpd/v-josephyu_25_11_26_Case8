"""Flask app module alias for CLI usage.

This module exposes the `app` object so you can run:

    flask --app project_manager run --debug

"""

from app import app  # noqa: F401
