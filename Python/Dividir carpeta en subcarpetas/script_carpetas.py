import os
from pathlib import Path
from os import walk

#Directorio donde están las fotos
dir = r"C:\Ruta\donde\estan\nuestras\fotos"

#Inicializo la variable que irá controlando el nº de carpeta a crear
contador_carpetas = 1

#Creamos la lista con los ficheros del directorio actual
res = []
for (dir, dir_names, file_names) in walk(dir):
    res.extend(file_names)
    #print(*res,sep='\n') #Esto es para pintar los ficheros en pantalla con un salto de línea, pura depuración

#Recogemos el nº de elementos de la lista para saber cuanto durará el for
num_ficheros = len(res)

#Directorio donde se crearán la nuevas carpetas
ruta = Path(r"C:\Ruta\nueva")

#Creamos un for que recorra los ficheros, cree las carpetas y mueva las fotos al nuevo destino
for i in range(num_ficheros):
    if (num_ficheros-i) < 99:
        print(num_ficheros-i)
        exit()

    #Creo una carpeta cuando el contador i sea múltiplo de 100, ya que quiero que en cada carpeta haya 100 fotos
    if i%100 == 0:
        nombreOK=str(contador_carpetas)
        ruta_destino=os.path.join(ruta, nombreOK)
        os.mkdir(ruta_destino)
        contador_carpetas += 1

    #Indico la ruta completa, con nombre incluído, de donde están las fotos y donde las quiero mover
    fichero_origen = os.path.join(dir,res[i])
    fichero_destino = os.path.join(ruta_destino,res[i])
    os.rename(fichero_origen,fichero_destino)