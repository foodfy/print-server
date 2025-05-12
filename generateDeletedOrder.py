from escpos.printer import Network
from datetime import datetime
from utils.cleanStrings import cleanStrings 

def print_deleted_order(orderId, ip, data, mesa, gerente, uso):
    timer     = datetime.now()
    hora      = timer.time()
    fechaHora = hora.strftime('%H:%M')
    fecha     = timer.strftime('%d-%m-%Y')
    
    kitchen   = Network(ip)
    kitchen.set(width=2, height=2, align='left', font='B', text_type='B')
    kitchen.text(f"{uso}:")
    kitchen.text("\n\n")
    kitchen.set(width=1, height=1, text_type='B')
    kitchen.text(f"GERENTE: {gerente.upper()}, {mesa.upper()}")
    kitchen.text("\n\n")
    total_orden = 0.00
    for item in data: 
        kitchen.set(width=1, height=1, align='left')
        for key, value in item.items():
            if(key == 'PRODUCTO'):
                articulo = cleanStrings(value.upper())
                kitchen.text(f"{articulo.strip()}\n")
            elif (key == 'PRECIO'):
                total_orden += float(value)  
            elif (key == 'EXTRAS' and value != 'SIN EXTRAS'): 
                kitchen.set(width=1, height=1, align='left', font='B', text_type='B')
                value = 'EXTRAS: [' + value + ']'
                kitchen.text(f"{value}\n")   
    kitchen.text("\n")

    kitchen.set(width=1, height=1, align='left')
    kitchen.text(f"\nTotal: {total_orden}$\n")
    kitchen.text(f"\nHora: {fechaHora}\n")
    kitchen.text(f"\nFecha: {fecha}\n")
    kitchen.text(f"\nPedido ID: {orderId}")
    kitchen.cut()
    # Corta el papel (opcional, depende de tu impresora)
    kitchen.close()
