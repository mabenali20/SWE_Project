from flask import Flask, request, jsonify, render_template
import uuid
from datetime import datetime

app = Flask(__name__)

tasks = []

@app.route("/")
def home():
    return "Welcome To Our Project!"
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    if not data or not data.get("title") or str(data.get("title")).strip() == "":
        return jsonify({"error": "Task title is required"}), 400

    task = {
        "id": str(uuid.uuid4()),
        "title": data["title"].strip(),
        "completed": False,
        "priority": data.get("priority", "normal"), # أولوية المهمة
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    tasks.append(task)
    return jsonify(task), 201

# مسار التحديث الشامل (لتغيير الحالة، أو تعديل النص، أو تغيير الأولوية)
@app.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json or {}
    for task in tasks:
        if task["id"] == task_id:
            if "completed" in data:
                task["completed"] = data["completed"]
            if "title" in data and data["title"].strip() != "":
                task["title"] = data["title"].strip()
            if "priority" in data:
                task["priority"] = data["priority"]
            return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    # ميزة حذف كل المهام المكتملة مرة واحدة
    if task_id == "completed":
        tasks = [t for t in tasks if not t["completed"]]
        return jsonify({"message": "Completed tasks deleted"}), 200

    # حذف مهمة محددة
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[i]
            return jsonify({"message": "Task deleted"}), 200

    return jsonify({"error": "Task not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)