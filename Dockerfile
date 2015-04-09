FROM continuumio/miniconda
ENV PYTHONUNBUFFERED 1
RUN conda update conda conda-env
ADD environment.yml /
RUN conda env update --file environment.yml --name root
ADD source /source
WORKDIR /source
RUN python /source/manage.py migrate
CMD python /source/manage.py runserver 0.0.0.0:8000
