FROM python:3.12-slim

WORKDIR /agent
COPY agent.py /agent/agent.py

ENTRYPOINT ["python", "/agent/agent.py"]
