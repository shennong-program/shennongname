# 3.11-slim-buster is the latest version of python3.11, slim is a smaller version of the image, buster is the version of debian.
FROM python:3.11-slim-buster

WORKDIR /app
COPY . /app

RUN cp .env.example .env
RUN pip install .

EXPOSE 5001

# Run the application when the container launches
CMD ["python", "shennongname/flask/run.py"]
