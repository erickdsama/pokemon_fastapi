FROM python:3.10

WORKDIR test

COPY ./app/requirements.txt /test/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /test/requirements.txt

COPY ./app /test/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--reload"]