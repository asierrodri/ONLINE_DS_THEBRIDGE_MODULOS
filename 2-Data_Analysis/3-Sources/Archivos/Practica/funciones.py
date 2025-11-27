from variables import *

def is_doc_type(archivo):
    for type in doc_types:
        if archivo.endswith(type):
            return True
    return False
        
def is_img_type(archivo):
    for type in img_types:
        if archivo.endswith(type):
            return True
    return False
        
def is_soft_type(archivo):
    for type in software_types:
        if archivo.endswith(type):
            return True
    return False