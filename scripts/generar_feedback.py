import argparse
import json
import os
import zipfile
import tempfile
from datetime import datetime
from openai import OpenAI

# Inicializar cliente con la API Key desde variable de entorno
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EXTENSIONES_VALIDAS = ('.java','.py')

def descomprimir_zip(ruta_zip):
    """Descomprime un archivo .zip a una carpeta temporal"""
    carpeta_temp = tempfile.mkdtemp()
    with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
        zip_ref.extractall(carpeta_temp)
    return carpeta_temp

def cargar_codigo_desde_carpeta(ruta_carpeta):
    """Lee todos los archivos con extensiones válidas en una carpeta y sus subcarpetas"""
    codigo_completo = ""
    for root, _, files in os.walk(ruta_carpeta):
        for archivo in files:
            if archivo.endswith(EXTENSIONES_VALIDAS):
                ruta_completa = os.path.join(root, archivo)
                try:
                    with open(ruta_completa, 'r', encoding='utf-8') as f:
                        codigo_completo += f"\n// Archivo: " + os.path.relpath(ruta_completa, ruta_carpeta) + "\n"
                        codigo_completo += f.read() + "\n"
                except Exception as e:
                    print(f"⚠️ No se pudo leer {ruta_completa}: {e}")
    return codigo_completo

def cargar_prompt_principal(ruta_archivo):
    """Carga el archivo de prompt principal"""
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        return f.read()

def cargar_criterios(ruta_json):
    """Carga los criterios desde el archivo JSON"""
    with open(ruta_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['criterios']

def construir_prompt(codigo, criterios, prompt_principal):
    """Construye el prompt completo con el código y los criterios"""
    prompt = prompt_principal
    prompt += "\n\n### Código del Estudiante:\n"
    prompt += f"```\n{codigo}\n```\n\n"
    prompt += "### Criterios de Evaluación:\n"
    for i, criterio in enumerate(criterios, 1):
        prompt += f"{i}. {criterio['nombre']} ({criterio['puntaje_maximo']} pts): {criterio['descripcion']}\n"
    prompt += "\nDevuelve una tabla con:\n- Criterio\n- Puntaje otorgado\n- Comentario\nY al final una nota total sobre 100.\n"
    return prompt

def evaluar_con_openai(prompt):
    """Llama a OpenAI para evaluar el código"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un evaluador académico de código Java y HTML."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def guardar_feedback(ruta_salida, contenido):
    """Guarda el feedback en un archivo de salida"""
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(f"# Reporte de Evaluación\n\n")
        f.write(f"Generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(contenido)
        f.write("\n")

def procesar_zip_estudiantes(carpeta_con_zip):
    """Procesa todos los archivos .zip en la carpeta proporcionada"""
    resultados = []
    for archivo in os.listdir(carpeta_con_zip):
        if archivo.endswith('.zip'):
            ruta_zip = os.path.join(carpeta_con_zip, archivo)
            print(f"⚙️ Procesando {ruta_zip}...")

            # Descomprimir el ZIP
            carpeta_extraida = descomprimir_zip(ruta_zip)

            # Leer los archivos de código en la carpeta descomprimida
            codigo = cargar_codigo_desde_carpeta(carpeta_extraida)

            resultados.append({
                "zip": archivo,
                "codigo": codigo,
                "ruta_extraida": carpeta_extraida
            })
    return resultados

def main():
    parser = argparse.ArgumentParser(description='Generar feedback con IA para proyectos comprimidos en ZIP.')
    parser.add_argument('--carpeta', required=True, help='Ruta a la carpeta que contiene los archivos .zip de los estudiantes')
    parser.add_argument('--criterios', required=True, help='Ruta al archivo criterios.json')
    parser.add_argument('--prompt_principal', required=True, help='Prompt a utilizar')

    args = parser.parse_args()

    # Cargar criterios y prompt
    criterios = cargar_criterios(args.criterios)
    prompt_princpal = cargar_prompt_principal(args.prompt_principal)

    # Procesar todos los archivos .zip
    resultados = procesar_zip_estudiantes(args.carpeta)

    # Generar y guardar el feedback para cada archivo .zip
    for resultado in resultados:
        codigo = resultado['codigo']
        prompt = construir_prompt(codigo, criterios, prompt_princpal)
        feedback = evaluar_con_openai(prompt)

        # Crear un nombre único para el archivo de salida basado en el nombre del .zip
        nombre_salida = os.path.splitext(resultado['zip'])[0]  # Nombre del archivo ZIP sin la extensión
        salida = "reportes/{nombre_salida}.md"  # Agregar el nombre del ZIP al reporte

        guardar_feedback(salida, feedback)
        print(f"✅ Feedback generado para {resultado['zip']} en: {salida}")

if __name__ == '__main__':
    main()
