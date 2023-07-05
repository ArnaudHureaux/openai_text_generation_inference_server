FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install openai
RUN pip install -r requirements.txt
RUN pip list