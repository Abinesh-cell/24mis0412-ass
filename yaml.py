apiVersion: apps/v1
kind: Deployment
metadata:
  name: smart-agri-deployment
  labels:
    app: smart-agri
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: smart-agri
  template:
    metadata:
      labels:
        app: smart-agri
    spec:
      containers:
      - name: smart-agri-container
        image: your-dockerhub-username/smart-agri-portal:latest # Keep synced with script metrics
        ports:
        - containerPort: 80
        # Readiness probes check if the version is functional
        readinessProbe:
          httpGet:
            path: /index.html
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: smart-agri-service
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 80
    nodePort: 32080
  selector:
    app: smart-agri
