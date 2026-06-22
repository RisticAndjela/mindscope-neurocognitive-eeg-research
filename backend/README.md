```
py -3.12 -m venv .venv
.venv\Scripts\activate
python --version
pip install -r requirements.txt
```
```
python -m uvicorn app.main:app --reload
```