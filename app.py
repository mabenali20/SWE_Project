from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = []

@app.route("/")
def home():
    return "Task Manager API Running"


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def add_task():

    data = request.json

    task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "completed": False
    }

    tasks.append(task)

    return jsonify(task)


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return jsonify(task)

    return jsonify({"message": "Task not found"}), 404


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return jsonify({"message": "Task deleted"})

    return jsonify({"message": "Task not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)