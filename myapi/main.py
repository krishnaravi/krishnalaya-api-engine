from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from second_house import second_house_router
from third_house import third_house_router
from routes.houses import router as houses_router
from routes.varga import router as varga_router
from routes.ashtakavarga import router as av_router

app = FastAPI(
    title='Krishnalaya Vedic Astrology API',
    version='2.0.0',
    description=(
        'Production-grade Vedic astrology engine — api.krishnalaya.cloud\n\n'
        '**Houses**: POST /api/v1/houses/{1-12}\n'
        '**Varga Charts**: POST /api/v1/varga/{d1|d2|d3|d9|d10|d12|d16|d24|d60}\n'
        '**Ashtakavarga**: POST /api/v1/ashtakavarga/{bav|sav|shodhana}\n'
        '**Legacy**: POST /api/v1/houses/second, /api/v1/houses/third'
    ),
servers=[
    {
        "url": "https://api.krishnalaya.cloud",
        "description": "Production API"
    }
],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ai.krishnalaya.cloud"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Legacy house endpoints (v1)
app.include_router(second_house_router)
app.include_router(third_house_router)

# New unified house endpoints (all 12)
app.include_router(houses_router)

# Varga chart endpoints
app.include_router(varga_router)

# Ashtakavarga endpoints
app.include_router(av_router)


@app.get('/', tags=['Health'])
async def root() -> dict:
    return {
        'service': 'Krishnalaya Vedic Astrology API',
        'version': '2.0.0',
        'status': 'operational',
        'endpoints': {
            'houses': 'POST /api/v1/houses/{1-12}',
            'varga':  'POST /api/v1/varga/{d1|d2|d3|d9|d10|d12|d16|d24|d60}',
            'ashtakavarga': {
                'bav':      'POST /api/v1/ashtakavarga/bav',
                'sav':      'POST /api/v1/ashtakavarga/sav',
                'shodhana': 'POST /api/v1/ashtakavarga/shodhana',
            },
            'legacy': {
                'second_house': 'POST /api/v1/houses/second',
                'third_house':  'POST /api/v1/houses/third',
            },
            'docs': '/docs',
        },
    }
