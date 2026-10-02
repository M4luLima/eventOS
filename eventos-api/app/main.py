from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database import Base, engine
from app.routers import auth, usuarios, eventos, atividades, inscricoes, ingressos

# Cria tabelas caso SQLite local
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API RESTful para Gerenciamento de Eventos e Festivais - EventOS",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(usuarios.router, prefix=settings.API_V1_STR)
app.include_router(eventos.router, prefix=settings.API_V1_STR)
app.include_router(atividades.router, prefix=settings.API_V1_STR)
app.include_router(inscricoes.router, prefix=settings.API_V1_STR)
app.include_router(ingressos.router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Health Check"])
def root():
    return {
        "status": "online",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs"
    }
