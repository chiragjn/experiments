## Setup

- EKS
- A10 GPUs
- NFS Volume created before hand

    ```yaml
    name: distributed-training-shared
    type: volume
    config:
    size: 200
    type: dynamic
    storage_class: efs-sc
    volume_browser:
    endpoint:
        host: >-
        distributed-training-shared-chirag-gpu-dev.tfy-usea1-ctl.devtest.truefoundry.tech
    username: admin
    password_secret_fqn: tfy-secret://truefoundry:chirag-personal:VOLUME_BROWSER_PASSWORD
    ```

- Image is public but docker.io image pull secret already applied `chirag-dockerio-public-ro` to avoid pull rate limits
- Installed Volcano

    ```yaml
    name: volcano
    type: helm
    source:
    path: installer/helm/chart/volcano
    type: git-helm-repo
    repo_url: https://github.com/volcano-sh/volcano.git
    revision: 711b3849e7022297f40602656407cf4986925f26
    values:
    basic:
        image_registry: tfy.jfrog.io/tfy-mirror
    ```

- Installed Kubeflow Training Operator

    ```bash
    kubectl apply --server-side -k "github.com/kubeflow/training-operator.git/manifests/overlays/standalone?ref=v1.8.1"
    ```

Patched args to use Volcano as the scheduler (and only react to specific CRDs)

    ```yaml
    command:
    - /manager
    args:
    - --gang-scheduler-name=volcano
    - --enable-scheme=tfjob
    - --enable-scheme=pytorchjob
    - --enable-scheme=xgboostjob
    - --enable-scheme=paddlejob
    ```

- Installed MPI Operator

> Note: You need to delete MPI v1 CRD installed by Kubeflow Training Operator

    ```bash
    kubectl apply --server-side -k "github.com/kubeflow/mpi-operator.git/manifests/overlays/standalone?ref=v0.6.0"
    ```

Patched args to use Volcano as the scheduler

    ```yaml
    args:
    - '--gang-scheduling=volcano'
    - '-alsologtostderr'
    - '--lock-namespace=mpi-operator'
    ```

## Experiments

### HF Transformers TRL via torchrun DDP

```bash
kubectl apply -f kfto-torchrun-trl.yaml
```



## Notes

Following environment variables are set by training operator
These are then used by Torch Elastic aka torchrun

```
MASTER_ADDR : pytorch-distributed-training-master-0
MASTER_PORT : 23456
PET_MASTER_ADDR : pytorch-distributed-training-master-0
PET_MASTER_PORT : 23456
PET_NNODES : 2
PET_NODE_RANK : 0
PET_NPROC_PER_NODE : auto
PYTHONUNBUFFERED : 1
RANK : 0
WORLD_SIZE : 2
```