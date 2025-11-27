# main.py

from fastapi import FastAPI
from routers import funcionarios

app = FastAPI(
    title="Aduana Digital Backend",
    description="Backend de Aduana Digital para distribución de flujo esperado por hora",
    version="1.0.0"
)

# Registrar los routers
app.include_router(funcionarios.router, prefix="/funcionarios", tags=["funcionarios"])

@app.get("/")
def root():
    return {"message": "Backend Aduana Digital funcionando correctamente"}
