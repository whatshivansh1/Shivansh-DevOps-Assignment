import docker
from docker.errors import APIError

client = docker.from_env()
container = None

try:
    print("Building image from Dockerfile...")
    client.images.build(path=".", tag="flask-apparmor")

    print("\nChecking whether the Docker daemon supports this AppArmor profile...")
    container = client.containers.run(
        "flask-apparmor",
        ports={"5000/tcp": 5000},
        security_opt=["apparmor=my-apparmor-profile"],
        detach=True,
    )

    info = client.api.inspect_container(container.id)
    security_options = info["HostConfig"].get("SecurityOpt") or []

    print(f"Container started: {container.short_id}")
    print(f"Configured security options: {security_options}")
    print("Note: configured options alone do not prove the profile is enforced.")

except APIError as exc:
    print("The Docker daemon rejected the AppArmor configuration.")
    print(f"Details: {exc}")
    print("This environment may not support loading custom AppArmor profiles.")

finally:
    if container is not None:
        try:
            container.remove(force=True)
            print("Test container removed.")
        except APIError as exc:
            print(f"Could not remove test container: {exc}")

    client.close()
