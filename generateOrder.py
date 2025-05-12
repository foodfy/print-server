from escpos.printer import Network
from datetime import datetime
from utils.cleanStrings import cleanStrings 

def output(data, mesa, mesero):
    # Inicializa una instancia de la clase Network con la dirección IP de la impresora
 
    orderDetailsOrdered = sorted(data, key=lambda order: (order['IP'] == "null", order['IP']))
    
    timer     = datetime.now()
    hora      = timer.time()
    fechaHora = hora.strftime('%H:%M')
    fecha     = timer.strftime('%d-%m-%Y')
    
    kitchen   = Network(orderDetailsOrdered[0]['IP'])
    kitchen.open()
    kitchen.set(width=3, height=3, align='left', font='B', text_type='B')
    kitchen.text(f"{mesero.upper()}, {mesa.upper()}")
    kitchen.text("\n\n")
    index     = 0
    for item in orderDetailsOrdered: 
        # Cierra la conexión con la impresora
        if((item['IP'] != orderDetailsOrdered[index - 1]['IP']) and orderDetailsOrdered[0]['IP'] != item['IP']):
            kitchen.set(width=2, height=2, align='left')
            kitchen.text(f"\nHora: {fechaHora}\n")
            kitchen.text(f"\nFecha: {fecha}\n")
            kitchen.cut()
            kitchen = Network(item['IP'])
            kitchen.open()
            kitchen.set(width=3, height=3, align='left', font='B', text_type='B')
            kitchen.text(f"{mesero.upper()}, {mesa.upper()}")
            kitchen.text("\n\n")
            kitchen.set(width=2, height=2, align='left')
        
            for key, value in item.items():
                if(key == 'ARTICULO'):
                    articulo = cleanStrings(value.upper())
                    kitchen.text(f"{articulo.strip()}\n")
                elif (key == 'EXTRAS' and value != 'SIN EXTRAS'): 
                    kitchen.set(width=2, height=2, align='left', font='B', text_type='B')
                    value = 'EXTRAS: [' + value + ']'
                    kitchen.text(f"{value}\n")
                elif (key == 'INGREDIENTES' and value != 'CON TODO'):
                    kitchen.set(width=2, height=2, align='left',  font='B', text_type='B')
                    value = 'SIN: [' + item['INGREDIENTES'] + ']'
                    kitchen.text(f"{value}\n")  
                elif (key == 'LLEVAR' and value == 'SI'):
                    value = 'PARA LLEVAR'
                    kitchen.text(f"{value}\n")
            kitchen.text("\n\n")
        else:
            kitchen.set(width=2, height=2, align='left')
            for key, value in item.items():
                if(key == 'ARTICULO'):
                    articulo = cleanStrings(value.upper())
                    kitchen.text(f"{articulo.strip()}\n")
                elif (key == 'EXTRAS' and value != 'SIN EXTRAS'): 
                    kitchen.set(width=2, height=2, align='left', font='B', text_type='B')
                    value = 'EXTRAS: [' + value + ']'
                    kitchen.text(f"{value}\n")
                elif (key == 'INGREDIENTES' and value != 'CON TODO'):
                    kitchen.set(width=2, height=2, align='left',  font='B', text_type='B')
                    value = 'SIN: [' + item['INGREDIENTES'] + ']'
                    kitchen.text(f"{value}\n")  
                elif (key == 'LLEVAR' and value == 'SI'):
                    value = 'PARA LLEVAR'
                    kitchen.text(f"{value}\n")    
            kitchen.text("\n\n")
        index += 1
    kitchen.set(width=2, height=2, align='left')
    kitchen.text(f"\nHora: {fechaHora}\n")
    kitchen.text(f"\nFecha: {fecha}\n")
    kitchen.cut()
    # Corta el papel (opcional, depende de tu impresora)
    kitchen.close()

    