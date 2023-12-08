# Herramientas para gestión de datos

En esta carpeta se encuentra el Docker Compose para levantar Hadoop con Hue.

# Requisitos

- [Docker](https://www.docker.com/get-started/)

# Pasos

Ejecutar en la linea de comandos:

```shell
docker compose up
```

Esto levantara los servicios de Hadoop, Postgres & Hue.

Para acceder a Hadoop: [localhost:9870](http://localhost:9870)
Para acceder a Hue: [localhost:8888](http://localhost:8888)

# Configuraciones

Para modificar la configuracion de hue, el archivo es `hue.ini`.
Para modificar la configuracion de hadoop, el archivo es `config`.