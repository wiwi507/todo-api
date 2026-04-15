from flask import Flask, jsonify, request, abort, render_template_string

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Aprender CI/CD",          "done": False},
    {"id": 2, "title": "Configurar GitHub Actions", "done": False},
]

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Todo App — CI/CD</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=DM+Mono&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #0a0f1a;
    color: #e2e8f0;
    font-family: 'DM Sans', sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 3rem 1rem;
  }
  body::before {
    content: '';
    position: fixed; inset: 0;
    background:
      linear-gradient(rgba(34,212,123,.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(34,212,123,.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
  }
  .container { width: 100%; max-width: 560px; position: relative; }
  .header { margin-bottom: 2rem; }
  .tag {
    font-family: 'DM Mono', monospace;
    font-size: .7rem; letter-spacing: .1em;
    color: #22d47b;
    background: rgba(34,212,123,.08);
    border: 1px solid rgba(34,212,123,.2);
    padding: .2rem .7rem; border-radius: 99px;
    display: inline-block; margin-bottom: .8rem;
  }
  h1 { font-size: 2rem; font-weight: 700; letter-spacing: -.02em; }
  h1 span { color: #22d47b; }
  .form-card {
    background: #111827;
    border: 1px solid #1e2d40;
    border-radius: 14px;
    padding: 1.2rem;
    margin-bottom: 1.5rem;
    display: flex; gap: .8rem;
  }
  input {
    flex: 1;
    background: #0a0f1a;
    border: 1px solid #1e2d40;
    border-radius: 8px;
    padding: .7rem 1rem;
    color: #e2e8f0;
    font-family: 'DM Sans', sans-serif;
    font-size: .9rem;
    outline: none;
    transition: border-color .2s;
  }
  input:focus { border-color: #22d47b; }
  input::placeholder { color: #374151; }
  button {
    background: #22d47b;
    color: #0a0f1a;
    border: none;
    border-radius: 8px;
    padding: .7rem 1.2rem;
    font-family: 'DM Sans', sans-serif;
    font-weight: 700; font-size: .9rem;
    cursor: pointer;
    transition: opacity .2s;
    white-space: nowrap;
  }
  button:hover { opacity: .85; }
  .tasks { display: flex; flex-direction: column; gap: .6rem; }
  .task {
    background: #111827;
    border: 1px solid #1e2d40;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    display: flex; align-items: center; justify-content: space-between;
    transition: border-color .2s;
    animation: fadeUp .3s ease both;
  }
  .task:hover { border-color: #2a3f5a; }
  .task.done { opacity: .5; }
  .task-left { display: flex; align-items: center; gap: .8rem; }
  .task-check {
    width: 20px; height: 20px;
    border-radius: 50%;
    border: 2px solid #1e2d40;
    cursor: pointer;
    transition: all .2s;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }
  .task-check:hover { border-color: #22d47b; }
  .task-check.checked { background: #22d47b; border-color: #22d47b; }
  .task-check.checked::after { content: '✓'; color: #0a0f1a; font-size: .7rem; font-weight: 700; }
  .task-title { font-size: .9rem; }
  .task-id { font-family: 'DM Mono', monospace; font-size: .65rem; color: #374151; }
  .delete-btn {
    background: transparent;
    color: #374151;
    padding: .3rem .6rem;
    font-size: .8rem;
    border: 1px solid transparent;
    border-radius: 6px;
    transition: all .2s;
  }
  .delete-btn:hover { color: #ff5c5c; border-color: rgba(255,92,92,.3); background: rgba(255,92,92,.08); }
  .empty {
    text-align: center; padding: 3rem;
    color: #374151; font-size: .9rem;
    font-family: 'DM Mono', monospace;
  }
  .footer-info {
    margin-top: 2rem;
    font-family: 'DM Mono', monospace;
    font-size: .65rem; color: #1e2d40;
    text-align: center;
  }
  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
  }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="tag">● live · todo-api-37c3.onrender.com</div>
    <h1>Todo <span>App</span></h1>
  </div>

  <div class="form-card">
    <input type="text" id="input" placeholder="Nueva tarea..." onkeydown="if(event.key==='Enter') addTask()">
    <button onclick="addTask()">+ Agregar</button>
  </div>

  <div class="tasks" id="tasks"></div>
  <div class="footer-info">CI/CD Pipeline · GitHub Actions · Docker · Render</div>
</div>

<script>
  async function loadTasks() {
    const res = await fetch('/tasks');
    const data = await res.json();
    render(data.tasks);
  }

  function render(tasks) {
    const container = document.getElementById('tasks');
    if (tasks.length === 0) {
      container.innerHTML = '<div class="empty">// no hay tareas aún</div>';
      return;
    }
    container.innerHTML = tasks.map(t => `
      <div class="task ${t.done ? 'done' : ''}" id="task-${t.id}">
        <div class="task-left">
          <div class="task-check ${t.done ? 'checked' : ''}" onclick="toggleTask(${t.id}, ${t.done})"></div>
          <div>
            <div class="task-title">${t.title}</div>
            <div class="task-id">#${t.id}</div>
          </div>
        </div>
        <button class="delete-btn" onclick="deleteTask(${t.id})">✕</button>
      </div>
    `).join('');
  }

  async function addTask() {
    const input = document.getElementById('input');
    const title = input.value.trim();
    if (!title) return;
    await fetch('/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title })
    });
    input.value = '';
    loadTasks();
  }

  async function deleteTask(id) {
    await fetch('/tasks/' + id, { method: 'DELETE' });
    loadTasks();
  }

  async function toggleTask(id, done) {
    await fetch('/tasks/' + id, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ done: !done })
    });
    loadTasks();
  }

  loadTasks();
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


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


@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        abort(404)
    data = request.get_json()
    if "done" in data:
        task["done"] = data["done"]
    if "title" in data:
        task["title"] = data["title"]
    return jsonify(task)


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        abort(404)
    tasks.remove(task)
    return jsonify({"result": "Task deleted"})
#prueba para la notificacion


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    