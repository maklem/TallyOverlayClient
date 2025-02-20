# Tally Overlay Client

This is an on screen tally light that connects to [TallyArbiter](https://github.com/josephdadams/TallyArbiter).
It show a red frame on screen, if video from that computer (or any configured device) is live.

## Installing (Releases)

There are no releases yet.

## Installing (Development Builds)

A self-contained python bundle is created for every successful pipeline run.
You can try the most recent successful [Github Actions workflow run](https://github.com/maklem/TallyOverlayClient/actions/workflows/python-ci.yml).

## Development

Prequisites: `python3.12` and `tox`

Run `tox` to launch CI/CD steps (unittests, linting, static code analysis)

Run `tox r -e py312-run` to launch the program.

Virtual environments are created by tox with all needed dependencies.
