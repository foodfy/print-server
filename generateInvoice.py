from escpos.printer import Network
from datetime import datetime
from utils.cleanStrings import cleanStrings 

def printInvoice(data):
    # Inicializa una instancia de la clase Network con la dirección IP de la impresora
    timer     = datetime.now()
    hora      = timer.time()
    fechaHora = hora.strftime('%H:%M')
    fecha     = timer.strftime('%d-%m-%Y')
    contribuyente = data["HEADER"][8]["CONTRIBUYENTE"]

    if(contribuyente == 'on'):
        contribuyente = "NO CONTRIBUYENTE"
  
    kitchen   = Network(data["HEADER"][5]["IMPRESORA"])
    kitchen.set(width=2, height=2, align='center', font='B', text_type='B')
    if(data["HEADER"][9]["TIPO_DOCUMENTO"] == 'FIS'):
        kitchen.text(f"SENIAT\n")
    else:
       kitchen.set(width=1, height=1, align='center', font='B') 
       kitchen.text("******** NO FISCAL **********\n")
    kitchen.set(width=1, height=1, align='center')
    kitchen.text(f"J-5022982207\n F&F DURAN BURGER, C.A\n")
    kitchen.text(f"AV INDUSTRIAL UNO CRUCE CON AVENIDA\n")
    kitchen.text(f"PRINCIPAL CC SAVE NIVEL PB LOCAL 24 y 25")
    kitchen.text(f"PB URB INDUSTRIAL Y COMERCIAL LA\n ISABELICA VALENCIA CARABOBO\n")
    kitchen.text(f"ZONA POSTAL 2003 \n")
    kitchen.text("\n")
    kitchen.set(width=1, height=1, align='left')
    kitchen.text(f"RIF/CI: {data['HEADER'][0]['RIF']} \n")
    kitchen.text(f"R.S: {contribuyente} \n")
    kitchen.text(f"{data['HEADER'][1]['CLIENTE']} \t Orden: {data['HEADER'][3]['ORDEN']} \t  | Mesa: {data['HEADER'][4]['MESA']} \n")
    kitchen.set(width=1, height=1, align='center')
    kitchen.text("FACTURA\n")
    kitchen.set(width=1, height=1, align='left')
    kitchen.text(f"FACTURA:{' ' * 30}{data['HEADER'][2]['FACTURA']}\n")
    kitchen.text(f"FECHA:{fecha}{' ' * 20}HORA:{fechaHora}\n")
    kitchen.text(f"{'_ ' * 24}")

    moneda = ''
    total_facturado = 0.00
    tasa_cambio = float(data["HEADER"][7]["TASA"])
    IVA = int(data["HEADER"][6]["IVA"])

    if(data["HEADER"][10]["MONEDA"] == 'USD'):
        moneda = "$ "
    else:
        moneda = "Bs"
    
    kitchen.set(width=1, height=1, align='left')
    for item in data["BODY"]: 
        for key, value in item.items():
            if(key == 'nombre'):
                articulo = cleanStrings(value.upper())
                kitchen.text(f"{articulo.strip()}")
            if (key == 'precio_unitario'):
                precio = float(value)
                if(data["HEADER"][10]["MONEDA"] == 'USD'):
                    precio = precio * tasa_cambio
                kitchen.text(f"{' ' * (40 - len(articulo) - len(moneda))} {moneda}{precio}") 
            if(key == 'precio'): 
                total_facturado += float(value)
    total_iva           = total_facturado * IVA / 100
    sub_total           = total_facturado
    total_facturado_iva = total_facturado + total_iva

    # if(data["HEADER"][10]["MONEDA"] == 'VEF'):
    #     total_iva = total_iva * tasa_cambio
    #     sub_total = sub_total * tasa_cambio
    #     total_facturado_iva = format(total_facturado_iva * tasa_cambio, '.2f')

    kitchen.text(f"{'_ ' * 24}")
    kitchen.set(width=1, height=1, align='left') 
    
    if(data["HEADER"][9]["TIPO_DOCUMENTO"] == 'FIS'):
        kitchen.text(f"IVA {IVA}%{' ' * (37 - len(str(total_iva)) - len(moneda))} {moneda}{total_iva}\n")
        kitchen.text(f"SUBTTL: {' ' * (36 - len(str(sub_total)) - len(moneda))} {moneda}{sub_total}\n")
    
    kitchen.text(f"TOTAL {' ' * (38 - len(str(total_facturado_iva)) - len(moneda))} {moneda}{total_facturado_iva}\n")
    
    if(data["HEADER"][9]["TIPO_DOCUMENTO"] != 'FIS'):
        kitchen.set(width=1, height=1, align='center', font='B') 
        kitchen.text("******** NO FISCAL **********")
    kitchen.cut()
    # Corta el papel (opcional, depende de tu impresora)
    kitchen.close()

    