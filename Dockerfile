FROM python:3.9-slim-buster AS builder

WORKDIR /app

RUN pip install uv

COPY pyproject.toml ./

RUN uv pip install --system --no-cache -r pyproject.toml


FROM python:3.9-slim-buster AS final

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

RUN pip install gunicorn

EXPOSE 8000
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:8000", "app.main:app"]


