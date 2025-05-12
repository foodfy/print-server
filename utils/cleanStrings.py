def cleanStrings(string):
    indice = string.find(")")
    if indice != -1:
        # Encuentra la posición del paréntesis ")"
        # Elimina todo lo que está antes del paréntesis
        nueva_cadena = string[indice + 1:]
        return nueva_cadena
    else:
        # Si no se encuentra el paréntesis, devuelve la cadena original
        return string