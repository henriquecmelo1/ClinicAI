create a virtual environment:
python -m venv venv

activate venv:
.\venv\Scripts\activate

install requirements:
pip install -r requirements.txt

run code:
uvicorn src.app:app --reload

ngrok setup:
ngrok http --url=sequestrable-serpentinely-arla.ngrok-free.app 8000 

webhook setup:
Set the webhook URL in your WhatsApp Business settings to:
https://<your-ngrok-subdomain>.ngrok-free.app/webhook
put your verify token in the .env



.env file (environment variables):
