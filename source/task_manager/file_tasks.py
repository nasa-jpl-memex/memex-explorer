import os
import shutil
import zipfile

from celery import shared_task, Task, task

@shared_task()
def unzip(input_zip, output_folder):
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    with zipfile.ZipFile(input_zip) as archive:
        for x in archive.namelist():
            filename = os.path.basename(x)
            if not filename:
                continue
            source = archive.open(x)
            target = file(os.path.join(output_folder, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)
    return "success"
    

