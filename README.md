# Solution\_Camunda\_Challenge

This repository contains a minimal microservice that fetches random pictures of **cats**, **dogs**, or **bears** using public APIs. It stores these images in a local SQLite database and provides a simple REST API and HTML UI to fetch or retrieve the most recent picture of each animal type.

The solution was built by **Ilja Tscharikow** for the **Camunda Tech Challenge** as part of the TAM application process.

While Java was mentioned as a primary language at Camunda, I chose **Python** for this MVP due to my deeper experience with it. It enabled faster prototyping and debugging within the given timeframe. Therefore, since this project is implemented in Python rather than Java, it does not rely on a traditional build tool like Maven or Gradle. Instead, it uses Docker as the build and packaging tool. The provided Dockerfile creates a fully portable build of the application. It installs all dependencies, copies the full project, and exposes it on port 8000. The resulting container can be deployed and run on any system with Docker installed — with no need for manual setup or pre-installed Python environments. The SQLite database is created inside the container automatically at runtime, so there are no assumptions about local database installations.



Where helpful, I used **generative AI** to support implementation steps — such as validating syntax, researching libraries and API structures or writing proper documentation. However, the **project logic, architectural design and coding decisions** were created and structured manually. I handled all system integration and infrastructure setup hands-on. Out of transparency I have to admit, that otherwise it would not have been possible for me to reach this coding result in a little over 2 hours. README was written mainly after finishing the challenge. 

---

### 🔧 How to Run (Docker)

💡 Docker allows you to run the full app in a prebuilt, self-contained container - no need to install Python or set up anything locally. 

💡 If you are using GitHub Codespaces, DevContainers or VS Code Remote environments (like I did), Docker may already be installed and configured for you — so you can skip installation and go directly to building the image. This image is based on python:3.12-slim and includes all dependencies from requirements.txt.

#### 1. Install Docker (if you don't have it yet)

* Download and install Docker Desktop: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
* Start Docker Desktop and ensure it is running
* You can verify the installation by running:

```bash
docker --version
```

#### 2. Get the project folder 

**If cloned from GitHub:**

💡 If this was a production system, I would have pushed it to Docker Hub - but for this MVP it is not required. Below we will build the image locally from the Dockerfile. 

```bash
git clone https://github.com/Ilja2307/Solution_Camunda_Challenge.git
cd Solution_Camunda_Challenge
```

**If downloaded as ZIP:**

1: Extract the ZIP file on your machine

2: Open a terminal inside the extracted folder (name may vary):

```bash
cd Solution_Camunda_Challenge-main
```


#### 3. Build the Docker image

```bash
docker build -t camunda-animal-service .
```

#### 4. Run the Docker container

```bash
docker run -p 8000:8000 camunda-animal-service
```

The app will now be accessible in your browser. Make sure port 8000 is open and accessible in your local/dev environment and not blocked by a firewall or already in use:

* UI: [http://localhost:8000/ui](http://localhost:8000/ui)
* API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

💡 If you're running this in GitHub Codespaces or a cloud-based dev environment, your preview link might look like:
https\://<random-id>-8000.preview\.app.github.dev

---

## 🧱 Manual Setup (No Docker)

Follow these steps if you want to run the app directly on your machine without Docker:

### 1. Install Python (if not already installed)

* Python 3.12.1+ is used in this project: [https://www.python.org/downloads/](https://www.python.org/downloads/)

#### 2. Get the project folder 

**If cloned from GitHub:**

```bash
git clone https://github.com/Ilja2307/Solution_Camunda_Challenge.git
cd Solution_Camunda_Challenge
```

**If downloaded as ZIP:**

1: Extract the ZIP file on your machine

2: Open a terminal and navigate into the extracted folder after extracting the ZIP (name may vary depending on your system):

```bash
cd Solution_Camunda_Challenge-main
```

### 3. (Optional) Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Initialize the database

```bash
python -c "from app.init_db import init; init()"
```

### 6. Start the FastAPI Server

```bash
python -m uvicorn app.main:app --reload
```

Once running, you can access:

* UI: [http://localhost:8000/ui](http://localhost:8000/ui)
* API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🌐 Endpoints

| Endpoint              | Method   | Description                                      |
| --------------------- | -------- | ------------------------------------------------ |
| `/fetch`              | POST     | Fetch and save `n` images of a given animal type |
| `/last/{animal_type}` | GET      | Retrieve the last saved image for that type      |
| `/ui`                 | GET/POST | Simple browser UI form for interaction           |
| `/`                   | GET      | Welcome message and navigation links             |
| `/docs`               | GET      | Swagger UI documentation                         |
| `/health`             | GET      | Basic health check                               |

---

## 📁 Structure Overview

```
Solution_Camunda_Challenge/
│
├── app/
│   ├── api.py           # REST API routes (UI & logic mixed)
│   ├── fetcher.py       # API integration logic (external image services)
│   ├── models.py        # SQLAlchemy model for DB entries
│   ├── database.py      # SQLite DB setup and engine configuration
│   ├── init_db.py       # One-time DB init script
│   ├── main.py          # FastAPI app entry point + UI routes
│   └── templates/       # Jinja2 HTML templates for UI
│       ├── index.html
│       └── welcome.html
│
├── Dockerfile
├── requirements.txt
```

---

## ✅ Implemented Features

* REST API for image fetching and last-image retrieval
* Public API integration with image format filtering
* Persistent image storage using **SQLite** and SQLAlchemy ORM
* HTML UI with dropdown and fetch controls
* Dockerized deployment for platform independence
* Automatic database initialization when container starts
* Simple terminal logging via `print()`
* Non-container setup instructions with database bootstrapping

---

## ❌ Features Not Implemented (but how I would go on from here)

💡 Below is a list of features commonly seen in production systems that I have not implemented. While automated tests are considered a nice bonus for an MVP like this, the other features listed below are critical for real-world deployments and deserve mention. There are of course many more such as proper CORS configuration, security headers or using robust servers and others that could be added in an even more advanced prototype. 


| Feature                              | Status | Implementation Plan                                                                                                                                                                                                                                         |
| ------------------------------------ | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Automated tests                      | ❌      | I would use `pytest` and `httpx.AsyncClient` to test endpoints. I'd configure a separate in-memory SQLite DB for tests and mock external image APIs for repeatable results. Due to time constraints and focus on MVP functionality, this step was excluded. |
| Observability/Monitoring             | ❌      | Logging could be improved with `logging` module. Health metrics and request tracing could be added via Prometheus or OpenTelemetry.                                                                                                                         |
| Error handling for failing APIs      | ❌      | Currently no fallback or retry strategy beyond format filtering. I'd wrap calls in try/except blocks with logging and error responses.                                                                                                                      |
| Type checking for external responses | ❌      | Assumes schema structure (e.g., `data[0]['url']`). I would use Pydantic models or manual schema validation for robustness.                                                                                                                                  |
| Extensibility (e.g., more animals)   | ❌      | Adding a new animal would require edits in multiple files. A better design would use a configuration map or plug-in pattern to register supported types dynamically.                                                                                        |
| Service abstraction layer            | ❌      | Logic is currently implemented directly inside route handlers. For testability and scalability, it should be moved into separate service or controller layers.                                                                                              |

---

## 🔗 References of used public API

* [The Cat API](https://thecatapi.com)
* [Random Dog API](https://random.dog/woof.json)
* [PlaceBear](https://placebear.com/)

---

### 🐾 Note on Image APIs

The challenge description mentioned `placekitten`, `place.dog`, and `placebear`.  
At the time of implementation, the `placekitten` and `place.dog` APIs were not reachable, so they were replaced with **TheCatAPI** (cats) and **random.dog** (dogs).  
`placebear` remained unchanged.

**Reason:** The chosen replacements are stable, actively maintained, and return direct image URLs suitable for automated fetching and storage. Functionally, they serve the same purpose and align with the challenge’s intent.

---

### Submission adjustments (post-review)
- Reduced dependencies to a minimal set to avoid long Docker builds.
- Removed a previously committed SQLite database file; the DB is created at startup. Reasoning: Avoid inflated dependencies (longer build times) and shipping local DB artifacts.


---

## 🧠 Learnings & Reflection

While I understand infrastructure concepts like REST, APIs and Docker in theory, I am not a software developer. I had to revisit many technical details to deliver a working MVP — especially around asynchronous I/O, Docker setup and database integration.

Mistakes like missing dependencies, async call errors, or poor formatting initially slowed me down. However, my background helped me debug these quickly and use better prompts with generative AI to research solutions faster.

Ultimately, this exercise helped sharpen my technical mindset, forced me to deliver end-to-end and reminded me of the trade-offs between clean design and MVP speed. I’m confident that I can bridge technical conversations, guide implementation decisions and build practical prototypes — which aligns well with the TAM role's focus on communication, architecture and value delivery.