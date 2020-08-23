# Import Python runtime and set up working directory
FROM python:3.7.3-stretch
WORKDIR /app
ADD . /app

# Install any necessary dependencies
RUN pip install --upgrade pip &&\
    pip install --trusted-host pypi.python.org -r requirements.txt

# Open port 80 for serving the webpage
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "app.py"]