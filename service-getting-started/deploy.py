import argparse

from servicefoundry import (
    Build,
    DockerFileBuild,
    Image,
    LocalSource,
    Port,
    PythonBuild,
    Service,
)

parser = argparse.ArgumentParser(description="Deploy a service to Truefoundry")
parser.add_argument("--workspace-fqn", "-w", type=str, required=True, help="FQN of the workspace to deploy to")
parser.add_argument("--host", type=str, required=True, help="Host for the service endpoint")
parser.add_argument("--path", type=str, required=False, default=None, help="Optional path for the service endpoint")
args = parser.parse_args()


python_build = PythonBuild(
    python_version="3.10", requirements_path="requirements.txt", command="uvicorn app:app --host 0.0.0.0 --port 8000"
)

dockerfile_build = DockerFileBuild()

image_build = Image(image_uri="truefoundrycloud/service-getting-started:0.0.1")

service = Service(
    name="emotion-class-svc",
    image=Build(
        build_source=LocalSource(local_build=False),
        build_spec=python_build,
    ),
    ports=[
        Port(
            port=8000,
            host=args.host,
            path=args.path,
        )
    ],
)

service.deploy(workspace_fqn=args.workspace_fqn)
