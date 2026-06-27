from fastapi import FastAPI
from second_house import second_house_router
from third_house import third_house_router

app = FastAPI(
    title='Krishnalaya Vedic Astrology API',
    version='1.1.0',
    description='Production-grade Vedic astrology analysis engine — api.krishnalaya.cloud',
)

app.include_router(second_house_router)
app.include_router(third_house_router)
