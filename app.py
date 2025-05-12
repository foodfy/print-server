from flask import Flask, request, jsonify
from comanderas import output
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/imprimir', methods=['POST'])
def imprimir():
    # Obtén los encabezados de la solicitud
    headers = request.headers

    # Accede a la dirección IP del encabezado personalizado
    printer_ip = headers.get('X-Printer-IP')
    mesa       = headers.get('MESA')
    mesero     = headers.get('VENDEDOR')

    # Verifica si se proporcionó la dirección IP
    if not printer_ip:
        return jsonify({"error": "No se proporcionó la dirección IP de la impresora"}), 400

    # Obtén los datos JSON de la solicitud
    if request.is_json:
       data = request.get_json()
    else:
        return jsonify({"error": "La solicitud no contiene datos JSON"}), 400
  
    # Llama al método 'output' con la dirección IP y los datos
    try:
        output(printer_ip, data, mesa, mesero)
        return jsonify({"message": "Datos JSON recibidos y enviados a la impresora correctamente"}), 200
    except Exception as e: 
        return jsonify({"message": f"Error de impresión: {str(e)}"}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
