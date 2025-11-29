# usm_app
The Application is built on a microservice architecture, separating the web interface, user modules, and summarization engine into independently scalable components.

<img width="2367" height="1803" alt="usm_diagram" src="https://github.com/user-attachments/assets/1445e6ad-b3fa-4f39-8329-f5a32fded2dd" />

<img width="1899" height="930" alt="Screenshot 2025-11-29 100617" src="https://github.com/user-attachments/assets/fec98692-edde-41c9-907f-0196566d22ea" />

<img width="1902" height="930" alt="Screenshot 2025-11-29 103433" src="https://github.com/user-attachments/assets/1b17eb58-686f-44fc-b1ac-ad1ffd662480" />

<img width="1903" height="928" alt="Screenshot 2025-11-29 103722" src="https://github.com/user-attachments/assets/09c63ef2-824d-4877-a944-069959d0b582" />

Key technical highlights:

-> Loosely Coupled Microservices enabling cleaner interfaces and independent deployment cycles.
-> Summarization Engine using a Map-Reduce Approach, allowing large content to be chunked, processed, and aggregated efficiently.
-> Single-Page Application served via Django, providing a smooth UI experience.
-> Django + DRF + FastAPI Hybrid Stack, blending reliability with high-performance async workloads.
-> Async Task Execution via Celery + Redis, offloading heavy summarization tasks and maintaining responsiveness.
-> Frontend UI fully generated using LLM-assisted workflow, accelerating the design cycle.
