FROM python:3.6
LABEL MAINTAINER="Anderson Grajales"

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# Copy everything into the folder and move on from there
COPY . /app
RUN ls /app

ENV HOME=/app
WORKDIR /app


# Install requirements
# RUN pip install --no-cache-dir -r requirements.txt

RUN echo quick python test
RUN python test.py

RUN which python3
RUN chmod 644 app.py
# Open port
EXPOSE 5001

# Turn on backend
ENTRYPOINT ["python"]
CMD ["app.py"]