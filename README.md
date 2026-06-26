# AI Recon Assistant

Asistente de reconocimiento en Python que automatiza tareas básicas de recolección de información, procesamiento de resultados, recuperación de contexto local mediante RAG y generación de análisis asistido por IA.

## Descripción

AI Recon Assistant es un script desarrollado en Python para apoyar tareas de reconocimiento en entornos de laboratorio de ciberseguridad. La herramienta solicita una IP objetivo y ejecuta distintas acciones de recolección de información, como Ping, Traceroute, Nmap y Curl.

Posteriormente, el script procesa los resultados mediante Scikit-Learn, extrae palabras clave relevantes, consulta una base de conocimiento local ubicada en la carpeta `knowledge_base/` y envía la información a un modelo de IA mediante la API de OpenAI. Finalmente, genera un reporte en formato Markdown con la evidencia técnica recolectada y el análisis generado.

El objetivo del proyecto es demostrar cómo integrar herramientas tradicionales de reconocimiento con técnicas básicas de procesamiento de texto, recuperación de contexto local y análisis asistido por inteligencia artificial.

## Funcionalidades

* Validación de conectividad mediante Ping.
* Identificación de ruta de red mediante Traceroute.
* Escaneo de servicios y versiones con Nmap.
* Obtención de cabeceras HTTP mediante Curl.
* Extracción de palabras clave con Scikit-Learn.
* Recuperación de contexto desde una base de conocimiento local.
* Comparación de resultados mediante cosine similarity.
* Análisis asistido por IA usando OpenAI API.
* Generación automática de reportes Markdown.
* Inclusión de un reporte de ejemplo para referencia.

## Arquitectura general

```text
Usuario
  ↓
Ingreso de IP objetivo
  ↓
Ping / Traceroute / Nmap / Curl
  ↓
Procesamiento con Scikit-Learn
  ↓
Extracción de palabras clave
  ↓
Recuperación de contexto local desde knowledge_base/
  ↓
Análisis mediante OpenAI API
  ↓
Generación de reporte Markdown
```

## Estructura del proyecto

```text
ai_recon_assistant/
├── ai_recon_assistant.py
├── requirements.txt
├── README.md
├── .gitignore
├── knowledge_base/
│   ├── services.txt
│   ├── contexto_recon.txt
│   ├── vulnerabilidades.txt
│   └── mitre.txt
└── examples/
    └── report_example.md
```

## Requisitos

* Python 3
* Nmap
* Traceroute
* Curl
* Cuenta o clave API de OpenAI
* Entorno Linux recomendado, por ejemplo Kali Linux

## Instalación de dependencias Python

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` debe incluir:

```text
python-dotenv
scikit-learn
openai
```

## Instalación de herramientas del sistema

En Kali Linux o distribuciones basadas en Debian:

```bash
sudo apt update
sudo apt install nmap traceroute curl
```

## Configuración de variable de entorno

El script requiere una clave API de OpenAI configurada en un archivo `.env`.

Crea un archivo llamado `.env` en la misma carpeta del script:

```env
OPENAI_API_KEY=tu_api_key_aqui
```

Importante: el archivo `.env` no debe subirse al repositorio.

## Base de conocimiento RAG

El proyecto utiliza una carpeta llamada `knowledge_base/` para almacenar archivos `.txt` que sirven como contexto local para el análisis.

Ejemplo de archivos:

```text
knowledge_base/services.txt
knowledge_base/contexto_recon.txt
knowledge_base/vulnerabilidades.txt
knowledge_base/mitre.txt
```

Estos documentos son leídos por el script y comparados con los resultados recolectados mediante Scikit-Learn y cosine similarity. El contexto más relevante se incorpora al prompt enviado al modelo de IA.

## Uso

Ejecuta el script con:

```bash
python ai_recon_assistant.py
```

Luego ingresa la IP objetivo cuando el programa lo solicite:

```text
Ingrese IP objetivo: 10.10.1.129
```

## Herramientas ejecutadas por el script

El flujo de reconocimiento incluye:

```text
Ping
Traceroute
Nmap
Curl
```

El escaneo Nmap utilizado por el script incluye:

```bash
nmap -sV -sC -O -T4 <IP>
```

Donde:

* `-sV` detecta servicios y versiones.
* `-sC` ejecuta scripts NSE por defecto.
* `-O` intenta detectar el sistema operativo.
* `-T4` aumenta la velocidad del escaneo en entornos de laboratorio.

## Reporte generado

El script genera reportes Markdown automáticamente con nombres incrementales:

```text
report_01.md
report_02.md
report_03.md
```

Cada reporte incluye:

* Objetivo evaluado.
* Palabras clave detectadas.
* Contexto recuperado mediante RAG.
* Análisis generado por IA.
* Evidencia técnica recolectada.
* Descripción de la arquitectura del script.

## Reporte de ejemplo

El repositorio incluye un reporte de ejemplo en la carpeta:

```text
examples/report_example.md
```

Este archivo permite visualizar el formato esperado del resultado generado por el asistente.

## Uso previsto

Este proyecto está orientado a:

* Laboratorios de ciberseguridad.
* Actividades académicas.
* Pruebas controladas.
* Reconocimiento defensivo autorizado.
* Experimentación con IA aplicada a seguridad.
* Demostración de integración entre herramientas clásicas y modelos de lenguaje.

## Advertencia

Este script debe utilizarse únicamente en sistemas propios, laboratorios controlados o entornos donde se cuente con autorización expresa para realizar pruebas de seguridad. El uso no autorizado contra sistemas de terceros puede ser ilegal.

## Notas de seguridad

No subas al repositorio:

```text
.env
API keys
tokens
credenciales
venv/
report_*.md
```

El archivo `.gitignore` debe excluir variables sensibles, entornos virtuales y reportes generados automáticamente.


### imagenes de referencia

<img width="921" height="288" alt="image" src="https://github.com/user-attachments/assets/7ab04a9b-5815-4837-a066-bd9180784ebe" />
<img width="800" height="300" alt="image" src="https://github.com/user-attachments/assets/b23e7628-99dc-4445-af8c-ea0bb669e0a5" />
<img width="921" height="598" alt="image" src="https://github.com/user-attachments/assets/30e76791-eb19-4347-94ea-1e135a53ee53" />
<img width="811" height="344" alt="image" src="https://github.com/user-attachments/assets/de19dfb3-3be0-491f-ab3b-120dff19dfc9" />
<img width="921" height="405" alt="image" src="https://github.com/user-attachments/assets/cfbdf00a-a42e-4ba9-bdd8-8fb6273d891c" />
<img width="921" height="256" alt="image" src="https://github.com/user-attachments/assets/13037c12-f734-4a1c-b200-e47c44066582" />
<img width="921" height="158" alt="image" src="https://github.com/user-attachments/assets/2e18bd70-50f6-47b2-9899-7fac17cbe1c7" />
<img width="921" height="254" alt="image" src="https://github.com/user-attachments/assets/4be059f8-1fe2-4e73-ba84-6eb6400ef88d" />
<img width="921" height="183" alt="image" src="https://github.com/user-attachments/assets/a3bb2e96-32f6-4878-ba5b-565a0255f3f1" />








