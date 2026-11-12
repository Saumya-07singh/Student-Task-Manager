
from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "student"),
        password=os.getenv("DB_PASSWORD", "student123"),
        database=os.getenv("DB_NAME", "tasks")
    )

@app.route("/", methods=["GET", "POST"])
def home():
    db = get_db()
    cursor = db.cursor()

    if request.method == "POST":
        task = request.form["task"]
        cursor.execute(
            "INSERT INTO tasks (task) VALUES (%s)", (task,)
        )
        db.commit()
        cursor.close()
        db.close()
        return redirect("/")

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:task_id>")
def delete(task_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    db.commit()

    cursor.close()
    db.close()

    return redirect("/")

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
