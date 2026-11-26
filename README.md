# AI-Powered IT Helpdesk & Ticket Management System

A web-based IT helpdesk built with **Python, Flask, SQLite (SQL), HTML and CSS**. Users raise support tickets, an ML model predicts the **category** and **priority**, and agents track, assign and resolve them.

## Features
- Create tickets (name, title, description)
- **AI-based ticket classification and priority prediction** (TF-IDF + Logistic Regression, scikit-learn)
- Ticket tracking with status: Open, In Progress, Resolved, Closed
- Assignment to support agents
- Resolution notes (required before a ticket is resolved or closed)
- Dashboard with status counts and filters by status and priority, sorted by priority

## Tech stack
Python, Flask, SQLite, scikit-learn, HTML, CSS

## Project structure
```
app.py            Flask routes
database.py       SQLite connection and schema
classifier.py     Loads trained models and predicts category/priority
train_model.py    Trains the models and prints test accuracy
data/make_dataset.py   Generates a small starter dataset (data/tickets.csv)
templates/, static/    HTML templates and CSS
```

## Setup
```bash
pip install -r requirements.txt
python data/make_dataset.py     # creates data/tickets.csv
python train_model.py           # trains models and saves them in model/
python app.py                   # open http://127.0.0.1:5000
```

## Note on model accuracy
The included dataset is small and **synthetic** (generated from templates), so the accuracy printed by `train_model.py` is not a real-world number. For realistic results, replace `data/tickets.csv` with real ticket data (columns: `text`, `category`, `priority`) and retrain.

## Future improvements
- Login for agents and users
- Email notifications
- Comments/history on each ticket
- Better model trained on real tickets
