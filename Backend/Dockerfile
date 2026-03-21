FROM python:3.11-slim
WORKDIR /app

#install dependices 
COPY requirments.txt .
RUN pip install --no-cache-dir -r requirments.txt

COPY AgenticAiProject.py .
COPY server.py .
COPY secret.env .

EXPOSE 5000
CMD ["python","server.py"]