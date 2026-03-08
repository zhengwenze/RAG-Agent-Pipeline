from fastapi import FastAPI

from app.api import agent, config, health, query, upload


app = FastAPI()

app.include_router(health.router)
app.include_router(upload.router)
app.include_router(query.router)
app.include_router(agent.router)
app.include_router(config.router)



