import os
import subprocess
import tempfile

import yaml
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")


def apply_kustomize_patches(resource_yaml: str, patches_yaml: str) -> str:
    """
    Apply kustomize patches to the resource YAML using the kustomize binary.
    Returns the processed YAML or error message.
    """
    try:
        # Create a temporary directory for kustomize files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Write the base resource
            base_path = os.path.join(temp_dir, "base.yaml")
            with open(base_path, "w") as f:
                f.write(resource_yaml)

            # Write the kustomization.yaml
            kustomization = {"resources": ["base.yaml"]}

            # Parse the patches YAML
            patches_data = yaml.safe_load(patches_yaml) if patches_yaml else {}

            # Add patches to appropriate sections only if they exist
            if "patches" in patches_data and patches_data["patches"]:
                kustomization["patches"] = patches_data["patches"]
            if "patchesJson6902" in patches_data and patches_data["patchesJson6902"]:
                kustomization["patchesJson6902"] = patches_data["patchesJson6902"]
            if (
                "patchesStrategicMerge" in patches_data
                and patches_data["patchesStrategicMerge"]
            ):
                kustomization["patchesStrategicMerge"] = patches_data[
                    "patchesStrategicMerge"
                ]

            kustomization_path = os.path.join(temp_dir, "kustomization.yaml")
            with open(kustomization_path, "w") as f:
                yaml.dump(kustomization, f)

            # Run kustomize
            result = subprocess.run(
                ["kustomize", "build", temp_dir], capture_output=True, text=True
            )

            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error applying patches:\n{result.stderr}"

    except Exception as e:
        return f"Error: {str(e)}"


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/kustomize")
async def kustomize(resource_yaml: str = Form(...), patches_yaml: str = Form(...)):
    result = apply_kustomize_patches(resource_yaml, patches_yaml)
    return {"result": result}
