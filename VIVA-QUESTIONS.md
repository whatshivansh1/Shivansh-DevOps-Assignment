# DevOps Lab — Viva Questions and Answers

This document contains viva questions and concise answers for the
DevOps lab exercises. Questions are organized by exercise for quick
revision.

---

# Exercise 1 — Kubernetes Getting Started

### 1. What is Kubernetes?

Kubernetes is a container orchestration platform used to deploy,
manage, scale, and maintain containerized applications.

### 2. What is a Pod?

A Pod is the smallest deployable unit in Kubernetes. It contains one
or more containers that share networking and storage resources.

### 3. What is Minikube?

Minikube runs a local Kubernetes cluster, making it useful for learning,
development, and testing Kubernetes applications.

### 4. What is kubectl?

`kubectl` is the command-line tool used to communicate with a Kubernetes
cluster and manage resources such as Pods, Services, and Deployments.

### 5. What is a Kubernetes Service?

A Service provides a stable network endpoint for accessing a group of
Pods selected by labels.

### 6. What is a NodePort Service?

A NodePort Service exposes an application on a port of each cluster node,
allowing access from outside the cluster when networking permits it.

---

# Exercise 2 — Flask App on Minikube

### 1. What is a Docker image?

A Docker image is a packaged, read-only template containing an
application and the dependencies required to run it.

### 2. What is a Docker container?

A container is a running instance of an image.

### 3. What is a Kubernetes Deployment?

A Deployment manages application replicas and supports declarative
updates and replacement of Pods.

### 4. Why was the image loaded into Minikube?

The image was loaded so the Minikube cluster could use the locally
built image without needing to pull it from a remote registry.

### 5. What is the purpose of imagePullPolicy: Never?

It tells Kubernetes not to pull the image from a registry. The image
must already be available to the node's container runtime.

### 6. What is the difference between port and targetPort in a Service?

`port` is the port exposed by the Service. `targetPort` is the port
on the destination container to which traffic is forwarded.

### 7. How was the Flask application verified?

The application was accessed through its Service and tested using
`curl`. An HTTP 200 response confirmed a successful request.

---

# Exercise 3 — Scaling Flask with ReplicaSets

### 1. What is a ReplicaSet?

A ReplicaSet ensures that a specified number of matching Pod replicas
are running at any given time.

### 2. How did you scale the application from three to five replicas?

The command used was:

`kubectl scale rs flashsale-rs --replicas=5`

### 3. What happens when a managed Pod is deleted?

The ReplicaSet detects that the number of available matching Pods is
below the desired count and creates a replacement Pod.

### 4. What is self-healing in Kubernetes?

Self-healing is Kubernetes' ability to maintain the desired state by
restarting failed containers or replacing unhealthy or deleted Pods,
depending on the resource and failure.

### 5. What does kubectl get pods -o wide show?

It displays Pod details including status, IP address, and the node
on which each Pod is scheduled.

### 6. Why was a Service used with the ReplicaSet?

The Service provides a stable endpoint for reaching application Pods
even when individual Pod instances are replaced.

### 7. Why did all five Pods run on the same node?

The exercise used a single-node Minikube cluster, so all scheduled
Pods ran on the Minikube node.

---

# Exercise 4 — Docker Networking

### 1. What is the purpose of the --network flag in docker run?

It connects a container to the specified Docker network.

### 2. How do containers communicate on the same user-defined bridge network?

They can communicate using container names or IP addresses. Docker's
embedded DNS resolves container names on user-defined bridge networks.

### 3. What is a bridge network?

A bridge network provides an isolated virtual network through which
connected containers can communicate.

### 4. What is the difference between bridge and host networking?

Bridge networking gives containers their own network interfaces within
a virtual network. Host networking shares the host's network stack and
reduces network isolation.

### 5. How do you expose a container port to the host?

Use the `-p` option, such as `-p 5001:5001`, to map host port 5001
to container port 5001.

### 6. How did you verify Docker container name resolution?

The Flask container used Python's socket library to resolve the names
`mysql` and `redis` to their container IP addresses.

### 7. What was the purpose of the custom bridge network?

It connected the Flask, MySQL, and Redis containers to the same
user-defined network so they could discover and communicate with
each other by container name.

---

# Exercises 5–10

Viva questions for these exercises will be added after reviewing the
corresponding lab instructions and completing the practical work.


## Exercise 5: Docker Security with AppArmor

**1. What is AppArmor?**
AppArmor is a Linux security module that restricts application capabilities through security profiles.

**2. Why use AppArmor with Docker?**
It can limit a container application’s access to files, capabilities, and system resources.

**3. What is the purpose of a Dockerfile?**
A Dockerfile contains instructions for building a Docker image.

**4. What is the Docker SDK for Python?**
It lets Python programs communicate with the Docker Engine API to build images, run containers, and inspect container configuration.

**5. Does accepting an AppArmor option prove enforcement?**
No. The profile must be verified as loaded and enforced, and the intended restrictions must be tested.

**6. What happened during the restricted-action tests?**
Both `cat /etc/passwd` and `/bin/bash --version` returned exit code 0, meaning the operations were allowed.

**7. What limitation was observed in this exercise?**
The exercise ran on macOS using Docker Desktop. The requested AppArmor option was accepted, but enforcement of the custom profile was not verified.


## Exercise 6: Real-Time Operations Monitoring and Alerting

**Q1. What is Prometheus?**
Prometheus is a monitoring and time-series database system that collects metrics from configured targets.

**Q2. What is Grafana used for in this project?**
Grafana visualizes delivery metrics in a dashboard using Prometheus as its data source.

**Q3. What does the Python `prometheus_client` library do?**
It exposes application metrics through an HTTP endpoint that Prometheus can scrape.

**Q4. What is a Gauge metric?**
A Gauge represents a value that can increase or decrease, such as pending deliveries.

**Q5. What is a Summary metric?**
A Summary observes values such as delivery durations and exposes observation count and sum, which can be used to calculate an average.

**Q6. What is a Prometheus scrape target?**
A scrape target is an endpoint from which Prometheus periodically collects metrics.

**Q7. What is the purpose of `for: 15s` in an alert rule?**
It requires the alert expression to remain true for 15 seconds before the alert fires.

**Q8. Why use Docker Compose?**
It defines and runs the related application and monitoring services together.

**Q9. Why is `host.docker.internal` not needed for the metrics target here?**
The metrics application and Prometheus share a Docker Compose network, so Prometheus can reach the application by its service name.

**Q10. What is the purpose of the Jenkinsfile?**
It defines automated pipeline stages to validate the project, build the image, deploy the stack, and verify the metrics endpoint.

**Q11. How can a high-pending-delivery alert be tested?**
Run the application with `SIMULATE_HIGH_PENDING=1`, wait for the alert's evaluation period, and inspect Prometheus Alerts.

**Q12. Do randomized metrics represent actual delivery-company data?**
No. They are simulated sample data used to demonstrate monitoring and alerting.
