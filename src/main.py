from fastapi import FastAPI
from src.routers import whatsapp_router, webhook_router



app = FastAPI()

app.include_router(whatsapp_router.router, prefix="/whatsapp", tags=["WhatsApp"])
app.include_router(webhook_router.router, prefix="/webhook", tags=["Webhook"])

@app.get("/")
async def root():
    return {"message": "Hello World"}