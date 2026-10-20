import docker
from docker.errors import APIError

client = docker.from_env()
container = None

tests = [
    ("Read /etc/passwd", ["cat", "/etc/passwd"]),
    ("Execute Bash", ["/bin/bash", "--version"]),
]

try:
    print("Building image if needed...")
    client.images.build(path=".", tag="flask-apparmor")

    print("\nStarting container with requested AppArmor profile...")
    container = client.containers.run(
        "flask-apparmor",
        command=["python", "-c", "import time; time.sleep(60)"],
        security_opt=["apparmor=my-apparmor-profile"],
        detach=True,
    )

    info = client.api.inspect_container(container.id)
    options = info["HostConfig"].get("SecurityOpt") or []
    print(f"Configured security options: {options}")

    for label, command in tests:
        result = container.exec_run(command)
        output = result.output.decode(errors="replace").strip()
        denied = result.exit_code != 0 and (
            "permission denied" in output.lower()
            or "operation not permitted" in output.lower()
        )

        print(f"\nTest: {label}")
        print(f"Command: {' '.join(command)}")
        print(f"Exit code: {result.exit_code}")
        print(f"Output: {output[:400]}")
        print("PASS: operation was denied" if denied else
              "FAIL: expected permission denial was not demonstrated")

except APIError as exc:
    print(f"Docker API error: {exc}")

finally:
    if container is not None:
        try:
            container.remove(force=True)
            print("\nTest container removed.")
        except APIError as exc:
            print(f"Container cleanup error: {exc}")
    client.close()
