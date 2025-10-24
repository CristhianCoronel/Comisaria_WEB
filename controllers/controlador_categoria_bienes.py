# controllers/controlador_categoria_bienes.py
from models.Bienes import Categoria_Bienes
from bd import bd

def obtener_categorias():
    """Devuelve todas las categorías de bienes registradas."""
    return Categoria_Bienes.query.all()

def obtener_categoria_por_id(id_categoria):
    """Devuelve una categoría específica por su ID."""
    return Categoria_Bienes.query.get(id_categoria)

def insertar_categoria(nombre, descripcion):
    """Inserta una nueva categoría de bienes en la base de datos."""
    nueva = Categoria_Bienes(
        nombre=nombre,
        descripcion=descripcion
    )
    bd.session.add(nueva)
    bd.session.commit()

def modificar_categoria(id_categoria, nombre, descripcion):
    """Actualiza una categoría de bienes existente."""
    categoria = Categoria_Bienes.query.get(id_categoria)
    if categoria:
        categoria.nombre = nombre
        categoria.descripcion = descripcion
        bd.session.commit()
        return True
    return False

def eliminar_categoria(id_categoria):
    """Elimina una categoría de bienes de la base de datos."""
    categoria = Categoria_Bienes.query.get(id_categoria)
    if categoria:
        bd.session.delete(categoria)
        bd.session.commit()
        return True
    return False
