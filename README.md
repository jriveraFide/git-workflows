Este es un codigo reusable en los action workflow ubicados en los repositorios donde tus estudiantes vana subir su codigo.
La estructura de folders dentro de tu repositorio debe de ser la siguiente:
- miRepositorio
  - .github/workflows/miworkflow.yml
  - examen1
     - nombre_del_estudiante.zip
     - criterios.json
  - tarea1
     - nombre_del_estudiante.zip
     - criterios.json
       
Crear los siguientes secretos en tu repositorio:

OPENAI_API_KEY

PAT_REPORTES --> este es tu github token

REPO_EVALUADOR --> este es la direccion en github donde se encuentra este repositorio, formato: org/repo, ex: jriveraFide/git-workflows (PUBLICO)

REPO_REPORTES --> este es la direccion en github donde se encuentra el repositorio donde quieres que la automatizacion cargue tus reportes formato: org/repo (PRIVADO)

Estructura para el archivo criterios.json:

{
  "criterios": [
    {
      "nombre": "Estructuras de datos",
      "descripcion": "Uso adecuado de listas, pilas, colas, etc.",
      "puntaje_maximo": 30
    },
    {
      "nombre": "Lógica del algoritmo",
      "descripcion": "El algoritmo resuelve correctamente el problema planteado.",
      "puntaje_maximo": 40
    },
    {
      "nombre": "Legibilidad",
      "descripcion": "El código está bien indentado, usa nombres claros y es fácil de entender.",
      "puntaje_maximo": 15
    },
    {
      "nombre": "Documentación y comentarios",
      "descripcion": "El código contiene comentarios útiles que explican partes clave.",
      "puntaje_maximo": 15
    }
  ]
}
