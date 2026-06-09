FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app/acompanhamento_cardiaco

RUN pip install --no-cache-dir "poetry>=2.0,<3.0"

COPY README.md /app/README.md
COPY acompanhamento_cardiaco/pyproject.toml acompanhamento_cardiaco/poetry.lock ./

RUN poetry install --only main --no-root

COPY acompanhamento_cardiaco/acompanhamento_cardiaco ./acompanhamento_cardiaco

EXPOSE 8000

CMD ["uvicorn", "acompanhamento_cardiaco.main:app", "--host", "0.0.0.0", "--port", "8000"]
