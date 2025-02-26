FROM node:22 as frontend-builder

WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

FROM python:3.12-slim


WORKDIR /app
COPY /backend/database.py . 
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
#EXPOSE 8080

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]