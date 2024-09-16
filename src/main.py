from fastapi import FastAPI

from proxy.router import router as proxy_router

app = FastAPI()


app.include_router(proxy_router)
