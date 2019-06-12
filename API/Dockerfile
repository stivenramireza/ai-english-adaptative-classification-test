FROM ubuntu:latest
MAINTAINER Anderson Grajales "agrajal7@eafit.edu.co"

# Ubuntu setup
RUN apt update --yes
RUN apt install wget bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 --yes
RUN apt install git mercurial subversion --yes

# Get Miniconda
RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
RUN bash ~/miniconda.sh -b -p /miniconda

ENV PATH=/miniconda/bin:${PATH}
RUN echo $PATH

RUN conda update conda --yes
RUN conda config --add channels conda-forge
RUN conda config --add channels contango

RUN which pip

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

# Automatically returns data
RUN chmod +x ./script.sh
RUN ./script.sh

# Turn on backend
ENTRYPOINT ["python"]
CMD ["app.py"]