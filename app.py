import os
from flask import Flask, jsonify, request

from models import db, Project, Task


app = Flask(__name__)


def init_database(flask_app: Flask) -> None:
    # Accept the widely-used DATABASE_URL env var (matches README/tutorial)
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("Missing DB_URL environment variable")

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()


init_database(app)


@app.route("/health", methods=["GET"])
def health() -> dict:
    return jsonify({"status": "ok"})


@app.route("/projects", methods=["GET"])
def list_projects():
    projects = Project.query.all()
    # Return owner as "owner_email" to match tutorial examples in the README
    data = [
        {"id": project.id, "name": project.name, "owner_email": project.owner}
        for project in projects
    ]
    return jsonify(data)


@app.route("/projects", methods=["POST"])
def create_project():
    payload = request.get_json(force=True)
    # Support both "owner" and "owner_email" keys so examples are flexible
    name = payload["name"]
    owner = payload.get("owner") or payload.get("owner_email")

    project = Project(name=name, owner=owner)
    db.session.add(project)
    db.session.commit()

    return (
        jsonify({"id": project.id, "name": project.name, "owner_email": project.owner}),
        201,
    )


@app.route("/projects/<int:project_id>/tasks", methods=["GET"])
def list_tasks(project_id: int):
    tasks = db.session.query(Task).filter_by(project_id=project_id).all()
    return jsonify([{"id": task.id, "title": task.title, "status": task.status} for task in tasks])
