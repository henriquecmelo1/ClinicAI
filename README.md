create a virtual environment:
python -m venv venv

activate venv:
.\venv\Scripts\activate

install requirements:
pip install -r requirements.txt

run code:
uvicorn src.app:app --reload


.env file (environment variables):
