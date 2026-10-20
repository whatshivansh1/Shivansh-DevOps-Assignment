# Exercise 5: Docker Security with AppArmor

## Objective

Build a Flask application in Docker, configure an AppArmor security profile, and test selected container operations.

## Files

- `app.py` — Flask application.
- `requirements.txt` — Python dependencies.
- `Dockerfile` — builds the application image.
- `my-apparmor-profile` — custom AppArmor profile.
- `apply_apparmor.py` — tests the requested AppArmor option.
- `test_restricted_actions.py` — tests file reading and shell execution.

## Build the Image

Command: `docker build -t flask-apparmor .`

## Run the Application

Start the container with `docker run -d --name flask-apparmor-test -p 5000:5000 flask-apparmor`.

Test the endpoints using `curl -i http://127.0.0.1:5000/` and `curl -i http://127.0.0.1:5000/health`.

The root endpoint returned HTTP 200 and the expected message:

> Hello, this is a secure Flask application running inside a Docker container!

## Security Tests

Run `python3 test_restricted_actions.py` and `python3 apply_apparmor.py` to perform the security tests.

The restricted-action tests returned exit code `0` for both `cat /etc/passwd` and `/bin/bash --version`. Both operations were allowed.

The AppArmor script successfully started a test container with the requested option `apparmor=my-apparmor-profile`. The test container was subsequently removed.

## Platform Limitation

Accepting the AppArmor option does not prove that the custom profile was loaded or enforced. The restricted-action tests did not demonstrate that the intended restrictions were active. AppArmor enforcement therefore remains unverified in this macOS Docker Desktop environment.

## Conclusion

The Flask image built successfully, and the application returned the expected response. The Docker SDK scripts ran, and a test container accepted the requested AppArmor option. However, enforcement of the intended security restrictions was not demonstrated. Further verification requires a Linux environment with AppArmor enabled.
