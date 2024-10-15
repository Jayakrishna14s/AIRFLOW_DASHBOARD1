from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure the database URI (Airflow metadata database connection)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql+psycopg2://airflow:airflow@postgres/airflow')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a model for the dag_run table in the Airflow database
class DagRun(db.Model):
    __tablename__ = 'dag_run'
    id = db.Column(db.Integer, primary_key=True)
    dag_id = db.Column(db.String)
    execution_date = db.Column(db.DateTime)
    state = db.Column(db.String)

@app.route('/')
def index():
    # Query the dag_run table to get the DAG run statuses
    dag_runs = DagRun.query.all()  # Limit to 10 results for display purposes
    return render_template('dag_status.html', dag_runs=dag_runs)

if __name__ == '__main__':
    app.run(debug=True)
