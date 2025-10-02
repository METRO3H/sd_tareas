# Tarea 1 - Sistemas Distribuidos | Plataforma de análisis de preguntas y respuestas en Internet
![Docker](https://img.shields.io/badge/docker-ready-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-async-lightgreen)
![Redis](https://img.shields.io/badge/redis-caching-red)
![Postgres](https://img.shields.io/badge/postgres-storage-green)
![Kaggle](https://img.shields.io/badge/kaggle-dataset-orange)

Este es un proyecto para analizar el trafico de consultas segun distintas distribuciones, las distintas politicas y tamaños de cache, y la implementación de consultas a un llm (Gemini) para su posterior clasificación y almacenamiento en una base de datos. Todo esto implementado en contenedores docker y orquestado con docker-compose.

---

## 📑 Contenidos

- [Tarea 1 - Sistemas Distribuidos | Plataforma de análisis de preguntas y respuestas en Internet](#tarea-1---sistemas-distribuidos--plataforma-de-análisis-de-preguntas-y-respuestas-en-internet)
  - [📑 Contenidos](#-contenidos)
  - [🚦 ¿Que hace este proyecto?](#-que-hace-este-proyecto)
  - [📖 Características principales](#-características-principales)
  - [📁 Estructura del repositorio](#-estructura-del-repositorio)
  - [🛠️ Infraestructura](#️-infraestructura)
  - [🚀 Instalación y ejecución](#-instalación-y-ejecución)
  - [🧪 Ejecución de experimentos](#-ejecución-de-experimentos)
  - [👽 Extra](#-extra)
  - [👨‍💻 Autor](#-autor)

## 🚦 ¿Que hace este proyecto?

- Este proyecto genera trafico de consultas tomando como base el dataset de Yahoo Respuestas, las filtra, y luego a partir de dos distribuciones distintas (Gauss y Zipf) genera consultas a un servidor itermediario (middleware). Luego, este ultimo procesa la consulta segun el estado de esa consulta en la cache (Redis) o en la base de datos (Postgres). Si la consulta no se encuentra en ninguno de los dos, se consulta a un modelo de lenguaje (Gemini) para obtener una respuesta, la cual es evaluada y almacenada tanto en la base de datos como en cache. 


---

## 📖 Características principales

- 📡 **Generador de trafico**, desde el dataset de yahoo respuestas
- 🗃 **Almacenamiento en Postgres**, Aprovechando los datos con estructura fija.
- 🚀 **Servicio web con FastAPI**, para consultar facilmente entre los distintos servidores.
- ⚡ **Uso de Redis como caché**, para mejorar tiempos de respuesta.
- 🐳 **Contenedores Docker y orquestación con Docker Compose**.

---

## 📁 Estructura del repositorio

```plaintext
C:.
│  .env
│  docker-compose.yml
│  readme
│  Tarea_1_Sistemas_Distribuidos_2025_2.pdf
│  tests.py
│  toDo.md
│
├─cache
│      redis_1.conf
│      redis_10.conf
│      redis_11.conf
│      redis_12.conf
│      redis_2.conf
│      redis_3.conf
│      redis_4.conf
│      redis_5.conf
│      redis_6.conf
│      redis_7.conf
│      redis_8.conf
│      redis_9.conf
│
├─database
│      init.sql
│
├─generator
│  │  checkpoint.py
│  │  dataset.py
│  │  Dockerfile
│  │  gauss_distribution.py
│  │  generator.py
│  │  requirements.txt
│  │  zipf_distribution.py
│  │
│  ├─dataset
│  │      qa_yahoo.csv
│  
│
│
├─middleware_server
│  │  cache_manager.py
│  │  db.py
│  │  Dockerfile
│  │  m_server.py
│  │  requirements.txt
│  │
│  ├─p_types
│  │      types.py
│  
│
└─qa_score
    │  ask_gemini.py
    │  Dockerfile
    │  gemini_model.py
    │  requirements.txt
    │  score_answer.py
    │  sc_server.py

```

---
## 🛠️ Infraestructura
Cada uno de los servicios anteriormente descritos, estan creados de forma modular e independiente gracias a Docker-compose. Facilitando así,  el escalado y facil despliegue de los servicios.
El sistema está compuesto por servicios desplegados mediante Docker Compose, organizados de forma modular para facilitar pruebas y escalabilidad:

- **Postgres**: Base de datos para almacenar las consultas y sus respectivos resultados.
- **Redis**: Caché para acelerar consultas repetidas.
- **Generator**: Generador de tráfico para realizar experimentos de carga y cache.
- **Middleware_server**: Servicio itermediario que maneja el procesamiento de consultas, gestionando la lógica de caché, base de datos y llamadas a clasificar respuestas.
- **QA_score**: Servicio que interactúa con el modelo de lenguaje Gemini para obtener respuestas y evaluarlas.
- **RedisInsight**: Herramienta visual para monitorear el estado de las distintas instancias de redis.

Ademas, todos los servicios están conectados en una misma red Docker (`netuworku`), utilizan volúmenes persistentes y se inicializan con variables de entorno definidas en `.env`. Se configuran dependencias entre servicios para garantizar el orden de arranque.

Esto se puede ver con mas detalle en el archivo de configuración docker-compose.yml.

```yml
version: "3.9"

services:
    postgres:
        image: postgres:17
        container_name: "postgres"
        environment:
            - POSTGRES_USER=${POSTGRES_USER}
            - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
            - POSTGRES_DB=${POSTGRES_DB}
        volumes:
            - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
            - postgres_data:/var/lib/postgresql/data
        networks:
            - netuworku
        ports:
            - "5432:5432"

        healthcheck:
            test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
            interval: 10s
            timeout: 5s
            retries: 5
    
    qa_score:
        build: "./qa_score"
        container_name: "qa_score"
        environment:
            - GOOGLE_API_KEY_1=${GOOGLE_API_KEY_1}
            - GOOGLE_API_KEY_2=${GOOGLE_API_KEY_2}
            - GOOGLE_API_KEY_3=${GOOGLE_API_KEY_3}
        volumes:
            - ./qa_score:/app  
            - qa_score_data:/data/qa_score_data
        networks:
            - netuworku
        ports:
            - "8000:8000"
        healthcheck:
            test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
            interval: 11s
            timeout: 5s
            retries: 5
    middleware_server:
        build: "./middleware_server"
        container_name: "middleware_server"
        environment:
            - POSTGRES_HOST=${POSTGRES_HOST}
            - POSTGRES_USER=${POSTGRES_USER}
            - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
            - POSTGRES_DB=${POSTGRES_DB}
            - POSTGRES_PORT=5432
        
        volumes:
            - ./middleware_server:/app
            - middleware_server_data:/data/middleware_server_data
            - ./tests.py:/app/tests.py
        networks:
            - netuworku
        ports:
            - "8075:8075"
        healthcheck:
            test: ["CMD", "curl", "-f", "http://localhost:8075/health"]
            interval: 10s
            timeout: 5s
            retries: 5

        depends_on:
            postgres:
                condition: service_healthy
            qa_score:
                condition: service_healthy
            redis_1:
                condition: service_healthy
            redis_2:
                condition: service_healthy
            redis_3:
                condition: service_healthy
            redis_4:
                condition: service_healthy
            redis_5:
                condition: service_healthy
            redis_6:
                condition: service_healthy
            redis_7:
                condition: service_healthy
            redis_8:
                condition: service_healthy
            redis_9:
                condition: service_healthy
            redis_10:
                condition: service_healthy
            redis_11:
                condition: service_healthy
            redis_12:
                condition: service_healthy
            
    redisinsight:
        image: redislabs/redisinsight:2.70
        container_name: redisinsight
        restart: always
        ports:
            - "5540:5540"
        networks:
            - netuworku
        volumes:
            - redisinsight_data:/data
        depends_on:
            middleware_server:
                condition: service_healthy


    generator:
        build: "./generator"
        container_name: "generator"
        volumes:
            - ./generator:/app
            - generator_data:/data/generator_data
        networks:
            - netuworku
        depends_on:
            middleware_server:
                condition: service_healthy

    redis_1:
        image: redis:8.2.1
        container_name: "redis_1_gauss_lru_2mb"
        volumes:
            - ./cache/redis_1.conf:/usr/local/etc/redis/redis.conf
            - redis_1_data:/data
            
        command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
        networks:
            - netuworku
        ports:
            - "6379:6379"
        healthcheck:
            test: ["CMD", "redis-cli", "-p", "6379", "ping"]
            interval: 10s
            timeout: 5s
            retries: 5

    redis_2:
        image: redis:8.2.1
        container_name: "redis_2_gauss_lru_5mb"
        volumes:
            - ./cache/redis_2.conf:/usr/local/etc/redis/redis.conf
            - redis_2_data:/data
            
        command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
        networks:
            - netuworku
        ports:
            - "6380:6380"
        healthcheck:
            test: ["CMD", "redis-cli", "-p", "6380", "ping"]
            interval: 10s
            timeout: 5s
            retries: 5    
    redis_3:
        image: redis:8.2.1
        container_name: "redis_3_gauss_lru_10mb"
        volumes:
            - ./cache/redis_3.conf:/usr/local/etc/redis/redis.conf
            - redis_3_data:/data
            
        command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
        networks:
            - netuworku
        ports:
            - "6381:6381"
        healthcheck:
            test: ["CMD", "redis-cli", "-p", "6381", "ping"]
            interval: 10s
            timeout: 5s
            retries: 5    

    redis_4:
        image: redis:8.2.1
        container_name: "redis_4_gauss_lfu_2mb"
        volumes:
            - ./cache/redis_4.conf:/usr/local/etc/redis/redis.conf
            - redis_4_data:/data

        command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
        networks:
            - netuworku
        ports:
            - "6382:6382"
        healthcheck:
            test: ["CMD", "redis-cli", "-p", "6382", "ping"]
            interval: 10s
            timeout: 5s
            retries: 5

    redis_5:
        image: redis:8.2.1
        container_name: "redis_5_gauss_lfu_5mb"
        volumes:
            - ./cache/redis_5.conf:/usr/local/etc/redis/redis.conf
            - redis_5_data:/data
        command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
        networks:
            - netuworku
        ports:
            - "6383:6383"
        healthcheck:
            test: ["CMD", "redis-cli", "-p", "6383", "ping"]
            interval: 10s
            timeout: 5s
            retries: 5    

    redis_6:
        image: redis:8.2.1
        container_name: "redis_6_gauss_lfu_10mb"
        volumes:
            - ./cache/redis_6.conf:/usr/local/etc/redis/redis.conf
            - redis_6_data:/data
        command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
        networks:
            - netuworku
        ports:
            - "6384:6384"
        healthcheck:
            test: ["CMD", "redis-cli", "-p", "6384", "ping"]
            interval: 10s
            timeout: 5s
            retries: 5    

    redis_7:
        image: redis:8.2.1
        container_name: "redis_7_zipf_lru_2mb"
        volumes:
            - ./cache/redis_7.conf:/usr/local/etc/redis/redis.conf
            - redis_7_data:/data
        
        command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
        networks:
            - netuworku
        ports:
            - "6385:6385"
        healthcheck:
            test: ["CMD", "redis-cli", "-p", "6385", "ping"]
            interval: 10s
            timeout: 5s
            retries: 5


    redis_8:
        image: redis:8.2.1
        container_name: "redis_8_zipf_lru_5mb"
        volumes:
            - ./cache/redis_8.conf:/usr/local/etc/redis/redis.conf
            - redis_8_data:/data
        
        command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
        networks:
            - netuworku
        ports:
            - "6386:6386"
        healthcheck:
            test: ["CMD", "redis-cli", "-p", "6386", "ping"]
            interval: 10s
            timeout: 5s
            retries: 5    

    redis_9:
        image: redis:8.2.1
        container_name: "redis_9_zipf_lru_10mb"
        volumes:
            - ./cache/redis_9.conf:/usr/local/etc/redis/redis.conf
            - redis_9_data:/data
        
        command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
        networks:
            - netuworku
        ports:
            - "6387:6387"
        healthcheck:
            test: ["CMD", "redis-cli", "-p", "6387", "ping"]
            interval: 10s
            timeout: 5s
            retries: 5
    redis_10:
        image: redis:8.2.1
        container_name: "redis_10_zipf_lfu_2mb"
        volumes:
            - ./cache/redis_10.conf:/usr/local/etc/redis/redis.conf
            - redis_10_data:/data
        
        command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
        networks:
            - netuworku
        ports:
            - "6388:6388"
        healthcheck:
            test: ["CMD", "redis-cli", "-p", "6388", "ping"]
            interval: 10s
            timeout: 5s
            retries: 5

    redis_11:
        image: redis:8.2.1
        container_name: "redis_11_zipf_lfu_5mb"
        volumes:
            - ./cache/redis_11.conf:/usr/local/etc/redis/redis.conf
            - redis_11_data:/data
        
        command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
        networks:
            - netuworku
        ports:
            - "6389:6389"
        healthcheck:
            test: ["CMD", "redis-cli", "-p", "6389", "ping"]
            interval: 10s
            timeout: 5s
            retries: 5    

    redis_12:
        image: redis:8.2.1
        container_name: "redis_12_zipf_lfu_10mb"
        volumes:
            - ./cache/redis_12.conf:/usr/local/etc/redis/redis.conf
            - redis_12_data:/data
        
        command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
        networks:
            - netuworku
        ports:
            - "6390:6390"
        healthcheck:
            test: ["CMD", "redis-cli", "-p", "6390", "ping"]
            interval: 10s
            timeout: 5s
volumes:
  qa_score_data:
  generator_data:
  postgres_data:
  middleware_server_data:
  redisinsight_data:
  redis_1_data:
  redis_2_data:
  redis_3_data:
  redis_4_data:
  redis_5_data:
  redis_6_data:
  redis_7_data:
  redis_8_data:
  redis_9_data:
  redis_10_data:
  redis_11_data:
  redis_12_data:
  
networks:
   netuworku:
      driver: bridge
```

Finalmente, se puede ver que todos los contenedores comparten la misma network. Se definieron volumenes de docker los cuales guardan los datos del scrapeo, de redis, y los resultados de los experimentos a ejecutar. Los contenedores se inicializan con variables de entorno ya definidas en un archivo .env en la carpeta raiz. Y se configuraron dependencias de inicialización para ciertos contenedores, de forma que tanto middleware_server como generator, solo se inicien una vez que los servicios de postgres, redis y qa_score esten activos y funcionando correctamente.

## 🚀 Instalación y ejecución

1. Clona el repositorio:

```bash
git clone https://github.com/METRO3H/sd_tareas
cd sd_tarea_1
```

2. Crea un archivo `.env` en la raíz del proyecto con este contenido:

```env
# Gemini API Key
GOOGLE_API_KEY_1=XXXXXXXXXXXXXXXXXXXXXXXXXX
GOOGLE_API_KEY_2=XXXXXXXXXXXXXXXXXXXXXXXXXX
GOOGLE_API_KEY_3=XXXXXXXXXXXXXXXXXXXXXXXXXX

# Postgres parameters
POSTGRES_HOST=postgres
POSTGRES_USER=bob
POSTGRES_PASSWORD=ga30mpqbkIzaSyVDr8_s
POSTGRES_DB=postgres
```
3. Desde [Kaggle](https://www.kaggle.com/datasets/jarupula/yahoo-answers-dataset), descargar el dataset test.csv de Yahoo Respuestas, renombrarlo y guardarlo en `./generator/dataset/qa_yahoo.csv`.

```bash
mkdir -p ./generator/dataset
mv ./path/to/downloaded/test.csv ./generator/dataset/qa_yahoo.csv
```

4. Levanta los servicios con Docker Compose:

```yml
docker-compose build;
docker-compose up -d;
docker-compose logs generator -f;
```

5. Accede a los servicios disponibles

- [http://localhost:8075/docs](http://localhost:8075/docs) – Interfaz de middleware_server.
- [http://localhost:8000/docs](http://localhost:8000/docs) – Interfaz de qa_score.
- [http://localhost:5540/](http://localhost:5540/) – Interfaz web de Redis insight.

6. Ejemplo de consulta a qa_score:

```bash
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the capital of france?", "yahoo_answer": "Paris"}'
```

Respuesta esperada del server:

```json
{
  "gemini_answer": "The capital of France is **Paris**. \n\nIt’s a common misconception that Paris is the *only* capital, but it’s the official and most widely recognized one.",
  "score": 78
}
```

## 🧪 Ejecución de experimentos
Los experimentos a realizar por parte del **generator** son los siguientes:

- Experimento 1: Gauuss - LRU - 2MB
- Experimento 2: Gauuss - LRU - 5MB
- Experimento 3: Gauuss - LRU - 10MB
- Experimento 4: Gauuss - LFU - 2MB
- Experimento 5: Gauuss - LFU - 5MB
- Experimento 6: Gauuss - LFU - 10MB
- Experimento 7: Zipf - LRU - 2MB
- Experimento 8: Zipf - LRU - 5MB
- Experimento 9: Zipf - LRU - 10MB
- Experimento 10: Zipf - LFU - 2MB
- Experimento 11: Zipf - LFU - 5MB
- Experimento 12: Zipf - LFU - 10MB

Cada uno de los anteriores experimentos se puede ir auditando con los respectivos logs de cada contenedor:

```yml
docker logs generator -f
docker logs middleware_server -f
docker logs qa_score -f
```
## 👽 Extra

Buen comando para empezar desde cero, eliminando todos los volumenes de docker menos el de redisinsight_data (ya que ahi se guardan las configuraciones de las distintas instancias de redis).

```bash
docker-compose down; docker volume ls -q | grep -v "redisinsight_data" | xargs -r docker volume rm
docker-compose up -d
```
---

## 👨‍💻 Autor

- [METRO3H](https://github.com/METRO3H)
