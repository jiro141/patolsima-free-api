migrate:
	python manage.py migrate

migrateapp:
	python manage.py migrate $(APP)

makemigrations:
	python manage.py makemigrations
	echo $(APP)

appmigrations:
	python manage.py makemigrations $(APP)
	echo $(APP)

addtestdata:
	python manage.py create_default_data_core

createauxdirectories:
	mkdir var
	mkdir var/pdfkit
	mkdir var/s3

test:
	python manage.py test