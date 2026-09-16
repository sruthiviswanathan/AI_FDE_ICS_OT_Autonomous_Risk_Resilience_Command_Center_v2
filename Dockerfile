FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH=/app/src
ENV AI_ENABLED=0
# No model credentials. No OT connectors. Advisory API only.
EXPOSE 8000
CMD ["uvicorn", "ot_command.api:app", "--host", "0.0.0.0", "--port", "8000"]
