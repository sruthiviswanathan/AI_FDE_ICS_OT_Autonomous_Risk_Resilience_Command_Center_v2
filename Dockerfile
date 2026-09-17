# Stage 1: build React frontend (integrated — no VITE_API_URL)
FROM node:20-alpine AS frontend
WORKDIR /fe
COPY apps/command_center/package.json apps/command_center/package-lock.json ./
RUN npm ci
COPY apps/command_center/ ./
RUN npm run build

# Stage 2: Python API + static UI + estate data
FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY data/ ./data/
COPY contracts/ ./contracts/
COPY apps/command_center/scenario_bindings.json ./apps/command_center/scenario_bindings.json
COPY scenarios/ ./scenarios/
COPY --from=frontend /fe/dist/ ./apps/command_center/dist/

ENV PYTHONPATH=/app/src
ENV OT_DATA_ROOT=/app

EXPOSE 8000
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')" || exit 1
CMD ["uvicorn", "ot_command.api:app", "--host", "0.0.0.0", "--port", "8000"]
