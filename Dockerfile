FROM python:3.12-slim

WORKDIR /app

ARG SERVICE_DIR

COPY requirements.txt requirements-container.txt ./
RUN pip install --no-cache-dir -r requirements-container.txt

RUN useradd --create-home --uid 10001 appuser

COPY ${SERVICE_DIR}/ /app/
RUN chown -R appuser:appuser /app

USER 10001

ENV PYTHONUNBUFFERED=1
ENV PORT=5000

EXPOSE 5000

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} --workers 1 app:app"]