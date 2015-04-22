import os
import zipfile

from celery import shared_task, Task, task

from base.models import Project

@shared_task()
def unzip(input_file, destination=""):
    with zipfile.ZipFile(input_file) as archive:
        archive.extractall()
#        for x in archive.infolist():
#            print(x.filename)
#            archive.extract(x, path=destination)
    

