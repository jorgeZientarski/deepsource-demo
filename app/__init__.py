from __future__ import annotations

from flask import Flask

from .repositories import RepositoryContainer
from .routes.candidates import candidates_bp
from .routes.health import health_bp
from .routes.jobs import jobs_bp
from .routes.match import match_bp


def create_app(config: dict | None = None) -> Flask:
    """Application factory used by tests and production."""
    app = Flask(__name__)

    if config:
        app.config.update(config)

    # Each app instance receives its own in-memory stores.
    app.config["repositories"] = RepositoryContainer()

    register_blueprints(app)
    return app


def register_blueprints(app: Flask) -> None:
    """Register all application blueprints."""
    app.register_blueprint(health_bp)
    app.register_blueprint(candidates_bp, url_prefix="/candidates")
    app.register_blueprint(jobs_bp, url_prefix="/jobs")
    app.register_blueprint(match_bp, url_prefix="/match")
