import os
import shutil
import zipfile

from celery import shared_task, Task, task

from tika_tasks import create_index

from django.conf import settings


class UnzipTask(Task):
    abstract = True

    def on_success(self, *args, **kwargs):
        """
        If we are in deployment mode, create the corresponding index after the task
        has succeeded.
        """
        if settings.DEPLOYMENT:
            create_index.delay(self.index)


@shared_task(bind=True, base=UnzipTask)
def unzip(self, input_zip, output_folder, index, *args, **kwargs):
    """
    Celery task which unzips files in a .zip archive and ignores folder
    structure, taking each file to the top level of the output folder.
    """
    self.index = index
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
