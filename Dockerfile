# docker build -t transactions_processing-app .
# docker run -p 8000:8000 --env-file .env -v $(pwd)/data:/usr/src/app/data transactions_processing-app


#set slim version
FROM python:3.9-slim

# set working directory
WORKDIR /usr/src/app

# copy requirements.txt
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy all files
COPY . .

# open port 8000
EXPOSE 8000

# run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
