import argparse
import json
import os
from datetime import datetime
from openai import OpenAI

# Inicializar cliente con la API Key desde variable de entorno
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def cargar_codigo(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        return f.read()
        
def cargar_promt_princpal(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        return f.read()

def cargar_criterios(ruta_json):
    with open(ruta_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['criterios']

def construir_prompt(codigo, criterios, promt_princpal):
    prompt = promt_principal
    prompt += "### Código del Estudiante:\n"
    prompt += f"```\n{codigo}\n```\n\n"
    prompt += "### Criterios de Evaluación:\n"
    for i, criterio in enumerate(criterios, 1):
        prompt += f"{i}. {criterio['nombre']} ({criterio['puntaje_maximo']} pts): {criterio['descripcion']}\n"
    prompt += "\nDevuelve una tabla con:\n- Criterio\n- Puntaje otorgado\n- Comentario\nY al final una nota total sobre 100.\n"
    return prompt

def evaluar_con_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un evaluador académico de código Java."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def guardar_feedback(ruta_salida, contenido):
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(f"# Reporte de Evaluación\n\n")
        f.write(f"Generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(contenido)
        f.write("\n")

def main():
    parser = argparse.ArgumentParser(description='Generar feedback con IA.')
    parser.add_argument('--codigo', required=True, help='Ruta al archivo de código .java')
    parser.add_argument('--criterios', required=True, help='Ruta al archivo criterios.json')
    parser.add_argument('--promt_principal', required=True, help='Prompt a utilizar')
    parser.add_argument('--salida', required=True, help='Ruta de salida del reporte Markdown')

    args = parser.parse_args()

    codigo = cargar_codigo(args.codigo)
    criterios = cargar_criterios(args.criterios)
    promt_princpal = cargar_promt_princpal(args.promt_principal)
    prompt = construir_prompt(codigo, criterios, promt_princpal)
    feedback = evaluar_con_openai(prompt)
    guardar_feedback(args.salida, feedback)

    print(f"✅ Feedback generado en: {args.salida}")

if __name__ == '__main__':
    main()
