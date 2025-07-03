# Clonación y ejecución de un proyecto Django REST Framework con Swagger

## 1. Clonar el repositorio
Abre tu terminal y ejecuta:
git clone https://github.com/MonicaBebesita/DjangoAPI.git


## 2. Crear y activar entorno virtual
python -m venv env
source env/bin/activate        # En Linux/Mac
env\Scripts\activate           # En Windows

## 3. Instalar dependencias
pip install -r requirements.txt

## 4. Aplicar migraciones
python manage.py migrate

## 5. Crear superusuario
python manage.py createsuperuser

## 6.  Ejecutar el servidor
python manage.py runserver

## 7. Acceder a la documentación Swagger
Abre tu navegador en:
http://127.0.0.1:8000/swagger/      verificar la documentación en:
http://127.0.0.1:8000/redoc/      
