
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def setup_database():
    con = sqlite3.connect("items.db")
    con.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_type TEXT,
            name TEXT,
            category TEXT,
            location TEXT,
            description TEXT,
            status TEXT DEFAULT 'Open'
        )
    """)
    con.commit()
    con.close()

@app.route("/", methods=["GET", "POST"])
def home():
    con = sqlite3.connect("items.db")
    con.row_factory = sqlite3.Row

    if request.method == "POST":
        item_type = request.form["item_type"]
        name = request.form["name"]
        category = request.form["category"]
        location = request.form["location"]
        description = request.form["description"]

        con.execute("""
            INSERT INTO items
            (item_type, name, category, location, description)
            VALUES (?, ?, ?, ?, ?)
        """, (item_type, name, category, location, description))

        con.commit()
        con.close()
        return redirect("/")

    search = request.args.get("search", "")

    items = con.execute(
        """SELECT * FROM items
        WHERE name LIKE ? OR category LIKE ? OR location LIKE ?
        ORDER BY id DESC""",
        (f"%{search}%", f"%{search}%", f"%{search}%")
    ).fetchall()

    con.close()
    return render_template("index.html", items=items, search=search)

@app.route("/returned/<int:item_id>", methods=["POST"])
def returned(item_id):
    con = sqlite3.connect("items.db")
    con.execute(
        "UPDATE items SET status='Returned' WHERE id=?",
        (item_id,)
    )
    con.commit()
    con.close()
    return redirect("/")

setup_database()

if __name__ == "__main__":
    app.run(debug=True)
