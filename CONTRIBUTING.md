# Contributing to Used Cars Price Prediction

Thank you for your interest in contributing to this project! Contributions of all kinds are welcome, including bug reports, feature suggestions, documentation improvements, tests, and code changes.

Please read this guide before submitting a contribution.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [How to Contribute](#how-to-contribute)
- [Coding Guidelines](#coding-guidelines)
- [Testing](#testing)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Reporting Bugs and Suggesting Features](#reporting-bugs-and-suggesting-features)

## Getting Started

1. Make sure you have Git and Python installed.
2. Fork this repository on GitHub.
3. Clone your fork:

   ```bash
   git clone https://github.com/<your-username>/used-cars-price-prediction.git
   cd used-cars-price-prediction
   ```

4. Add the original repository as the upstream remote:

   ```bash
   git remote add upstream https://github.com/AvinabhDutta-Dev/used-cars-price-prediction.git
   ```

## Development Setup

Create and activate a virtual environment.

**Windows (PowerShell):**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```cmd
py -m venv .venv
.venv\Scripts\activate.bat
```

**Linux and macOS (Bash/Zsh):**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

To run the application locally, start the Flask backend from the project root:

```bash
python server/server.py
```

Then open `client/UCPPM.html` in your web browser. Keep the Flask server running while using the frontend.

## Project Structure

The main project directories are:

- `client/` — frontend files (HTML, CSS, JavaScript, and assets).
- `data/` — raw and cleaned datasets.
- `docs/images/` — screenshots and README images.
- `model/` — model training notebook and saved model.
- `server/` — Flask API.
- `tests/` — automated tests for the API.

Please place new files in the appropriate directory and avoid committing generated files or local environment folders.

## How to Contribute

1. Make sure your fork is up to date with the original repository.
2. Create a descriptive branch for your work:

   ```bash
   git checkout main
   git pull upstream main
   git checkout -b feature/short-description
   ```

   For bug fixes, a branch name such as `fix/short-description` is also suitable.

3. Make your changes in focused, logical commits.
4. Run the relevant tests and review your changes.
5. Push your branch to your fork:

   ```bash
   git push origin feature/short-description
   ```

6. Open a pull request against the original repository's `main` branch.

Replace `feature/short-description` with the branch name you created.

## Coding Guidelines

- Follow the existing code style and keep changes clear and readable.
- Use descriptive names for variables, functions, and files.
- Keep functions focused and avoid unnecessary duplication.
- Add or update tests when changing application behaviour.
- Update the README or other documentation when your changes affect setup, usage, or project functionality.
- Do not commit virtual environments, caches, local configuration, or unrelated generated files.
- Do not change the saved model or datasets unless the contribution specifically requires it; explain any such changes in the pull request.

## Testing

Run the test suite from the project root:

```bash
python -m unittest discover -s tests -v
```

Please make sure the tests pass before opening a pull request. The repository's GitHub Actions workflow also runs the unit tests for pushes to its configured branches and pull requests targeting `main`.

If you add or modify tests, keep them focused and include coverage for relevant success and error cases.

## Pull Request Guidelines

Before submitting a pull request:

- Check that your branch contains only changes related to the contribution.
- Run the test suite and confirm it passes.
- Provide a clear title and explain what changed and why.
- Link any related issue, if applicable.
- Include screenshots for relevant frontend or visual changes.
- Mention any known limitations, compatibility considerations, or changes to datasets and model files.

Keep pull requests focused and reasonably small where possible. Be prepared to discuss feedback and make follow-up changes.

## Reporting Bugs and Suggesting Features

Please use the repository's [GitHub Issues](https://github.com/AvinabhDutta-Dev/used-cars-price-prediction/issues) page to report bugs or suggest features.

When reporting a bug, include:

- A clear description of the problem.
- Steps to reproduce it.
- What you expected to happen and what actually happened.
- Relevant error messages, logs, or screenshots.
- Your operating system and Python version, where relevant.

Before opening a new issue, check whether a similar issue already exists.

---

Thank you for helping improve Used Cars Price Prediction!
