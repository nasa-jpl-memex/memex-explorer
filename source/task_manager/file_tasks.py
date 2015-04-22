import os
import shutil
import zipfile

from celery import shared_task, Task, task

from base.models import Project

@shared_task()
def unzip(input_zip, folder):
    if not os.path.exists(folder):
        os.mkdir(folder)
    with zipfile.ZipFile(input_zip) as archive:
        for x in archive.namelist():
            filename = os.path.basename(x)
            if not filename:
                continue
            source = archive.open(x)
            target = file(os.path.join(folder, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)
    return "success"
    

