from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class EnergyUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(50), nullable=False)
    energy_consumed = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/log', methods=['POST'])
def log_energy_usage():
    data = request.get_json()
    new_entry = EnergyUsage(
        device_id=data['device_id'],
        energy_consumed=data['energy_consumed']
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Data logged successfully"}), 201

@app.route('/data', methods=['GET'])
def get_energy_data():
    data = EnergyUsage.query.all()
    result = []
    for entry in data:
        entry_data = {
            'id': entry.id,
            'device_id': entry.device_id,
            'energy_consumed': entry.energy_consumed,
            'timestamp': entry.timestamp
        }
        result.append(entry_data)
    return jsonify(result)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
