# Banpay

# Requisitos
- Tener instalado Docker en tu computadora.
- Tener instalado Git en tu computadora.

# Instalación
**Clona este repositorio**

    git clone https://github.com/Luis452x/Banpay_v01.git

## Configuración del docker

  - En una terminal, abre la carpeta donde hayas copiado el proyecto
  - Una vez en la carpeta escribe el siguiente comando
  ``` 
    docker build -t nombre_de_imagen .
  ```
  - Una vez creada la imagen la ejecutamos con el siguiente comando

  ``` 
    docker run -d --name nombre_de_tu_docker -p 8000:8000 nombre_de_imagen
  ```
  - Y ya debería estar funcionando :)

## Endpoints

- **Bienvenido a la API**: `Get /`
- **Crear usuario**: `POST /Login/CreateUser`
- **Obtener todos los usuarios**: `GET /User/`
- **Obtener usuario a través del nombre de usuario**: `GET /User/{user_name}`
- **Obtener los datos de la API de Ghibli filtrados por el rol del usuario**: `GET /User/Ghibli/`
- **Actualizar usuario**: `PUT /User/{user_name}`
- **Borrar usuario**: `DELETE /User/{user_name}`

### Ejemplos realizados con /docs de FastAPI

- **Bienvenido a la API**

Para asegurarse que la API esta corriendo, al ingresar al enlace se regresa un mensaje de bienvenida

```   curl -X 'GET' \
 'http://127.0.0.1:8000/' \
  -H 'accept: application/json'
```

- Respuesta
![Imagen de respuesta](images/bienvenida_api.jpg)

- **Crear usuario**

Con el propósito de facilitar las pruebas, se puede crear un usuario admin simplemente enviando 'true' como parametro de 'is_admin' al momento de crear un usuario


- Ejemplo 
  ![Imagen de ejemplo a través de /docs de FastAPI](images/create_user_docs_try_out.jpg)

```curl -X 'POST' \
'http://127.0.0.1:8000/Login/CreateUser?is_admin_f=true' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
"user_name": "Luis",
"user_password": "12345678",
"user_rol": "films"}'
```
- Respuesta de creación de usuario
  ![Imagen de respuesta](images/create_user_docs_try_out_response.jpg)


- **Obtener todos los usuarios**

    
```curl -X 'GET' \
'http://127.0.0.1:8000/User/' \
-H 'accept: application/json'
```
  
- Ejemplo obteniendo todos los usuarios
  ![Imagen de ejemplo a través de /docs de FastAPI](images/response_get_all_users.jpg)

- **Obtener usuario a través del nombre de usuario**

    - A partir de este ejemplo será necesario autentificarte para acceder a los demás Endpoints.
    - La API verifica que el nombre de usuario y contraseña coincidan con alguno registrado.
    - Una vez verificado, se genera un JWT, para propósito de esta prueba se uso la secret_key='SECRET_KEY', no se recomienda por razones de seguridad que la secret_key vaya implicita en el código.
    - Para los ejemplos se usó la autenticación que viene en FastAPI con ayuda de un form_data y OAuth2PasswordRequestForm.
    - En caso de que el usuario sea 'admin', podrá hacer peticiones GET, PUT y DELETE de cualquier usuario.
    
    - Ejemplo de autenticación
    ![Imagen de ejemplo a través de /docs de FastAPI](images/authorization_form_data_fastapi.jpg) 

    Una vez hecha la autenticación se puede proceder con los Endpoints

```curl -X 'GET' \
'http://127.0.0.1:8000/User/Luis' \
-H 'accept: application/json' \
-H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJMdWlzIiwiSWQiOjEsInJvbCI6ImZpbG1zIiwiaXNfYWRtaW4iOnRydWUsImV4cCI6MTcyNTUyNTY2OH0.NEaSgshHL2h2Q1yPpmCl6-Q-HkXJlPohfOmgnwxY1kg'
```

  - Ejemplo obteniendo datos de usuario a través del nombre de usuario
    ![Imagen de ejemplo a través de /docs de FastAPI](images/get_user_by_user_name.jpg)
  
  - En caso de no tener autenticación la respuesta sería la siguiente
    ![Imagen de ejemplo a través de /docs de FastAPI](images/authentication_error.jpg)

- **Obtener los datos de la API de Ghibli filtrados por el rol del usuario**

    Hace una petición a la API de Studio Ghibli obteniendo datos con base en el rol del usuario

```curl -X 'GET' \
'http://127.0.0.1:8000/User/Ghibli/' \
-H 'accept: application/json' \
-H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJMdWlzIiwiSWQiOjEsInJvbCI6ImZpbG1zIiwiaXNfYWRtaW4iOnRydWUsImV4cCI6MTcyNTUyNzE5Nn0.xzl3bi8KsAdhpBdTRg9JKCVxRM6mXigG31qxfb_CtIY'
```
  
- Ejemplo de los datos obtenidos
![Imagen de ejemplo a través de /docs de FastAPI](images/get_Ghibli_data_by_rol.jpg)

- **Actualizar usuario**

```curl -X 'PUT' \
  'http://127.0.0.1:8000/User/Luis' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJMdWlzIiwiSWQiOjEsInJvbCI6ImZpbG1zIiwiaXNfYWRtaW4iOnRydWUsImV4cCI6MTcyNTUyNzE5Nn0.xzl3bi8KsAdhpBdTRg9JKCVxRM6mXigG31qxfb_CtIY' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_name": "Luis",
  "user_password": "12345678",
  "user_rol": "locations"
}'
```
- Ejemplo
![Imagen de ejemplo a través de /docs de FastAPI](images/update_user_request.jpg)

- Respuesta de actualización de usuario
![Imagen de ejemplo a través de /docs de FastAPI](images/update_user_response.jpg)

- **Borrar usuario**

```curl -X 'DELETE' \
  'http://127.0.0.1:8000/User/Luis' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJMdWlzIiwiSWQiOjEsInJvbCI6ImZpbG1zIiwiaXNfYWRtaW4iOnRydWUsImV4cCI6MTcyNTUyNzE5Nn0.xzl3bi8KsAdhpBdTRg9JKCVxRM6mXigG31qxfb_CtIY'
  ```
  
- Ejemplo 
![Imagen de ejemplo a través de /docs de FastAPI](images/delete_user_request.jpg)

- Respuesta
![Imagen de ejemplo a través de /docs de FastAPI](images/delete_user_response.jpg)

