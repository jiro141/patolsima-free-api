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