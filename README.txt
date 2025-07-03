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
python manage.py makemigrations
python manage.py migrate

## 5. Crear superusuario
python manage.py createsuperuser

## (opcional) Correr las pruebas:
python manage.py test

## 6.  Ejecutar el servidor
python manage.py runserver

## 7. Acceder a la documentación Swagger
Abre tu navegador en:
http://127.0.0.1:8000/api/schema/swagger-ui/

## 8. Para usar todos los endpoints primero debes autenticarte, ve a 
/api/token/ y genera un token en la interfaz, luego pega el token en
 el boton de "Authorize" que esta arriba.
 {
    "refresh": "eyJhbGciOiJI...",
    "access": "eyJhbGciOiJ..."  <-- ¡Copia este!
}
## 9. si pegaste el token correctamente, podras realizar las pruebas sin ningun
inconveniente