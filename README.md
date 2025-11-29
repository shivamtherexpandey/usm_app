# usm_app
The Application is built on a microservice architecture, separating the web interface, user modules, and summarization engine into independently scalable components.

Key technical highlights:

-> Loosely Coupled Microservices enabling cleaner interfaces and independent deployment cycles.
-> Summarization Engine using a Map-Reduce Approach, allowing large content to be chunked, processed, and aggregated efficiently.
-> Single-Page Application served via Django, providing a smooth UI experience.
-> Django + DRF + FastAPI Hybrid Stack, blending reliability with high-performance async workloads.
-> Async Task Execution via Celery + Redis, offloading heavy summarization tasks and maintaining responsiveness.
-> Frontend UI fully generated using LLM-assisted workflow, accelerating the design cycle.