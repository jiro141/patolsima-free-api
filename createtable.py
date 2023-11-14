from django.db import connection

create_table_query = '''
CREATE TABLE nombre_tabla (
    n_notadebito SERIAL PRIMARY KEY,
    n_factura INTEGER DEFAULT 0,
    factura_id INTEGER REFERENCES facturacion_factura(id) ON DELETE CASCADE,
    pago_id INTEGER REFERENCES facturacion_pago(id) ON DELETE CASCADE,
    monto NUMERIC(14, 2) DEFAULT 0.00
)
'''
with connection.cursor() as cursor:
    cursor.execute(create_table_query)
