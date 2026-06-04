from fastapi import FastAPI

from acompanhamento_cardiaco.database import Base, engine
from acompanhamento_cardiaco.measurements.measurement_router import (
    router as measurements_router,
)
from acompanhamento_cardiaco.users.user_router import router as users_router
from .database import Base, engine
from .users.user_router import router as users_router
from .auth.auth_router import router as auth_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API de Acompanhamento de Saúde Cardíaca",
    version="1.0.0",
    description=( 
        "API REST para apoiar pacientes com problemas cardíacos "
        "no monitoramento da saúde."
    ),
)


app.include_router(users_router, prefix="/v1")
app.include_router(measurements_router, prefix="/v1")
app.include_router(auth_router, prefix="/v1")
