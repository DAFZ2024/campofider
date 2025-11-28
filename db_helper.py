"""
Helper module para convertir las consultas restantes de MySQL a SQLite3
Este archivo contiene funciones auxiliares para las rutas que aún no se han convertido
"""

def convert_mysql_to_sqlite_query(query):
    """
    Convierte una consulta MySQL a SQLite3
    - Reemplaza %s con ?
    - Reemplaza CURDATE() con date('now')
    - Reemplaza LAST_INSERT_ID() con last_insert_rowid()
    """
    query = query.replace('%s', '?')
    query = query.replace('CURDATE()', "date('now')")
    query = query.replace('LAST_INSERT_ID()', 'last_insert_rowid()')
    return query
