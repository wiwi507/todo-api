from flask import Flask, jsonify, request, abort

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Aprender CI/CD",          "done": False},
    {"id": 2, "title": "Configurar GitHub Actions", "done": False},
]


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks})


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or "title" not in data:
        abort(400)
    new_task = {
        "id":    len(tasks) + 1,
        "title": data["title"],
        "done":  data.get("done", False),
    }
    tasks.append(new_task)
    return jsonify(new_task), 201


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        abort(404)
    return jsonify(task)


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        abort(404)
    tasks.remove(task)
    return jsonify({"result": "Task deleted"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)