# Kustomize Playground

A web-based playground for testing and experimenting with Kustomize patches. This application provides a user-friendly interface to apply Kustomize patches to Kubernetes resources in real-time.

## Features

- Real-time YAML editing with syntax highlighting
- Support for all Kustomize patch types:
  - Strategic Merge Patches
  - JSON 6902 Patches
  - Regular patches
- Copy functionality for both input and output
- Clear output option
- Smooth scrolling and navigation
- Mobile-responsive design

## Prerequisites

- Python 3.11 or higher
- Docker (optional, for containerized deployment)

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/kustomize-playground.git
cd kustomize-playground
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies using UV:
```bash
uv pip install -e .
```

4. Run the development server:
```bash
uvicorn main:app --reload
```

5. Open your browser and navigate to `http://localhost:8000`

## Docker Deployment

1. Build the Docker image:
```bash
docker build -t kustomize-playground .
```

2. Run the container:
```bash
docker run -p 8000:8000 kustomize-playground
```

3. Open your browser and navigate to `http://localhost:8000`

## Usage

1. Enter your Kubernetes resource YAML in the left editor
2. Enter your Kustomize patches in the right editor
3. Click "Apply Patches" to see the result
4. Use the copy buttons to copy the content of any editor
5. Use the clear button to reset the output

## Example

### Resource YAML
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 1
  template:
    spec:
      containers:
        - name: nginx
          image: nginx:1.14.2
```

### Patches YAML
```yaml
patches:
  - patch: |-
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: nginx
      spec:
        replicas: 3
        template:
          spec:
            containers:
              - name: nginx
                image: nginx:latest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

Made using Cursor Agent (with a bunch of back and forth sillyness) - as the kids call it Vibe Coding ✨
