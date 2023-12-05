from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    string_field = db.Column(db.String(100))
    number_field = db.Column(db.Float)
    date_field = db.Column(db.Date)

    def __init__(self, string_field, number_field, date_field):
        self.string_field = string_field
        self.number_field = number_field
        self.date_field = date_field


@app.route('/')
def index():
    records = Record.query.all()
    return render_template('index.html', records=records)


@app.route('/add', methods=['POST'])
def add():
    string_field = request.form['string_field']
    number_field = request.form['number_field']
    date_field = request.form['date_field']

    record = Record(string_field, number_field, date_field)
    db.session.add(record)
    db.session.commit()

    return redirect('/')


@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    record = Record.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return redirect('/')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    record = Record.query.get(id)

    if request.method == 'POST':
        record.string_field = request.form['string_field']
        record.number_field = request.form['number_field']
        record.date_field = request.form['date_field']
        db.session.commit()

        return redirect('/')

    return render_template('edit.html', record=record)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
