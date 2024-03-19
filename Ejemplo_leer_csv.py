
def obtener_csv_como_lista_de_diccionarios(nombre_archivo):
    
    separador = ";"
    #with open(nombre_archivo, encoding="utf-8") as archivo:
    with open(nombre_archivo) as archivo:
        next(archivo)  # Omitir encabezado del archivo
        clientes = []
        for linea in archivo:
            linea = linea.rstrip("\n")  # Quitar salto de línea
            columnas = linea.split(separador)
            idcliente = columnas[0]
            nombre = columnas[1]
            razonsocial = columnas[2]
            cif = columnas[3]
            clientes.append({
                "idcliente": idcliente,
                "nombre": nombre,
                "razonsocial": razonsocial,
                "cif": cif,
            })
        return clientes


def main():
    clientes = obtener_csv_como_lista_de_diccionarios("data\clientes.csv")
    for cliente in clientes:
        idcliente = cliente["idcliente"]
        nombre = cliente["nombre"]
        razonsocial = cliente["razonsocial"]
        Cif = cliente["cif"]
        print(
            f"Tenemos a {idcliente} con el nombre  {nombre} y la razon social {razonsocial}")


main()

