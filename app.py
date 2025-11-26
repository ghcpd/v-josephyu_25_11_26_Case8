import os
from flask import Flask, jsonify, request, abort

from models import db, Project, Task


app = Flask(__name__)


def init_database(flask_app: Flask) -> None:
    """Initialize SQLAlchemy with the configured database URL.

    Prefers DATABASE_URL (as documented) and falls back to DB_URL. If neither
    is provided, defaults to a local sqlite file `project_manager.db` to
    simplify onboarding.
    """

    database_url = (
        os.environ.get("DATABASE_URL")
        or os.environ.get("DB_URL")
        or "sqlite:///project_manager.db"
    )

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()


init_database(app)


@app.route("/health", methods=["GET"])
def health() -> dict:
    return {"status": "ok"}


@app.route("/projects", methods=["GET"])
@app.route("/api/projects", methods=["GET"])
def list_projects():
    projects = Project.query.all()
    data = [
        {
            "id": project.id,
            "name": project.name,
            "owner_email": project.owner_email,
        }
        for project in projects
    ]
    return jsonify(data)


@app.route("/projects", methods=["POST"])
@app.route("/api/projects", methods=["POST"])
def create_project():
    payload = request.get_json(force=True) or {}
    name = payload.get("name")
    owner_email = payload.get("owner_email") or payload.get("owner")

    if not name or not owner_email:
        return jsonify({"error": "Missing 'name' or 'owner_email'"}), 400

    project = Project(name=name, owner_email=owner_email)
    db.session.add(project)
    db.session.commit()

    return (
        jsonify(
            {
                "id": project.id,
                "name": project.name,
                "owner_email": project.owner_email,
            }
        ),
        201,
    )


@app.route("/projects/<int:project_id>/tasks", methods=["GET"])
@app.route("/api/projects/<int:project_id>/tasks", methods=["GET"])
def list_tasks(project_id: int):
    tasks = db.session.query(Task).filter_by(project_id=project_id).all()
    return jsonify(
        [
            {"id": task.id, "title": task.title, "status": task.status}
            for task in tasks
        ]
    )


@app.route("/projects/<int:project_id>/tasks", methods=["POST"])
@app.route("/api/projects/<int:project_id>/tasks", methods=["POST"])
def create_task(project_id: int):
    payload = request.get_json(force=True) or {}
    title = payload.get("title")
    status = payload.get("status", "todo")

    if not title:
        return jsonify({"error": "Missing 'title'"}), 400

    project = db.session.get(Project, project_id)
    if not project:
        abort(404, description="Project not found")

    task = Task(title=title, status=status, project=project)
    db.session.add(task)
    db.session.commit()

    return (
        jsonify(({"id": task.id, "title": task.title, "status": task.status})),
        201,
    )
