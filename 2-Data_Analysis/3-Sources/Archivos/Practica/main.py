from funciones import *
import os
import shutil

ruta_descargas = "C:\\Users\\Asier\\Downloads"
os.chdir(ruta_descargas)

os.mkdir('Imagenes')
os.mkdir('Documentos')
os.mkdir('Software')
os.mkdir('Otros')

archivos = []
for i in os.listdir():
    if '.' in i:
        archivos.append(i)

for archivo in archivos:
    if is_doc_type(archivo) == True:
        shutil.move(archivo, "Documentos/")
    elif is_img_type(archivo) == True:
        shutil.move(archivo, "Imagenes/")
    elif is_soft_type(archivo) == True:
        shutil.move(archivo, "Software/")
    else:
        shutil.move(archivo, "Otros/")