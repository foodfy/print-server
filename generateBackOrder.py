from escpos.printer import Network
from datetime import datetime
from utils.cleanStrings import cleanStrings 

def generate(ip, data, cliente, abono):
    # Inicializa una instancia de la clase Network con la dirección IP de la impresora
    timer     = datetime.now()
    hora      = timer.time()
    fechaHora = hora.strftime('%H:%M')
    fecha     = timer.strftime('%d-%m-%Y')
    
    kitchen   = Network(ip)
    kitchen.set(width=3, height=3, align='left', font='B', text_type='B')
    kitchen.text(f"PENDIENTE:")
    kitchen.text("\n\n")
    kitchen.set(width=2, height=2)
    kitchen.text(f"{cliente.upper()}")
    kitchen.text("\n\n")
    total_orden = 0.00
    total = 0.00
    for item in data: 
        kitchen.set(width=2, height=2, align='left')
        for key, value in item.items():
            if(key == 'ARTICULO'):
                articulo = cleanStrings(value.upper())
                kitchen.text(f"{articulo.strip()}\n")
            elif (key == 'PRECIO'):
                total_orden += float(value)  
            elif (key == 'EXTRAS' and value != 'SIN EXTRAS'): 
                kitchen.set(width=2, height=2, align='left', font='B', text_type='B')
                value = 'EXTRAS: [' + value + ']'
                kitchen.text(f"{value}\n")   
        kitchen.text("\n")
    
    kitchen.set(width=2, height=2, align='left')

    if(float(abono) > 0.00):
        total = total_orden - float(abono)
        kitchen.text(f"\nMonto: {total_orden}$ \b Abono: {abono}$\n")
        kitchen.text(f"\nTotal a Pagar: {total}$\n")
    else:
        kitchen.text(f"\nTotal: {total_orden}$\n")
    kitchen.text(f"\nHora: {fechaHora}\n")
    kitchen.text(f"\nFecha: {fecha}\n")
    kitchen.cut()
    # Corta el papel (opcional, depende de tu impresora)
    kitchen.close()

    