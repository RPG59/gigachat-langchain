FROM python:3.11

WORKDIR /app

COPY ./requirements.txt .
COPY ./src .

RUN pip install --no-cache-dir -r requirements.txt

# Download Sentence Transformers Model
RUN python3 -c "import os; from sentence_transformers import SentenceTransformer; SentenceTransformer(os.environ.get('model_name_or_path', 'sentence-transformers/all-mpnet-base-v2'));"

CMD ["uvicorn", "main:app"]
