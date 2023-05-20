from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="db_teste"
)

@app.route('/api/registros', methods=['GET'])
def obtener_registros():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Pessoas")
    registros = cursor.fetchall()
    cursor.close()
    return jsonify(registros)

@app.route('/api/registros', methods=['POST'])
def crear_registro():
    data = request.get_json()
    cursor = db.cursor()
    cursor.execute("INSERT INTO Pessoas (nome, horario) VALUES (%s, %s)", (data['nome'], data['horario']))
    db.commit()
    cursor.close()
    return jsonify({'message': 'Registro creado'})

@app.route('/api/registros/<nome>', methods=['GET'])
def obtener_registro(nome):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Pessoas WHERE nome = %s", (nome,))
    registro = cursor.fetchone()
    cursor.close()
    if registro:
        return jsonify(registro)
    else:
        return jsonify({'message': 'Registro no encontrado'})

@app.route('/api/registros/<nome>', methods=['PUT'])
def actualizar_registro(nome):
    data = request.get_json()
    cursor = db.cursor()
    cursor.execute("UPDATE Pessoas SET nome = %s, horario = %s WHERE id = %s", (data['nome'], data['horario'], id))
    db.commit()
    cursor.close()
    return jsonify({'message': 'Registro actualizado'})

@app.route('/api/registros/<nome>', methods=['DELETE'])
def eliminar_registro(nome):
    cursor = db.cursor()
    cursor.execute("DELETE FROM Pessoas WHERE nome = %s", (nome,))
    db.commit()
    cursor.close()
    return jsonify({'message': 'Registro eliminado'})

if __name__ == '__main__':
    app.run()
