# AI Recon Assistant

Asistente de reconocimiento en Python que automatiza tareas básicas de recolección de información, procesamiento de resultados, recuperación de contexto local mediante RAG y generación de análisis asistido por IA.

## Descripción

AI Recon Assistant es un script desarrollado en Python para apoyar tareas de reconocimiento en entornos de laboratorio de ciberseguridad. La herramienta solicita una IP objetivo y ejecuta distintas acciones de recolección de información, como Ping, Traceroute, Nmap y Curl.

Posteriormente, el script procesa los resultados mediante Scikit-Learn, extrae palabras clave relevantes, consulta una base de conocimiento local y envía la información a un modelo de IA mediante la API de OpenAI. Finalmente, genera un reporte en formato Markdown con la evidencia técnica recolectada y el análisis generado.

## Funcionalidades

- Validación de conectividad mediante Ping.
- Identificación de ruta de red mediante Traceroute.
- Escaneo de servicios y versiones con Nmap.
- Obtención de cabeceras HTTP mediante Curl.
- Extracción de palabras clave con Scikit-Learn.
- Recuperación de contexto desde una base de conocimiento local.
- Comparación de resultados mediante cosine similarity.
- Análisis asistido por IA usando OpenAI API.
- Generación automática de reportes Markdown.

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
Recuperación de contexto local RAG
  ↓
Análisis mediante OpenAI API
  ↓
Generación de reporte Markdown
```
instalar dependencias 
pip install -r requirements.txt

Crea un archivo llamado .env en la misma carpeta del script:

OPENAI_API_KEY=tu_api_key_aqui o la que prefieras o utilices solo cambia este parametrto en el script.

Ejecuta el script con:

python ai_recon_assistant.py

Luego ingresa la IP objetivo cuando el programa lo solicite:

Ingrese IP objetivo: 10.10.1.129

descarga knowledge_base con los ejemplos de un rag basico para este script.

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








