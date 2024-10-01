TrueFoundry DockerBuild example for private pypi
---

1. In your Dockerfile setup an arg and use it in `--extra-index-url`


```Dockerfile
ARG JFROG_PYPI_EXTRA_INDEX_URL
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --extra-index-url "$JFROG_PYPI_EXTRA_INDEX_URL"
```

2. Create a secret on the platform with private pypi index url

For example it might look like this

```
https://[USERNAME-REDACTED]:[PASSWORD-REDACTED]@myorg.jfrog.io/artifactory/api/pypi/private-pypi-example/simple
```

**Make sure to url encode username and password!**

![image](https://github.com/user-attachments/assets/b8075eb5-c974-438f-ae6f-6518f99a01d7)


3. Finally when deploying link the secret in `build_spec` in `truefoundry.yaml` or your python deploy script by specifying the secret fqn against the arg name in step 1


```yaml
image:
  type: build
  build_source: 
    ...
  build_spec:
    type: dockerfile
    build_args:
      JFROG_PYPI_EXTRA_INDEX_URL: tfy-secret://myorg:jfrog-pypi:JFROG_PYPI_EXTRA_INDEX_URL
    command: ...
...
```
