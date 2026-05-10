# Kubernetes HTTP Methods + Volume Mount Demo

## Objective

This project demonstrates:

- HTTP Methods (`GET`, `POST`, `PUT`, `DELETE`)
- NGINX Reverse Proxy
- Kubernetes Services
- Kubernetes Volume Types
- Persistent Storage
- CSI Storage

The purpose is to understand how Kubernetes applications interact with storage while processing API requests.

---

# Architecture

```text
Client (curl/browser)
        |
        v
NGINX Reverse Proxy
        |
        v
Flask API Service
        |
        v
Volume Mount (/data)
        |
------------------------------------------------
|            |             |                  |
emptyDir   hostPath       NFS               CSI
```

---

# Namespace

All resources are deployed in:

```text
akash-kt
```

Create namespace:

```bash
kubectl create namespace akash-kt
```

Verify:

```bash
kubectl get ns
```

---

# Components Used

| Component | Purpose |
|------------|----------|
| Flask API | HTTP Methods |
| NGINX | Reverse Proxy |
| Service | Internal Communication |
| Volume Mount | Data Persistence |
| PVC | CSI Storage |
| ConfigMap | NGINX Configuration |

---

# Project Structure

```text
k8-http-demo/
│
├── app.py
├── Dockerfile
├── requirements.txt
│
├── api-service.yaml
├── nginx-config.yaml
├── nginx-deployment.yaml
├── nginx-service.yaml
│
├── api-emptydir.yaml
├── api-hostpath.yaml
├── api-nfs.yaml
├── api-csi.yaml
│
└── pvc.yaml
```

---

# HTTP Methods Demonstrated

## GET

Fetch data.

Example:

```bash
curl http://NODE-IP:30080/api/items
```

Expected output:

```json
{
  "data": []
}
```

---

## POST

Add new data.

Example:

```bash
curl -X POST http://NODE-IP:30080/api/items \
-H "Content-Type: application/json" \
-d '{"name":"apple"}'
```

Expected output:

```json
{
  "message": "added"
}
```

---

## PUT

Update existing data.

Example:

```bash
curl -X PUT http://NODE-IP:30080/api/items/0 \
-H "Content-Type: application/json" \
-d '{"name":"orange"}'
```

Expected output:

```json
{
  "message": "updated"
}
```

---

## DELETE

Delete data.

Example:

```bash
curl -X DELETE http://NODE-IP:30080/api/items/0
```

Expected output:

```json
{
  "message": "deleted"
}
```

---

# Docker Build

Build image:

```bash
docker build -t flask-http-demo:v1 .
```

Verify image:

```bash
docker images
```

---

# Deployment

Deploy common components:

```bash
kubectl apply -f nginx-config.yaml -n akash-kt
kubectl apply -f nginx-deployment.yaml -n akash-kt
kubectl apply -f nginx-service.yaml -n akash-kt
kubectl apply -f api-service.yaml -n akash-kt
```

---

# Volume Types

---

## 1. emptyDir

### Description

Temporary storage created with Pod.

### Characteristics

- Survives container restart
- Lost when Pod is deleted
- Not persistent

### Deploy

```bash
kubectl apply -f api-emptydir.yaml -n akash-kt
```

### Test

Add data:

```bash
curl -X POST http://NODE-IP:30080/api/items \
-H "Content-Type: application/json" \
-d '{"name":"apple"}'
```

Delete pod:

```bash
kubectl delete pod -l app=flask-api -n akash-kt
```

Verify:

```bash
curl http://NODE-IP:30080/api/items
```

Result:

Data is lost.

---

## 2. hostPath

### Description

Mounts local filesystem from worker node.

### Characteristics

- Persistent
- Node dependent
- Not suitable for production multi-node cluster

### Deploy

```bash
kubectl apply -f api-hostpath.yaml -n akash-kt
```

### Verify Storage

SSH into worker node:

```bash
ls -l /opt/k8-storage
```

Expected:

```text
items.json
```

---

## 3. NFS

### Description

Network shared storage.

### Characteristics

- Shared across nodes
- Supports ReadWriteMany (RWX)
- Persistent

### Deploy

Update NFS server details:

```yaml
server: 192.168.1.50
path: /export/k8
```

Apply:

```bash
kubectl apply -f api-nfs.yaml -n akash-kt
```

Verify on NFS server:

```bash
ls -l /export/k8
```

---

## 4. CSI Storage

### Description

Modern Kubernetes storage provisioning.

Uses:

```text
StorageClass
      |
PVC
      |
PV
```

### Deploy PVC

```bash
kubectl apply -f pvc.yaml -n akash-kt
```

### Deploy API

```bash
kubectl apply -f api-csi.yaml -n akash-kt
```

Verify PVC:

```bash
kubectl get pvc -n akash-kt
```

---

# Verify Pods

```bash
kubectl get pods -n akash-kt
```

---

# Verify Services

```bash
kubectl get svc -n akash-kt
```

---

# Get Node IP

```bash
kubectl get nodes -o wide
```

Access API:

```text
http://NODE-IP:30080/api/items
```

---

# Persistence Testing

After POST request:

Delete pod:

```bash
kubectl delete pod -l app=flask-api -n akash-kt
```

Check again:

```bash
curl http://NODE-IP:30080/api/items
```

### Expected Result

| Volume Type | Persistence |
|-------------|-------------|
| emptyDir | No |
| hostPath | Yes |
| NFS | Yes |
| CSI | Yes |

---

# Cleanup

Delete namespace:

```bash
kubectl delete namespace akash-kt
```

This removes all demo resources.