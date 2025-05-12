from escpos.printer import Network
from datetime import datetime
from utils.cleanStrings import cleanStrings 

def output(ip, data, mesa, mesero):
    # Inicializa una instancia de la clase Network con la dirección IP de la impresora
    kitchen = Network(ip)

    timer = datetime.now()
    hora  = timer.time()
    fechaHora = hora.strftime('%H:%M')
    fecha = timer.strftime('%d-%m-%Y')

    # Conecta con la impresora
    kitchen.open()
    count = 0
    # Imprime cada elemento de los datos JSON utilizando el método kitchen
    kitchen.set(width=2, height=2, align='left')
    kitchen.text(f"{mesero}, {mesa}")
    kitchen.text("\n\n")
    for item in data:
        for key, value in item.items():
            kitchen.set(width=2, height=2, align='left')
            if(key == 'ARTICULO'):
                count += 1
                articulo = cleanStrings(value)
                kitchen.text(f"{articulo.strip()}\n")
            else: 
                
                if(key == 'CON EXTRAS' and value == 'SIN EXTRAS'):
                    continue
                
                if(key == 'SIN INGREDIENTES' and value == 'CON TODO'):
                    continue

                if(key == 'CON EXTRAS' and value != 'SIN EXTRAS'): 
                  kitchen.set(width=2, height=2, align='left',  font='B', text_type='B')
                  value = 'EXTRAS: [' + value.strip() + ']'
                
                if(key == 'SIN INGREDIENTES' and value != 'CON TODO'):
                  kitchen.set(width=2, height=2, align='left',  font='B', text_type='B')
                  value = 'SIN: [' + value.strip() + ']'  
            
                if (key == 'LLEVAR' and value == 'NO'):
                    continue

                if(key == 'LLEVAR' and value == 'SI'):
                    value = 'PARA LLEVAR'
                
                kitchen.text(f"{value}\n")
        kitchen.text("\n")
    # Corta el papel (opcional, depende de tu impresora)
    kitchen.text(f"\nHora: {fechaHora}\n")
    kitchen.text(f"\nFecha: {fecha}\n")
    kitchen.cut()
    # Cierra la conexión con la impresora
    kitchen.close()
    