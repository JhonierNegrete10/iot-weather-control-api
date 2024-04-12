# Prueba Técnica: Construcción de una API con Docker

Construir una aplicación en Python que funcione como una API, conectándose a un servicio externo y almacenando los resultados en una base de datos MySQL. Toda la aplicación debe estar contenida en Docker Compose.

## Requisitos

Crear una aplicación en Python que exponga una API RESTful con los siguientes endpoints:

* GET /api/data: Obtener datos de un servicio externo (puedes utilizar una API pública de tu elección).

* POST /api/data: Almacenar los datos obtenidos del servicio externo en una base de datos MySQL.

* GET /api/data/{id}: Obtener un registro de datos específico de la base de datos MySQL por su ID.

* Un websocket que permita ver los datos de manera similar al primer endpoint.

* Utilizar FastAPI para construir la API.

* Configurar un contenedor de base de datos MySQL utilizando Docker Compose para almacenar los datos. La base de datos debe tener una tabla para almacenar los datos recuperados.

* Manejo de Errores: Implementar un manejo de errores adecuado y respuestas de error para diferentes escenarios.

* Utilizar Docker Compose para gestionar los contenedores de la aplicación y la base de datos.

Criterios de Evaluación:

Funcionalidad: La API debe funcionar correctamente con endpoints para obtener datos de un servicio externo, almacenarlos en la base de datos MySQL y recuperar datos de la base de datos.
Calidad del Código: Se evaluará la claridad y organización del código, el cumplimiento de las mejores prácticas y los comentarios/documentación.

Contenerización: Asegurarse de que Docker Compose se utilice para gestionar eficazmente los contenedores de la API y la base de datos.

Almacenamiento de Datos: Los datos obtenidos del servicio externo deben almacenarse con precisión en la base de datos MySQL
