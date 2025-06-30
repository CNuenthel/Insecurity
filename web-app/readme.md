# Insecure WebApp

A deliberately vulnerable Python Flask web application to demonstrate common web security flaws. 

Currently included flaws:
- SQL Injection
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Insecure File Upload
- Broken Authentication

## 🚀 Getting Started

### Prerequisites
- Docker
- Docker Compose

### Run the App

```bash
git clone https://github.com/CNuenthel/Insecurity.git
cd Insecurity/web-app
docker-compose up --build
```