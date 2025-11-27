# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import funcionarios

app = FastAPI(
    title="Aduana Digital Backend",
    description="Backend de Aduana Digital para distribución de flujo esperado por hora",
    version="1.0.0"
)

# ======================================
#  CORS: PERMITIR PETICIONES DESDE VERCE
# ======================================

origins = [
    "https://funcionarios-seven.vercel.app",   # tu dashboard de funcionarios
    "https://aduana-digital.vercel.app",        # si tienes el frontend viajeros en vercel
    "*",                                        # OPCIONAL: permitir todo (útil en prototipo)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # sitios permitidos
    allow_credentials=True,
    allow_methods=["*"],        # permitir GET, POST, PUT, etc
    allow_headers=["*"],        # permitir cualquier header
)

# ============================
# Registrar routers
# ============================

app.include_router(funcionarios.router, prefix="/funcionarios", tags=["funcionarios"])

@app.get("/")
def root():
    return {"message": "Backend Aduana Digital funcionando correctamente"}
