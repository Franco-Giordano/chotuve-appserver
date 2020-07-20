# Chotuve - Application Server
![Grupo](https://img.shields.io/badge/grupo-11-blue)
[![Build Status](https://travis-ci.com/Franco-Giordano/chotuve-appserver.svg?token=7zpnJJggDS7tTpxSzkvp&branch=master)](https://travis-ci.com/Franco-Giordano/chotuve-appserver)
[![Coverage Status](https://coveralls.io/repos/github/Franco-Giordano/chotuve-appserver/badge.svg?branch=master&t=hXdO0j)](https://coveralls.io/github/Franco-Giordano/chotuve-appserver?branch=master)
![api](https://img.shields.io/badge/api-v1.0.0-blueviolet)
[![sv](https://img.shields.io/badge/view-media%20sv-important)](https://github.com/sebalogue/chotuve-mediaserver)
[![sv](https://img.shields.io/badge/view-auth%20sv-important)](https://github.com/santiagomariani/chotube-auth-server)
[![sv](https://img.shields.io/badge/view-android-important)](https://github.com/javier2409/Chotuve-Android)


## Instrucciones

1. Instalar [Docker Engine](https://docs.docker.com/engine/install/) y [Docker Compose](https://docs.docker.com/compose/install/)

2. Levantar server + database: `docker-compose up`

4. Probar la REST API en `0.0.0.0:5000`



---------------------------------------------


## API v1.0.0
_May be outdated, check staging branch for latest updates_

Para ejecutar las requests, se recomienda utilizar [Postman](https://www.postman.com/downloads/)

**Salvo por /ping, /reset-codes y PUT /auth, TODOS los endpoints REQUIEREN el campo "x-access-token" en los headers, con un token valido**

#### Videos

- Obtener todos los videos guardados en la database:
`GET 0.0.0.0:5000/videos`

- Obtener datos de un solo video (sin comentarios):
`GET 0.0.0.0:5000/videos/<id>`

- Obtener todos los comentarios de un video:
`GET 0.0.0.0:5000/videos/<id>/comments`

- Postear un video:
`POST 0.0.0.0:5000/videos` con body (todos opcionales salvo firebase_url y thumbnail_url):
```json
{
	
	"title":"titulo video",
	"description": "descripcion de ejemplo",
	"location":"lugar posteado",
	"firebase_url":"...firebase.com...",
	"is_private":false,
	"thumbnail_url":"www.url.com..."
}
```

- Editar un video:
`PATCH 0.0.0.0:5000/videos/<id>` con body (todos opcionales):
```json
{
	
	"title":"titulo video",
	"description": "descripcion de ejemplo",
	"location":"lugar posteado",
	"is_private":false,
}
```

- Borrar un video (y todas las racciones+comentarios):
`DELETE 0.0.0.0:5000/videos/<id>`

- Postear un comentario:
`POST 0.0.0.0:5000/videos/<id>/comments` con body (text obligatorio, vid_time opcional):
```json
{
	"text":"comentario de ejemplo",
	"vid_time":"5:43"
}
```

- Obtener todas las reacciones a un video (username + like/dislike):
`GET 0.0.0.0:5000/videos/<id>/reactions` (en la respuesta: likes_video es true si es like, false si es dislike)


- Reaccionar a un video:
`POST 0.0.0.0:5000/videos/<id>/reactions` con body (true es like, false es dislike; campo obligatorio):
```json
{
	"likes_video":true
}
```

- Editar reaccion a un video
`PATCH 0.0.0.0:5000/videos/<id>/reactions` con body (true es like, false es dislike; campo obligatorio):
```json
{
	"likes_video":true
}
```

#### Usuarios

- Obtener mi ID de usuario al loguearme:
```GET 0.0.0.0:5000/auth```, devuelve {"id":int}

- Obtener datos publicos de un usuario
```GET 0.0.0.0:5000/users/<uuid>```

- Buscar usuarios con datos coincidentes:
```GET 0.0.0.0:5000/users?name=<name>&email=<email>&phone=<phone>&per_page=<int>&page=<int>```
Notas:
	- Cualquier argumento es opcional
	- TODOS buscan coincidencias parciales (si busco 'Fran' encuentro 'Franco').
	- Si quiero incluir un '+' en la busqueda (para phone, por ej), se debe escribirlo como '%2B' (si quiero buscar '+54 9 ...' debo buscar '%2B54 9 ...'). Probablemente ocurra lo mismo para otros caracteres especiales, [ver tabla de encodings aqui](https://www.w3schools.com/tags/ref_urlencode.asp). Esto NO ocurre con el @.
	- per_page: cuantos resultados en la rta, page: numero de pagina a ver 


- Obtener videos subidos por un usuario
```GET 0.0.0.0:5000/users/<uuid>/videos```

- Registrar un nuevo usuario:
```POST 0.0.0.0:5000/users```
con body (display_name e email obligatorios, resto opcional):
```json
{
	"display_name":"Cosme Fulanito",
	"email":"cosme_rivercampeon@gmail.com",
	"image_location":"https://image.freepik.com/foto-gratis/playa-tropical_74190-188.jpg",
	"phone_number":"+542323232323"
}
```

- Modificar datos de un usuario:
`PUT 0.0.0.0:5000/users/<id>` con body (todos opcionales):
```json
{
	"email": "juanperez@gmail.com",
	"display_name":"Matias Perez",
	"phone_number": "+5492264511422",
	"image_location":"https://image.freepik.com/foto-gratis/playa-tropical_74190-188.jpg"
}
```

- Crear reset code para generar una nueva contraseña (no necesita firebase token):
`POST 0.0.0.0:4000/reset-codes` con body:
```json
{
	
    "email": "juanperez@gmail.com"
    
}


```

- Cambiar contraseña usando el reset code (no necesita firebase token):
`PUT 0.0.0.0:4000/auth` con body:
```json
{
	
	"email": "juanperez@gmail.com",
	"reset_code":"KnPlDQ",
	"password": "Unacontraseña123"
	
}
```

#### Amistades

- Ver amigos de un usuario:
```GET 0.0.0.0:5000/users/<uuid>/friends```

- Enviar solicitud de amistad al user 9999:
```POST 0.0.0.0:5000/friend-requests``` con body (obligatorio):
```json
{
	"to": 9999
}
```

- Ver mis solicitudes pendientes:
```GET 0.0.0.0:5000/friend-requests```


- Aceptar/Rechazar solicitud pendiente:
```POST 0.0.0.0:5000/friend-requests/<otheruuid>``` con body (campo obligatorio)
```json
{
	"accept":true
}
```
(accept true para aceptar, accept false para rechazar)

#### Ping

- Chequear estado del appserver:
``` GET 0.0.0.0:5000/ping```

(devuelve {"appserver":"UP"} con codigo 200)

#### Mensajes y Chats

- Ver mensajes entre otro usuario y yo:
```GET 0.0.0.0:5000/messages/<other_user_id>?page=1&per_page=20```

page y per_page similares al endpoint GET /users

-> devuelve, por ejemplo (si mi id: 40, otro id:28):
```json
[
    {
        "id": 3,
        "sender_id": 40,
        "recver_id": 28,
        "text": "Hola bro",
        "timestamp": "2020-06-30 21:31:56.770661"
    },
    {
        "id": 4,
        "sender_id": 28,
        "recver_id": 40,
        "text": "commo anda la fiuba",
        "timestamp": "2020-06-30 21:33:00.032960"
    }
]
```

- Enviar mensaje
```POST 0.0.0.0:5000/messages/<other_user_id>``` con body:
```json
{
	"text":"Buenas tardes"
}
```

#### Registrar Push Token
- Subir mi push tkn
```POST 0.0.0.0:5000/tokens``` con body:
```json
{
	"push_token": "ExponentPushToken[XXX]"
}
```

- Ver mi push tkn (por las dudas)
```GET 0.0.0.0:5000/tokens```
-> devuelve:
```json
{
	"push_token":...
}
```

#### Estadisticas de uso

_[NO IMPLEMENTADO]_

#### Recuperacion de Passwords

_[NO IMPLEMENTADO]_

#### Modificar o borrar videos/comentarios/reacciones/amistades

_[NO IMPLEMENTADO]_

#### Ver videos sugeridos por motor de reglas

_[NO IMPLEMENTADO]_
