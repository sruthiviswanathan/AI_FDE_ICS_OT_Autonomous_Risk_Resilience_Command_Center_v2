FROM node:20-slim AS ui
WORKDIR /ui
COPY apps/command_center/package.json apps/command_center/package-lock.json ./
RUN npm ci
COPY apps/command_center/index.html apps/command_center/vite.config.js ./
COPY apps/command_center/src ./src
RUN npm run build

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY --from=ui /ui/static/app.js /ui/static/app.css ./apps/command_center/static/
ENV PYTHONPATH=/app/src
ENV AI_ENABLED=0
# No model credentials. No OT connectors. Advisory API only.
EXPOSE 8000
CMD ["uvicorn", "ot_command.api:app", "--host", "0.0.0.0", "--port", "8000"]
