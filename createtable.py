from django.db import connection

create_table_query = '''
CREATE TABLE facturacion_notadebito (
    id SERIAL PRIMARY KEY,
    n_notadebito INTEGER NOT NULL,
    factura_id INTEGER REFERENCES facturacion_factura(id) ON DELETE CASCADE,
    pago_id INTEGER REFERENCES facturacion_pago(id) ON DELETE CASCADE,
    monto NUMERIC(14, 2) DEFAULT 0.00
)
'''
with connection.cursor() as cursor:
    cursor.execute(create_table_query)
