# Anime Recommender Deployment Guide

This guide covers packaging the `anime-recommender` app in Docker, deploying it to Minikube, and exposing it through Kubernetes.

## 1. Prerequisites

- A local clone of the anime recommender project.
- Docker installed and running.
- Minikube installed on your machine.
- `kubectl` installed and configured.

## 2. Build the Docker image

Run these commands from the project root:

```bash
eval $(minikube docker-env)
docker build -t anime-recommender:latest .
```

This ensures the image is built in the same Docker environment that Minikube uses.

## 3. Create Kubernetes secrets

If your application needs API credentials, create a secret first:

```bash
kubectl create secret generic anime-recommender-secrets \
  --from-literal=GROQ_API_KEY="" \
  --from-literal=HUGGINGFACE_API_KEY="" \
  --from-literal=HUGGINGFACE_API_KEY="llama-3.1-8b-instant"
```

Replace the empty values with your real keys when available.

## 4. Deploy the application

Apply the Kubernetes manifest:

```bash
kubectl apply -f anime-recommender-k8s.yaml
```

Then verify the deployment:

```bash
kubectl get pods
kubectl get deployments
kubectl get services
```

The manifest starts one Deployment and one LoadBalancer Service for the app.

## 5. Access the service

For Minikube, run a tunnel in one terminal:

```bash
minikube tunnel
```

Then forward the service port locally:

```bash
kubectl port-forward svc/anime-recommender-service 8501:80 --address 0.0.0.0
```

Open your browser to:

```text
http://localhost:8501
```

You can also inspect the service directly:

```bash
kubectl get svc anime-recommender-service
```

## 6. Cleanup

Remove the deployment and secrets when you are finished:

```bash
kubectl delete -f anime-recommender-k8s.yaml
kubectl delete secret anime-recommender-secrets
minikube stop
```

## Notes

- The manifest file is named `llmops-k8s.yaml`, but it deploys resources using the `anime-recommender` naming convention.
- The container exposes port `8501` internally and routes it through service port `80`.
- Adjust the secret values and service exposure if you later deploy to a non-Minikube Kubernetes cluster.
