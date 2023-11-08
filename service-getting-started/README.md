FastAPI Emotion Classification
---

This example wraps an Emotion Classification model from Huggingface Hub in a FastAPI app

## Run Locally

1. Install requirements

```shell
python -m pip install -r requirements.txt
```

2. Run with uvicorn

```shell
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Deploy with Truefoundry

1. Install servicefoundry

```shell
python -m pip install -U servicefoundry
```

2. Login

```shell
sfy login --host <Truefoundry Platform URL>
```

3. Deploy to a workspace

```
python deploy --workspace-fqn <Your Workspace FQN>
```
