##IMPORTS
import os
from pathlib import Path
from os import walk
import mutagen
from mutagen.easyid3 import EasyID3
from os import listdir
from youtubesearchpython import VideosSearch
from dateutil.parser import parse, ParserError

#Directorio de la agrupación a gestionar
rootdir = r"C:\Carnaval\Nombre_de_la_agrupación_que_toque"

for rootdir, dirs, files in os.walk(rootdir):
	for subdir in dirs:
		###########################################>>>DEPURACIÓN
		'''
		print("La agrupación es: " + subdir)
		print("La ruta es: " + os.path.join(rootdir, subdir))
		ruta = os.path.join(rootdir,subdir)
		print(ruta)

		contenido = os.listdir(ruta)
		print(contenido)
		print(contenido[0])

		print("\n\n###################")
		print("Estoy trabajando sobre la agrupación: " + subdir.upper())
		'''
		###########################################<<<DEPURACIÓN

		ruta = os.path.join(rootdir,subdir)
		pistas = os.listdir(ruta)
		numero_pistas = len(pistas)
		print("En esta agrupación hay " + str(numero_pistas) + " pistas")
		#print(*pistas,sep='\n')#Lista las pistas con salto de línea ###########################################>>>DEPURACIÓN
		
		#VARIABLES GLOBALES POR AGRUPACIÓN
		genero = "Chirigota"
		autor = "J. A. Vera Luque"
		agrupacion = subdir #Vale para intérprete y álbum
		search_cadena = genero + " " + agrupacion
		#print (search_cadena)

		#Obtener el año de la agrupación buscándolo en youtube
		videosSearch = VideosSearch(search_cadena, limit = 10)
		result = videosSearch.result()
		result1 = result["result"]
		anio_agrupacion = None
		i = 0
		while not anio_agrupacion:
			resultdict = result1[i]
			year = resultdict['title']
			try:
				anio_agrupacion = str(parse(str(year), fuzzy=True).year)
			except ParserError:
				i += 1
				if i == 10:
					anio_agrupacion = 2500

		for i in range(numero_pistas):
			pista = pistas[i]
			print(pista)
			ruta_pista = os.path.join(ruta,pista)
			print(ruta_pista)

			#Manejo de cadenas de texto para formar el título de la pista y el tracknumber
			inicio_pista = pista.index('-')
			fin_pista = pista.index('.mp3')
			nombre_pista = pista[inicio_pista+2:fin_pista]

			fin_track = pista.index('-')
			track_OK = pista[:fin_track]

			#Manejo de posible error si los .mp3 a editar no tienen etiquetas id3 iniciadas
			try:
				tags = EasyID3(ruta_pista)
			except mutagen.id3.ID3NoHeaderError:
				tags = mutagen.File(ruta_pista, easy=True)

			###########################################>>>DEPURACIÓN
			#print("Para titulo canción: " + pista_OK)
			#print("Nº de pista: " + track_OK)
			#print("Etiquetas previas: " + tags.pprint())
			###########################################<<<DEPURACIÓN

			#CAMPOS A RELLENAR: album, artist, composer, date, genre, title, tracknumber
			tags['title'] = nombre_pista
			tags['artist'] = agrupacion
			tags['album'] = agrupacion
			tags['tracknumber'] = track_OK
			tags['genre'] = genero
			tags['composer'] = autor
			tags['albumartist'] = ''
			tags['date'] = anio_agrupacion
			
			tags.save()