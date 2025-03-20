from flask import Flask, jsonify, request, render_template_string
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('tanks.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET'])
def list_endpoints():
    routes = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and rule.endpoint != "static" and "<int:id>" not in rule.rule:
            routes.append({
                'url': rule.rule
            })

    html_content = "<h1>Tank.ly API Endpoints</h1>"
    html_content += "<p>Click to view data.</p>"
    html_content += "<p>See individual tanks by making a curl request or manually navigating to /tanks/{id}.</p><ul>"
    for route in routes:
        html_content += f'<li><a href="{route["url"]}">{route["url"]}</a></li>'
    html_content += "</ul>"

    return render_template_string(html_content)

@app.route('/api/tanks', methods=['GET'])
def get_tanks():
    conn = get_db_connection()
    tanks = conn.execute('SELECT tank.id, tank.name, country.name AS country, type.name AS type, tank.year_mfg FROM tank LEFT JOIN country ON country.id = tank.country_id LEFT JOIN type on type.id = tank.type_id').fetchall()
    conn.close()
    return jsonify([dict(row) for row in tanks])

@app.route('/api/tanks/<int:id>', methods=['GET'])
def get_tank(id):
    conn = get_db_connection()
    query = '''
    SELECT tank.id, tank.name, country.name AS country, type.name AS type, tank.year_mfg
    FROM tank
    LEFT JOIN country ON country.id = tank.country_id
    LEFT JOIN type ON type.id = tank.type_id
    WHERE tank.id = ?
    '''
    tank = conn.execute(query, (id,)).fetchone()
    conn.close()
    return jsonify([dict(tank)])

@app.route('/api/countries', methods=['GET'])
def get_countries():
    conn = get_db_connection()
    countries = conn.execute('SELECT * FROM country').fetchall()
    conn.close()
    return jsonify([dict(row) for row in countries])

@app.route('/api/types', methods=['GET'])
def get_types():
    conn = get_db_connection()
    types = conn.execute('SELECT * FROM type').fetchall()
    conn.close()
    return jsonify([dict(row) for row in types])

@app.route('/api/types', methods=['POST'])
def add_tank():
    new_tank = request.json
    conn = get_db_connection()
    conn.execute('INSERT INTO tank (name) VALUES (?)', (new_tank['name'],))
    conn.commit()
    conn.close()
    return jsonify({"status": "added"}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
