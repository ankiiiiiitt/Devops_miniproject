# FocusVault: AI-Powered Study Assistant (DevOps Edition) 🚀

FocusVault is a premium AI-powered study assistant built with Flask, MongoDB, and Groq AI. This repository is configured as a **Mini DevOps Project** demonstrating a complete CI/CD pipeline from local development to AWS EC2 deployment.

## 🛠️ DevOps Architecture
The project follows a standard industry-level DevOps flow:
**GitHub** ➔ **Jenkins** ➔ **Docker** ➔ **Docker Hub** ➔ **AWS EC2**

### CI/CD Pipeline Stages:
1. **Source Code**: Developers push code to the `main` branch on GitHub.
2. **CI Server (Jenkins)**: Automatically triggers the build process.
3. **Containerization**: Jenkins builds a Docker image using the `Dockerfile`.
4. **Artifact Storage**: The image is pushed to **Docker Hub** for versioning.
5. **Continuous Deployment**: Jenkins uses SSH to connect to **AWS EC2**, pulls the latest image, and restarts the application container.

---

## 🏗️ Getting Started

### 1. Local Development (Docker Compose)
Run the entire stack locally with a single command:
```bash
docker-compose up --build
```
This will start both the **Flask App** (port 5001) and **MongoDB** (port 27017).

### 2. Jenkins Integration
- Create a **Pipeline Project** in Jenkins.
- Point it to this repository.
- Configure the following credentials in Jenkins:
  - `docker-hub-creds`: Your Docker Hub username and password.
  - `ec2-ssh-creds`: SSH private key for your AWS EC2 instance.
- Update the environment variables in `Jenkinsfile` (IP, Repo URL).

### 3. AWS EC2 Setup
Ensure your EC2 instance (Ubuntu recommended) has Docker and the `scripts/deploy.sh` script permissions:
```bash
chmod +x scripts/deploy.sh
```

---

## 📂 Project Structure
```text
.
├── app.py              # Main Flask Application
├── Dockerfile          # App Container Configuration
├── docker-compose.yml  # Multi-container orchestration
├── Jenkinsfile         # CI/CD Pipeline Definition
├── scripts/
│   └── deploy.sh       # Automated Deployment Script
├── static/             # Frontend Assets (CSS/JS)
├── templates/          # HTML Templates
└── requirements.txt    # Python Dependencies
```

## 📜 License
This project is for educational purposes as part of a DevOps Portfolio.
