# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Run from this directory (`Week 3/login`). The path contains a space, so quote it.

```bash
uv sync                                  # install deps (Flask + Robot Framework dev group)
uv run rfbrowser install chromium        # one-time Playwright browser download for the Browser library

uv run python src/index.py               # start the app on http://localhost:5001 (debug mode)

# Acceptance tests — the app MUST already be running in another terminal
uv run robot src/tests                           # all suites (headed, 500ms slowMo by default)
uv run robot -v HEADLESS:true src/tests          # headless
uv run robot src/tests/login.robot               # one suite
uv run robot -t "Login With Correct Credentials" src/tests   # one test case
```

Robot writes `output.xml`, `log.html`, `report.html` and `playwright-log.txt` into the current directory; these are gitignored.

## Architecture

Flask app with a layered structure. Modules import each other by bare name (`from services.user_service import user_service`), so `src/` is the import root — run things from paths that keep it that way (`src/index.py` does).

- `app.py` — all routes. POST handlers call the service and turn any raised exception into a `flash()` message plus a redirect back to the form. The Robot tests check for these messages in the page body, so the exception text is effectively part of the tested UI.
- `services/user_service.py` — validation and auth (`UserInputError`, `AuthenticationError`). Takes the repository by constructor injection, defaulting to the module-level singleton.
- `repositories/user_repository.py` — in-memory list of users (no database; state is lost on restart). Duplicate-username check lives here, not in the service.
- `entities/user.py` — plain `User(username, password)`; passwords are stored and compared in plaintext. `User` has no `id`, so `UserRepository.delete(user_id)` would fail if called.
- Both the repository and the service are module-level singletons (`user_repository`, `user_service`) shared by the app.

Test-support endpoints in `app.py`: `GET /ping` (liveness) and `POST /tests/reset` (clears the repository).

## Robot Framework tests

- `src/tests/resource.robot` — shared settings, variables (`SERVER`, `DELAY`, `BROWSER`, `HEADLESS`) and page-level keywords (`Go To …`, `… Page Should Be Open` checks by page `<title>`, `Set Username`/`Set Password`). New suites should import it with `Resource  resource.robot`.
- `src/AppLibrary.py` — Python keyword library that talks to the running app over HTTP: `Reset Application` (→ `/tests/reset`) and `Create User` (→ `POST /register`). Each suite's `Test Setup` calls `Reset Application` so tests are isolated; seed data goes through `Create User` rather than the UI.
- Each suite opens one browser in `Suite Setup` and closes it in `Suite Teardown`; suite-specific keywords sit in that suite's `*** Keywords ***` section.
- Passwords are typed with `Fill Secret  id=…  $password` — the `$var` form (no braces) is deliberate so the Browser library keeps the value out of the logs.
- Page titles asserted by tests come from the templates in `src/templates/` (all extend `layout.html`); changing a `<title>` there breaks the matching `… Page Should Be Open` keyword.
