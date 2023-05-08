FROM python:3.10-slim

COPY . /ltv_analysis

WORKDIR /ltv_analysis

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "./src/frontend/Onboarding.py"]
