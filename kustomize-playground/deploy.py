import argparse
import logging

from truefoundry.deploy import (
    Build,
    DockerFileBuild,
    HealthProbe,
    HttpProbe,
    LocalSource,
    Port,
    Resources,
    Service,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Deploy Kustomize Playground to TrueFoundry"
    )
    parser.add_argument(
        "--host",
        required=True,
        help="Host",
    )
    parser.add_argument(
        "--workspace-fqn",
        required=True,
        help="TrueFoundry workspace FQN",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    service = Service(
        name="kustomize-playground",
        image=Build(
            build_source=LocalSource(
                local_build=False,
            ),
            build_spec=DockerFileBuild(
                dockerfile_path="Dockerfile",
                command="uvicorn main:app --host 0.0.0.0 --port 8000",
            ),
        ),
        ports=[Port(port=8000, host=args.host)],
        resources=Resources(
            cpu_request=0.05,
            cpu_limit=0.5,
            memory_request=100,
            memory_limit=500,
        ),
        liveness_probe=HealthProbe(
            config=HttpProbe(
                path="/health",
                port=8000,
            ),
            period_seconds=10,
            timeout_seconds=5,
            success_threshold=1,
            failure_threshold=5,
        ),
        readiness_probe=HealthProbe(
            config=HttpProbe(
                path="/health",
                port=8000,
            ),
            period_seconds=10,
            timeout_seconds=5,
            success_threshold=1,
            failure_threshold=3,
        ),
        workspace_fqn=args.workspace_fqn,
    )
    service.deploy(workspace_fqn=args.workspace_fqn, wait=False)


if __name__ == "__main__":
    main()
