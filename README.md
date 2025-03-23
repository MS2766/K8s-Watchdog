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

### ✅ Simulate Realistic Data -
  Purpose: Generate data with normal operations and anomalies (pod failures, resource exhaustion, network issues) to reflect real-world Kubernetes behavior.
Instructions
Setup: Use PowerShell and kubectl to deploy workloads.
Realism: Multi-pod app for normal load, varied anomalies for production-like issues.
1. **Normal Operation** - normal_load.yaml
2. **Pod Failure** - crash_pod.yaml
3. **Recource Exhaustion** - resource_exhaustion.yaml
4. **Network Failure** - deny_network.yaml
Apply and delete the pods 2,3 and 4 to simulate anomalies in the pod operations

### ✅ Collect Metrics with Prometheus -
1. **Access Prometheus:**
   ```bash
   kubectl port-forward -n monitoring svc/prometheus-server 9090:80
   ```
2. **Export Data with Python:**
   ```bash
   pip install requests pandas
   ```
   Use scrape_metrics.py
   -Run :
   ```bash
   python export_metrics.py
   ```

### ✅ Train the model -
Train the Random Forest model using the generated data and create a model:
```bash
python src/model_train_and_accuracy.py
```

## Tech Stack
- **Frontend:** React, React Router, CSS
- **Backend:** FastAPI, PyTorch, Pillow, torchvision
- **Database:** PostgreSQL (if applicable)
- **Deployment:** Docker, Kubernetes, GitHub Actions

## Usage
Just feed the dataset to the model and adjust the parameters based on use case
