#!/usr/bin/env python3

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
# OpenAI permite consumir APIs compatibles con el formato OpenAI.
# También puede usarse con otros proveedores si entregan un endpoint compatible.


# ============================================================
# CARGA DE VARIABLES DE ENTORNO
# ============================================================

load_dotenv()
# Carga las variables definidas en el archivo .env.

# LLM_API_KEY   = clave API del proveedor
# LLM_BASE_URL  = URL base del proveedor compatible
# LLM_MODEL     = modelo que se utilizará
#
# Ejemplo para OpenAI:
# LLM_API_KEY=tu_api_key_de_openai
# LLM_BASE_URL=https://api.openai.com/v1
# LLM_MODEL=gpt-4o-mini
#
# Ejemplo para otro proveedor compatible:
# LLM_API_KEY=tu_api_key_del_proveedor
# LLM_BASE_URL=https://api.proveedor-ejemplo.com/v1
# LLM_MODEL=nombre-del-modelo
#

llm_api_key = os.getenv("LLM_API_KEY")
llm_base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
llm_model = os.getenv("LLM_MODEL", "gpt-4o-mini")

if llm_api_key:
    print("[+] API Key del proveedor LLM cargada correctamente")
else:
    print("[-] No se encontró LLM_API_KEY")
    print("Configura la variable en el archivo .env")
    print("")
    print("Ejemplo:")
    print("LLM_API_KEY=tu_api_key_aqui")
    print("LLM_BASE_URL=https://api.openai.com/v1")
    print("LLM_MODEL=gpt-4o-mini")
    exit()

client = OpenAI(
    api_key=llm_api_key,
    base_url=llm_base_url
)

print(f"[+] Proveedor LLM configurado: {llm_base_url}")
print(f"[+] Modelo configurado: {llm_model}")


# ============================================================
# EJECUCIÓN DE NMAP
# ============================================================

def run_nmap_scan(target):
    """
    Ejecuta Nmap contra el objetivo indicado.

    Parámetros:
        target: IP o dominio objetivo.

    Retorna:
        Salida estándar de Nmap o mensaje de error.
    """

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
            timeout=300
        )

        return result.stdout if result.stdout else result.stderr

    except Exception as e:
        return f"Error ejecutando Nmap: {e}"


# ============================================================
# EJECUCIÓN DE PING
# ============================================================

def run_ping(target):
    """
    Ejecuta ping para validar conectividad básica con el objetivo.
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


# ============================================================
# EJECUCIÓN DE TRACEROUTE
# ============================================================

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


# ============================================================
# EJECUCIÓN DE CURL
# ============================================================

def run_curl(target):
    """
    Ejecuta curl para obtener cabeceras HTTP del objetivo.

    Por defecto consulta:
        http://<target>
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


# ============================================================
# PROCESAMIENTO CON SCIKIT-LEARN
# ============================================================

def extract_keywords(text_data):
    """
    Procesa los resultados usando Scikit-Learn.

    Usa CountVectorizer para extraer palabras clave relevantes desde
    la evidencia técnica recolectada.
    """

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


# ============================================================
# CARGA DE BASE DE CONOCIMIENTO RAG
# ============================================================

def load_knowledge_base(path="knowledge_base"):
    """
    Carga archivos .txt desde la carpeta knowledge_base.

    Esta carpeta funciona como base de conocimiento local para RAG.

    Estructura sugerida:
        knowledge_base/
        ├── services.txt
        ├── contexto_recon.txt
        ├── vulnerabilidades.txt
        └── mitre.txt
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


# ============================================================
# RECUPERACIÓN DE CONTEXTO RAG
# ============================================================

def retrieve_context(query_text, documents, filenames, top_k=2):
    """
    Implementa un RAG simple.

    Compara los resultados del reconocimiento con los documentos
    locales de la base de conocimiento usando CountVectorizer y
    cosine similarity.

    Retorna:
        Fragmentos de contexto más relevantes.
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


# ============================================================
# ANÁLISIS CON LLM
# ============================================================

def analyze_with_llm(target, combined_results, keywords, rag_context):
    """
    Envía la información recolectada al LLM configurado en .env.

    El análisis incluye:
        1. Servicios detectados.
        2. Posibles riesgos.
        3. Técnicas MITRE ATT&CK relacionadas.
        4. Recomendaciones iniciales de evaluación.
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
- No entregues instrucciones de explotación.
- Enfoca las recomendaciones en evaluación, validación y mitigación defensiva.
"""

    try:
        response = client.chat.completions.create(
            model=llm_model,
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


# ============================================================
# GENERACIÓN DE REPORTE MARKDOWN
# ============================================================

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

    existing_reports = glob.glob("report_*.md")

    report_number = len(existing_reports) + 1

    filename = f"report_{report_number:02d}.md"

    report_content = f"""# Reporte de Reconocimiento Asistido por IA

## Objetivo Evaluado
{target}

## Proveedor LLM Utilizado
- Endpoint configurado: {llm_base_url}
- Modelo utilizado: {llm_model}

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
- API compatible con formato OpenAI
- Modelo configurable mediante .env

5. Reporte automático
- Generación incremental de archivos Markdown

Reporte generado automáticamente por ai_recon_assistant.py
"""

    with open(filename, "w", encoding="utf-8") as file:
        file.write(report_content)

    print(f"[+] Reporte generado correctamente: {filename}")


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():
    """
    Flujo principal del programa:

    1. Solicita una IP objetivo.
    2. Ejecuta Ping.
    3. Ejecuta Traceroute.
    4. Ejecuta Nmap.
    5. Ejecuta Curl.
    6. Combina evidencia técnica.
    7. Extrae palabras clave.
    8. Carga base de conocimiento RAG.
    9. Recupera contexto relevante.
    10. Consulta al LLM.
    11. Genera reporte Markdown.
    """

    target = input("\nIngrese IP objetivo: ").strip()

    if not target:
        print("[-] No se ingresó un objetivo válido.")
        return

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


if __name__ == "__main__":
    main()
