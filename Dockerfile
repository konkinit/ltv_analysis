FROM python:3.10-slim

COPY . .

WORKDIR /src/frontend

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "Onboarding.py"]
