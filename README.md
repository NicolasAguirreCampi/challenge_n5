# challenge_n5
## Notas imoprtantes
Al inicio del programa se corre un seed que elimina la base de datos, entonces cada vez que se reinicia el servidor se resetea la base de datos (para que sea mas facil volver a empezar).

## Docker image
```bash
docker pull nicolasaguirre/n5challenge-app:latest
```

## Cómo Usar la API
Hay una coleccion de postman en este proyecto llamado n5challenge collection.postman_collection en el cual hay un login, alta de infraccion y generar informe.

En el seed que se corre al inicio del programa se crean 2 oficales para usar la api:
* usuario: Ryan, password: ryan_password
* usuario: Sara, password: sara_password

Ademas tambien hay 2 personas de prueba y un auto por persona.

Para dar de alta una infraccion primero hay que logearse, copiarel token y pegarlo como "Bearer {token}" en el authorization de la request.