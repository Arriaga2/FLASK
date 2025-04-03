from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "supersecreto"

# URL de la API de FastAPI
FASTAPI_URL = "http://127.0.0.1:3000"

# Ruta formulario
@app.route('/', methods=['GET'])
def home():
    return render_template('registro.html')

# Ruta para la consulta
@app.route('/consulta', methods=['GET'])
def get_usuarios():
    try:
        respuesta = requests.get(f"{FASTAPI_URL}/todoUsuarios")
        respuesta.raise_for_status()
        usuarios = respuesta.json()
        return render_template('consulta.html', usuarios=usuarios)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "No se pudo conectar con la API", "detalle": str(e)}), 500

# Ruta para agregar usuario
@app.route('/usuariosFastAPI', methods=['POST'])
def post_usuario():
    try:
        # Recibir datos del formulario
        usuarioNuevo = {
            "name": request.form['txtNombre'],
            "age": int(request.form['txtEdad']),
            "email": request.form['txtCorreo']
        }

        # Realizar la petición POST a FastAPI
        response = requests.post(f"{FASTAPI_URL}/usuario/", json=usuarioNuevo)

        if response.status_code in [200, 201]:
            flash("Usuario guardado correctamente", "success")
        else:
            flash(f"Error al guardar usuario: {response.json().get('detail', 'Error desconocido')}", "danger")

        return redirect(url_for('home'))

    except requests.exceptions.RequestException as e:
        flash(f"Error de conexión con la API: {str(e)}", "danger")
        return redirect(url_for('home'))

# Ruta para eliminar usuario
@app.route('/eliminar_usuario/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    try:
        respuesta = requests.delete(f"{FASTAPI_URL}/usuario/{id}")
        if respuesta.status_code == 200:
            flash("Usuario eliminado correctamente", "success")
        else:
            flash("Error al eliminar usuario", "danger")
    except requests.exceptions.RequestException as e:
        flash("No se pudo conectar con la API", "danger")
    
    return redirect(url_for('get_usuarios'))

# Ruta para editar usuario
@app.route('/editar_usuario/<int:id>', methods=['GET'])
def editar_usuario(id):
    try:
        respuesta = requests.get(f"{FASTAPI_URL}/usuario/{id}")
        respuesta.raise_for_status()
        usuario = respuesta.json()
        return render_template('editar.html', usuario=usuario)
    except requests.exceptions.RequestException as e:
        flash("No se pudo obtener la información del usuario", "danger")
        return redirect(url_for('get_usuarios'))

# Ruta para actualizar usuario
@app.route('/actualizar_usuario/<int:id>', methods=['POST'])
def actualizar_usuario(id):
    try:
        usuarioActualizado = {
            "name": request.form['txtNombre'],
            "age": int(request.form['txtEdad']),
            "email": request.form['txtCorreo']
        }

        respuesta = requests.put(f"{FASTAPI_URL}/usuarios/{id}", json=usuarioActualizado)  # 👈 Plural corregido


        if respuesta.status_code == 200:
            flash("Usuario actualizado correctamente", "success")
        else:
            flash("Error al actualizar usuario", "danger")
    except requests.exceptions.RequestException as e:
        flash("No se pudo conectar con la API", "danger")
    
    return redirect(url_for('get_usuarios'))

if __name__ == '__main__':
    app.run(debug=True, port=8002)
