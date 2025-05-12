import os
from flask import Flask, request, jsonify
from generateOrder import output
from generateBackOrder import generate
from generateInvoice import printInvoice
from generateDeletedOrder import print_deleted_order
from flask_cors import CORS
# Get the absolute path to the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the full path to the certificate and private key files
# cert_path = os.path.join(script_dir, 'cert.com.crt')
# key_path = os.path.join(script_dir, 'cert.com.key')

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
    uso        = headers.get('USO')
    abono      = headers.get('ABONO')
    cuerpo     = headers.get('CUERPO')
    cliente    = headers.get('CLIENTE')
    rif        = headers.get('RIF')

    # Verifica si se proporcionó la dirección IP
    if not printer_ip:
        return jsonify({"error": "No se proporcionó la dirección IP de la impresora"}), 400

    # Obtén los datos JSON de la solicitud
    if request.is_json:
       data = request.get_json()
    else:
        return jsonify({"error": "La solicitud no contiene datos JSON"}), 403

    # Llama al método 'output' con la dirección IP y los datos
    try:
        if(uso == 'PENDIENTE'):
            generate(printer_ip, data, mesero, abono)
        if(uso == 'FACTURA'):
            print(printer_ip, data, cuerpo, mesero, uso)
        if(uso == 'ORDEN ELIMINADA' or uso == 'PRODUCTO ELIMINADO'):
            orderId   = headers.get('Order_Id')
            print_deleted_order(orderId, printer_ip, data, mesa, mesero, uso)
        else:  
            output(data, mesa, mesero)
        return jsonify({"message": "Datos JSON recibidos y enviados a la impresora correctamente"}), 200
    except Exception as e: 
        return jsonify({"message": f"Error de impresión: {str(e)}"}), 500
@app.route('/imprimir-factura', methods=['POST'])
def invoice():
    # Obtén los datos JSON de la solicitud
    if request.is_json:
       data = request.get_json()
    else:
        return jsonify({"error": "La solicitud no contiene datos JSON"}), 403

    try:
        printInvoice(data)
        return jsonify({"message": "Datos JSON recibidos y enviados a la impresora correctamente"}), 200
    except Exception as e: 
        return jsonify({"message": f"Error de impresión: {str(e)}"}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)