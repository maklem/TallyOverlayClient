# Tally Overlay Client

This is an on-screen tally light that connects to 
[TallyArbiter](https://github.com/josephdadams/TallyArbiter). It shows a red 
frame on the screen if video from that computer (or any configured device) is 
live.

## Installing (Releases)

There are no releases yet.

## Installing (Development Builds)

A self-contained Python bundle is created for every successful pipeline run.
You can try the most recent successful 
[GitHub Actions workflow run](https://github.com/maklem/TallyOverlayClient/actions/workflows/python-ci.yml).

## Development

**Prerequisites:** `python3.12` and `tox`

Run `tox` to launch CI/CD steps (unit tests, linting, static code analysis).

Run `tox r -e py312-run` to launch the program.

Run `tox r -e py312-pyinstaller` to build a Python app bundle.

Virtual environments are created by tox with all needed dependencies.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request 
with your changes. Ensure that your code adheres to the existing style and 
passes all tests.
