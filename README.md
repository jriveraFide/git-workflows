Este es un codigo reusable en los action workflow ubicados en los repositorios donde tus estudiantes vana subir su codigo.
La estructura de folders dentro de tu repositorio debe de ser la siguiente:
- miRepositorio
  - .github/workflows/miworkflow.yml
  - examen1
     - nombre_del_estudiante.py
     - criterios.json
  - tarea1
     - nombre_del_estudiante.py
     - criterios.json
       
Debes de crear los siguientes secretos en tu repositorio:
OPENAI_API_KEY
PAT_REPORTES --> este es tu github token
REPO_EVALUADOR --> este es la direccion en github donde se encuentra este repositorio, formato: org/repo, ex: jriveraFide/git-workflows (PUBLICO)
REPO_REPORTES --> este es la direccion en github donde se encuentra el repositorio donde quieres que la automatizacion cargue tus reportes (PRIVADO)
