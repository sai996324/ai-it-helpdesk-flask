from flask import Flask, abort, flash, redirect, render_template, request, url_for

import classifier
from database import get_db, init_db

app = Flask(__name__)
app.secret_key = "change-this-secret-key"  # change before deploying

STATUSES = ["Open", "In Progress", "Resolved", "Closed"]
PRIORITIES = ["Low", "Medium", "High", "Critical"]
CATEGORIES = ["Network", "Hardware", "Software", "Account Access", "Server/Database", "General"]
AGENTS = ["Unassigned", "Ravi", "Sneha", "Kiran", "Anitha"]  # edit to your team

init_db()


@app.route("/")
def index():
    status = request.args.get("status", "")
    priority = request.args.get("priority", "")
    query = "SELECT * FROM tickets WHERE 1=1"
    params = []
    if status:
        query += " AND status = ?"
        params.append(status)
    if priority:
        query += " AND priority = ?"
        params.append(priority)
    query += (
        " ORDER BY CASE priority WHEN 'Critical' THEN 1 WHEN 'High' THEN 2"
        " WHEN 'Medium' THEN 3 ELSE 4 END, created_at DESC"
    )
    with get_db() as conn:
        tickets = conn.execute(query, params).fetchall()
        counts = {
            row["status"]: row["n"]
            for row in conn.execute("SELECT status, COUNT(*) AS n FROM tickets GROUP BY status")
        }
    return render_template(
        "index.html", tickets=tickets, counts=counts, statuses=STATUSES,
        priorities=PRIORITIES, f_status=status, f_priority=priority,
    )


@app.route("/new", methods=["GET", "POST"])
def new_ticket():
    if request.method == "POST":
        title = request.form["title"].strip()
        description = request.form["description"].strip()
        requester = request.form["requester"].strip()
        if not (title and description and requester):
            flash("Fill in your name, a title and a description.", "error")
            return render_template("new.html"), 400
        category, priority, used_ai = classifier.predict(title, description)
        with get_db() as conn:
            cur = conn.execute(
                "INSERT INTO tickets (title, description, requester, category, priority, ai_suggested)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                (title, description, requester, category, priority, int(used_ai)),
            )
            ticket_id = cur.lastrowid
        flash(f"Ticket #{ticket_id} created. Category: {category}, priority: {priority}.", "ok")
        return redirect(url_for("ticket_detail", ticket_id=ticket_id))
    return render_template("new.html")


@app.route("/ticket/<int:ticket_id>", methods=["GET", "POST"])
def ticket_detail(ticket_id):
    with get_db() as conn:
        ticket = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
        if ticket is None:
            abort(404)
        if request.method == "POST":
            status = request.form["status"]
            priority = request.form["priority"]
            category = request.form["category"]
            assigned = request.form["assigned_to"]
            resolution = request.form.get("resolution", "").strip()
            if status in ("Resolved", "Closed") and not resolution:
                flash("Add a resolution note before resolving or closing a ticket.", "error")
                return render_template(
                    "ticket.html", ticket=ticket, statuses=STATUSES, priorities=PRIORITIES,
                    categories=CATEGORIES, agents=AGENTS,
                ), 400
            conn.execute(
                "UPDATE tickets SET status=?, priority=?, category=?, assigned_to=?, resolution=?,"
                " updated_at=datetime('now') WHERE id=?",
                (status, priority, category,
                 None if assigned == "Unassigned" else assigned, resolution or None, ticket_id),
            )
            flash("Ticket updated.", "ok")
            return redirect(url_for("ticket_detail", ticket_id=ticket_id))
    return render_template(
        "ticket.html", ticket=ticket, statuses=STATUSES, priorities=PRIORITIES,
        categories=CATEGORIES, agents=AGENTS,
    )


if __name__ == "__main__":
    app.run(debug=True)
