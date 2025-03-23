Here is a formatted version of your README file:

---

# K8s-Watchdog - ML model to predict failures in a K8s cluster

## Overview
K8s-Watchdog is a solution developed for the Guidewire DEVTrails University Hackathon, Phase 1. The goal is to build an AI/ML model that predicts potential issues in Kubernetes clusters, such as pod failures, resource exhaustion, and other anomalies.

## Setup Steps

### ✅ Setup Azure Kubernetes Service (AKS)
1. **Install Azure CLI**
    - Download the installer from docs.microsoft.com.
    - Run the .msi file, follow the prompts, and restart your terminal.
    - Check the installation:
      ```bash
      az --version
      ```
2. **Login to Azure**
    ```bash
    az login
    ```
    - A browser window opens; sign in with your Azure credentials.
    - After login, PowerShell shows your subscription details.
3. **Create a resource group**
    ```bash
    az group create --name HackathonRG --location eastus
    ```
    - This command creates a container for your AKS cluster.
4. **Create the AKS cluster**
    ```bash
    az aks create --resource-group HackathonRG --name HackathonAKS --node-count 2 --enable-addons monitoring --generate-ssh-keys
    ```
    - `node-count 2`: Two nodes mimic a small production cluster, allowing pod distribution and realistic resource usage.
    - `enable-addons monitoring`: Adds Azure Monitor (optional visibility), but we’ll use Prometheus for custom metrics.
    - `generate-ssh-keys`: Creates SSH keys for secure access.
    - Takes ~10-15 minutes. Output confirms the cluster is created.
5. **Connect to your cluster**
    - Install kubectl via Azure CLI:
      ```bash
      az aks install-cli
      ```
    - Get cluster credentials:
      ```bash
      az aks get-credentials --resource-group HackathonRG --name HackathonAKS
      ```
    - Verify connection:
      ```bash
      kubectl get nodes
      ```

### ✅ Install Prometheus
Deploy Prometheus to collect real-time metrics from the cluster, replicating how production clusters monitor performance.
1. **Install Helm**
    - Open Git Bash (search "Git Bash" in Start menu):
      ```bash
      curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
      chmod +x get_helm.sh  # Skip this on Windows; just run next line
      ./get_helm.sh
      ```
    - Verify:
      ```bash
      helm version
      ```
2. **Add Prometheus Repository**
    ```bash
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo update
    ```
3. **Install Prometheus**
    ```bash
    helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace --set server.persistentVolume.enabled=false
    ```
    - Verify:
      ```bash
      kubectl get pods -n monitoring
      ```

### ✅ Simulate Realistic Data
High-performance API for handling AI tasks.

### ✅ React Frontend
A responsive UI for a smooth user experience.

### ✅ Docker Support
Easily deployable with Docker & Kubernetes.

## Tech Stack
- **Frontend:** React, React Router, CSS
- **Backend:** FastAPI, PyTorch, Pillow, torchvision
- **Database:** PostgreSQL (if applicable)
- **Deployment:** Docker, Kubernetes, GitHub Actions

## Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/AI-ArtFusionLab.git
cd AI-ArtFusion-Lab
```

### 2️⃣ Backend Setup
#### Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Run FastAPI Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3️⃣ Frontend Setup
#### Install Dependencies
```bash
cd frontend
npm install
```

#### Run React App
```bash
npm start
```

## Usage
- **Art Generation:** Enter a text prompt and let the AI generate an artwork.
- **Style Transfer:** Upload a content image and a style image to create a fusion of both.
- **Save & Share:** Download and showcase your AI-generated artwork.

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/art-generation/` | Generates AI artwork from text |
| `POST` | `/style-transfer/` | Transfers artistic style to an image |

## Contributing
1. **Fork** the repository.
2. **Create a branch** (`git checkout -b feature-branch`).
3. **Commit changes** (`git commit -m "Added new feature"`).
4. **Push** (`git push origin feature-branch`).
5. **Open a pull request** on GitHub.

---

You can copy and paste this formatted README file into your repository.
