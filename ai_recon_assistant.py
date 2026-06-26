import os
# os permite interactuar con variables del sistema operativo.

import subprocess
# subprocess permite ejecutar comandos del sistema operativo directamente desde Python.

import glob
# glob permite buscar archivos que cumplan un patrón.

from dotenv import load_dotenv
# python-dotenv permite cargar variables de entorno desde un archivo .env.

from sklearn.feature_extraction.text import CountVectorizer
# CountVectorizer permite transformar texto en palabras clave para análisis básico.

from sklearn.metrics.pairwise import cosine_similarity
# cosine_similarity permite comparar el resultado del escaneo con documentos de contexto.

from openai import OpenAI
# OpenAI permite consumir la API de ChatGPT desde Python.

### CARGA DE VARIABLES DE ENTORNO
load_dotenv()   # Carga las variables definidas en el archivo .env.

### LECTURA Y VALIDACIÓN DE API KEY
api_key = os.getenv("OPENAI_API_KEY")  # Lee la variable OPENAI_API_KEY desde el entorno.

if api_key:
    print("[+] API Key cargada correctamente")  #si existe la API KEY
else:
    print("[-] No se encontró OPENAI_API_KEY")  # Si no existe API Key, detenemos el programa.
    exit()

client = OpenAI(api_key=api_key)  # Cliente usado para consumir la API de OpenAI.

### EJECUCION DE NMAP
def run_nmap_scan(target):
   
    print(f"\n[+] Iniciando escaneo Nmap contra {target}...")

    command = [
        "nmap",
        "-sV",   # Detección de servicios y versiones.
        "-sC",   # Scripts NSE por defecto.
        "-O",    # Detección de sistema operativo.
        "-T4",   # Escaneo más rápido para laboratorio.
        target
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=300   ### PODEMOS MODIFICAR EL TIEMPO EN SEGUNDOS
        )

        return result.stdout if result.stdout else result.stderr

    except Exception as e:
        return f"Error ejecutando Nmap: {e}"

#### EJECUCION DE PING A LA MAQUINA
def run_ping(target):
    """
    Ejecuta ping para validar conectividad básica.
    """

    print(f"\n[+] Ejecutando Ping contra {target}...")

    command = ["ping", "-c", "4", target]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=20
        )

        return result.stdout if result.stdout else result.stderr

    except Exception as e:
        return f"Error ejecutando Ping: {e}"

### EJECUTA TRACEROUTE
def run_traceroute(target):
    """
    Ejecuta traceroute para identificar la ruta de red hacia el objetivo.
    """

    print(f"\n[+] Ejecutando Traceroute contra {target}...")

    command = ["traceroute", target]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60
        )

        return result.stdout if result.stdout else result.stderr

    except Exception as e:
        return f"Error ejecutando Traceroute: {e}"

##### DE DETECTAR UN URL PUEDE EJECUTAR CURL PARA EXTRAER LA CABECERA
def run_curl(target):
    """
    Ejecuta curl para obtener cabeceras HTTP.
    """

    print(f"\n[+] Ejecutando Curl contra {target}...")

    command = [
        "curl",
        "-I",
        "-L",
        "--max-time",
        "15",
        f"http://{target}"
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=20
        )

        return result.stdout if result.stdout else result.stderr

    except Exception as e:
        return f"Error ejecutando Curl: {e}"

### Procesa los resultados usando Scikit-Learn, Extrae palabras clave relevantes.
def extract_keywords(text_data):

    print("\n[+] Procesando información con Scikit-Learn...")

    try:
        vectorizer = CountVectorizer(
            stop_words="english",
            max_features=25
        )

        vectorizer.fit_transform([text_data])
        keywords = vectorizer.get_feature_names_out()

        return list(keywords)

    except Exception as e:
        return [f"Error procesando información: {e}"]

#### CARGA LOS ARCHIVOS DEL RAG QUE CREAMOS
def load_knowledge_base(path="knowledge_base"):
    """
    Carga archivos .txt desde la carpeta knowledge_base.
    Esta carpeta funciona como base de conocimiento para RAG.
    """

    documents = []
    filenames = []

    if not os.path.exists(path):
        return documents, filenames

    for file in os.listdir(path):
        if file.endswith(".txt"):
            filepath = os.path.join(path, file)

            with open(filepath, "r", encoding="utf-8") as f:
                documents.append(f.read())
                filenames.append(file)

    return documents, filenames

### COMPARACION DE RESULTADOS
def retrieve_context(query_text, documents, filenames, top_k=2):
    """
    Implementa un RAG simple.
    Compara los resultados del escaneo con la base local.
    """

    if not documents:
        return "No se encontró contexto RAG disponible."

    vectorizer = CountVectorizer(stop_words="english")

    all_texts = documents + [query_text]
    vectors = vectorizer.fit_transform(all_texts)

    query_vector = vectors[-1]
    document_vectors = vectors[:-1]

    similarities = cosine_similarity(query_vector, document_vectors)

    results = []

    for index, score in enumerate(similarities[0]):
        results.append({
            "filename": filenames[index],
            "score": score,
            "content": documents[index]
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    context = ""

    for item in results[:top_k]:
        context += f"\nFuente: {item['filename']}\n"
        context += item["content"]
        context += "\n"

    return context

#### ENVIA LA INOFRMACION AL LLM
def analyze_with_llm(target, combined_results, keywords, rag_context):
    """
    Envía la información recolectada al LLM.
    Genera análisis de servicios, riesgos, MITRE ATT&CK y recomendaciones.
    """

    print("\n[+] Consultando modelo LLM...")

    prompt = f"""
Actúa como un analista de ciberseguridad ofensiva dentro de un laboratorio autorizado.

Analiza la siguiente información recolectada sobre el objetivo.

OBJETIVO:
{target}

CONTEXTO RAG:
{rag_context}

PALABRAS CLAVE DETECTADAS:
{', '.join(keywords)}

RESULTADOS DE RECONOCIMIENTO:
{combined_results}

Genera un análisis en formato Markdown con estas secciones:

1. Servicios detectados
2. Posibles riesgos
3. Técnicas MITRE ATT&CK relacionadas
4. Recomendaciones iniciales de evaluación

Instrucciones:
- No inventes vulnerabilidades.
- Si falta información, indícalo claramente.
- Mantén el análisis dentro del contexto de laboratorio autorizado.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error consultando el LLM: {e}"

### GENERAR REPORTE .MD
def generate_markdown_report(target, combined_results, keywords, rag_context, ai_analysis):
    """
    Genera automáticamente un reporte Markdown sin sobrescribir anteriores.
    Formato:
    report_01.md
    report_02.md
    report_03.md
    """

    print("\n[+] Generando reporte Markdown...")

    keyword_section = "\n".join([f"- {word}" for word in keywords])

    # Buscar reportes existentes
    existing_reports = glob.glob("report_*.md")
    # Ejemplo: ["report_01.md", "report_02.md"]

    report_number = len(existing_reports) + 1
    # Si hay 2 reportes, el siguiente será 3

    filename = f"report_{report_number:02d}.md"
    # Formato 2 dígitos: 01, 02, 03...

    report_content = f"""# Reporte de Reconocimiento Asistido por IA

## Objetivo Evaluado
{target}

## Palabras Clave Detectadas con Scikit-Learn
{keyword_section}

## Contexto Recuperado mediante RAG
{rag_context}

## Análisis Generado por IA
{ai_analysis}

## Evidencia Técnica Recolectada
{combined_results}

---

## Arquitectura del Script

1. Recolección de información
- Ping
- Traceroute
- Nmap
- Curl

2. Procesamiento
- Scikit-Learn
- CountVectorizer

3. RAG
- Base de conocimiento local
- Cosine Similarity

4. IA Generativa
- OpenAI API
- GPT-4o-mini

5. Reporte automático

Reporte generado automáticamente por ai_recon_assistant.py
"""

    with open(filename, "w", encoding="utf-8") as file:
        file.write(report_content)

    print(f"[+] Reporte generado correctamente: {filename}")


# ---------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------

target = input("\nIngrese IP objetivo: ")

ping_result = run_ping(target)
traceroute_result = run_traceroute(target)
scan_result = run_nmap_scan(target)
curl_result = run_curl(target)

print("\n===== RESULTADO PING =====")
print(ping_result)

print("\n===== RESULTADO TRACEROUTE =====")
print(traceroute_result)

print("\n===== RESULTADO NMAP =====")
print(scan_result)

print("\n===== RESULTADO CURL =====")
print(curl_result)

combined_results = f"""
PING:
{ping_result}

TRACEROUTE:
{traceroute_result}

NMAP:
{scan_result}

CURL:
{curl_result}
"""

keywords = extract_keywords(combined_results)

print("\n===== PALABRAS CLAVE DETECTADAS =====")
for word in keywords:
    print(f"- {word}")

documents, filenames = load_knowledge_base()

rag_context = retrieve_context(
    combined_results,
    documents,
    filenames
)

ai_analysis = analyze_with_llm(
    target,
    combined_results,
    keywords,
    rag_context
)

print("\n===== ANÁLISIS GENERADO POR IA =====")
print(ai_analysis)

generate_markdown_report(
    target,
    combined_results,
    keywords,
    rag_context,
    ai_analysis
)