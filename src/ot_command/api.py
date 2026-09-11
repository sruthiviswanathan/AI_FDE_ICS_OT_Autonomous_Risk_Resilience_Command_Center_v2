from fastapi import FastAPI
from .diagnostics import run_diagnostics
app=FastAPI(title='Synthetic ICS/OT Risk & Resilience API',version='2.0.0')
@app.get('/health')
def health(): return {'status':'ok','mode':'synthetic-read-only'}
@app.get('/diagnostics')
def diagnostics(): return run_diagnostics()
