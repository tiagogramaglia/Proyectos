from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error
import logging

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3307,
            user='root',
            password='',
            database='bdminisuperr'
        )
        if connection.is_connected():
            logger.info("Conexión exitosa a la base de datos")
            return connection
        else:
            logger.error("No se pudo establecer la conexión")
            return None
    except Error as e:
        logger.error(f"Error de conexión MySQL: {str(e)}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rubros', methods=['GET'])
def get_rubros():
    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Error de conexión a la base de datos"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, codrubro, rubro FROM rubros')
        rubros = cursor.fetchall()
        return jsonify({"success": True, "data": rubros})
    except Error as e:
        logger.error(f"Error en get_rubros: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()

@app.route('/rubros', methods=['POST'])
def add_rubro():
    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Error de conexión a la base de datos"}), 500

    try:
        data = request.get_json()
        if not data or 'codrubro' not in data or 'rubro' not in data:
            return jsonify({"success": False, "error": "Datos incompletos"}), 400

        if len(data['codrubro']) > 3:
            return jsonify({"success": False, "error": "El código de rubro no puede exceder 3 caracteres"}), 400

        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO rubros (codrubro, rubro) VALUES (%s, %s)',
            (data['codrubro'], data['rubro'])
        )
        conn.commit()

        return jsonify({
            "success": True,
            "message": "Rubro agregado exitosamente",
            "id": cursor.lastrowid
        }), 201
    except Error as e:
        conn.rollback()
        logger.error(f"Error en add_rubro: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()

@app.route('/rubros/<codrubro>', methods=['DELETE'])
def delete_rubro(codrubro):
    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Error de conexión a la base de datos"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM rubros WHERE codrubro = %s', (codrubro,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Rubro no encontrado"}), 404

        return jsonify({"success": True, "message": "Rubro eliminado exitosamente"}), 200
    except Error as e:
        conn.rollback()
        logger.error(f"Error en delete_rubro: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()

@app.route('/articulos', methods=['GET'])
def get_articulos():
    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Error de conexión a la base de datos"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id2, codarticulo, articulo FROM articulos')
        articulos = cursor.fetchall()
        return jsonify({"success": True, "data": articulos})
    except Error as e:
        logger.error(f"Error en get_articulos: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()

@app.route('/articulos', methods=['POST'])
def add_articulo():
    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Error de conexión a la base de datos"}), 500

    try:
        data = request.get_json()
        if not data or 'codarticulo' not in data or 'articulo' not in data:
            return jsonify({"success": False, "error": "Datos incompletos"}), 400

        if len(data['codarticulo']) > 7:
            return jsonify({"success": False, "error": "El código de artículo no puede exceder 7 caracteres"}), 400

        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO articulos (codarticulo, articulo) VALUES (%s, %s)',
            (data['codarticulo'], data['articulo'])
        )
        conn.commit()

        return jsonify({
            "success": True,
            "message": "Artículo agregado exitosamente",
            "id": cursor.lastrowid
        }), 201
    except Error as e:
        conn.rollback()
        logger.error(f"Error en add_articulo: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()

@app.route('/articulos/<codarticulo>', methods=['DELETE'])
def delete_articulo(codarticulo):
    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Error de conexión a la base de datos"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM articulos WHERE codarticulo = %s', (codarticulo,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Artículo no encontrado"}), 404

        return jsonify({"success": True, "message": "Artículo eliminado exitosamente"}), 200
    except Error as e:
        conn.rollback()
        logger.error(f"Error en delete_articulo: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()

@app.route('/descripciones', methods=['GET'])
def get_descripciones():
    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Error de conexión a la base de datos"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id3, coddescripcion, descripcion FROM descripcion')
        descripciones = cursor.fetchall()
        return jsonify({"success": True, "data": descripciones})
    except Error as e:
        logger.error(f"Error en get_descripciones: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()

@app.route('/descripciones', methods=['POST'])
def add_descripcion():
    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Error de conexión a la base de datos"}), 500

    try:
        data = request.get_json()
        if not data or 'coddescripcion' not in data or 'descripcion' not in data:
            return jsonify({"success": False, "error": "Datos incompletos"}), 400

        if len(data['coddescripcion']) > 12:
            return jsonify({"success": False, "error": "El código de descripción no puede exceder 12 caracteres"}), 400

        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO descripcion (coddescripcion, descripcion) VALUES (%s, %s)',
            (data['coddescripcion'], data['descripcion'])
        )
        conn.commit()

        return jsonify({
            "success": True,
            "message": "Descripción agregada exitosamente",
            "id": cursor.lastrowid
        }), 201
    except Error as e:
        conn.rollback()
        logger.error(f"Error en add_descripcion: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()

@app.route('/descripciones/<coddescripcion>', methods=['DELETE'])
def delete_descripcion(coddescripcion):
    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "Error de conexión a la base de datos"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM descripcion WHERE coddescripcion = %s', (coddescripcion,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Descripción no encontrada"}), 404

        return jsonify({"success": True, "message": "Descripción eliminada exitosamente"}), 200
    except Error as e:
        conn.rollback()
        logger.error(f"Error en delete_descripcion: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)