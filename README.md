# tank.ly API
Companion API for my [tank.ly demo project.](https://github.com/hayden-cole/tank.ly)

About as simple as it can get. Flask serving SQLite. Requires a Python installation to run. I used version 3.13.2. I just used the latest version of flask and its dependencies. If you run into compatibility issues, run it with uv.

To run:

    pip install flask
    python main.py

To run with **uv**:

    pip install uv
    uv sync
    uv run main.py