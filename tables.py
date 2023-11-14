from django.db import connection

# Obtener una lista de todas las tablas en la base de datos
with connection.cursor() as cursor:
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE'")
    tables = cursor.fetchall()
    print(tables)
