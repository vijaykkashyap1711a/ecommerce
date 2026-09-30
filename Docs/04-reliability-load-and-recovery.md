# Reliability, Load, and Recovery

## Health checks

Product and Order expose a `/health` endpoint.

Each Kubernetes Deployment configures:

- A readiness probe that starts after 5 seconds.
- A liveness probe that starts after 15 seconds.
- CPU request `100m` and CPU limit `250m`.
- Memory request `128Mi` and memory limit `256Mi`.

Readiness controls when a Pod is considered ready for traffic. Liveness lets Kubernetes restart an unhealthy container.

## Horizontal Pod Autoscaler configuration

Both Product and Order use an `autoscaling/v2` HPA:

| Service | Minimum replicas | Maximum replicas | CPU target |
| --- | ---: | ---: | ---: |
| Product | 1 | 3 | 60% average utilization |
| Order | 1 | 3 | 60% average utilization |

The scale-down stabilization window is 30 seconds to make scale-down observable during the demo.

> HPA adds or removes Pods. It does not add EKS worker nodes. The current managed node group has a maximum size of three nodes. Cluster Autoscaler or Karpenter is a future production improvement.

## HPA load-test procedure

Keep these two commands visible in separate terminals:

```bash
kubectl get hpa -n ecommerce -w
kubectl get pods -n ecommerce -w
```

Create a temporary in-cluster load generator:

```bash
kubectl create deployment load-generator \
  -n ecommerce \
  --image=busybox:1.36 \
  -- /bin/sh -c 'while true; do wget -q -O- http://product:5001/products >/dev/null; done'
```

Increase load:

```bash
kubectl scale deployment load-generator -n ecommerce --replicas=3
```

Collect a snapshot during the run:

```bash
kubectl get hpa -n ecommerce
kubectl get pods -n ecommerce
kubectl top pods -n ecommerce
```

Remove the load after the test:

```bash
kubectl delete deployment load-generator -n ecommerce
```

## Observed HPA result

The supplied test output confirms the following:

1. Multiple `load-generator` Pods ran concurrently. The captured output showed ten running load-generator Pods.
2. Product started with one running Pod.
3. Kubernetes created two additional Product Pods. They moved through `Pending`, `ContainerCreating`, and then `Running`.
4. Product reached the configured HPA maximum of **three running Pods**.
5. After the load generator was removed, the load-generator Pods terminated and two Product Pods entered `Terminating`, while one Product Pod remained running. This shows scale-down toward the minimum replica count.

Do not add a response-time, throughput, or CPU percentage claim unless it comes from a captured command or load-tool output.

## Pod self-healing test

Get the current Product Pod:

```bash
kubectl get pods -n ecommerce -l app=product
```

Delete exactly one Pod:

```bash
kubectl delete pod -n ecommerce <product-pod-name>
```

Watch recovery:

```bash
kubectl get pods -n ecommerce -l app=product -w
```

## Observed HPA result

the Deployment controller notices that the number of ready Pods is below the desired replica count and creates a replacement Pod automatically seemlessly.

