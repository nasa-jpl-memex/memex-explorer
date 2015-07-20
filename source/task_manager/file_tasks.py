import os
import shutil
import zipfile

from celery import shared_task, Task, task

from tika_tasks import create_index

from django.conf import settings


class UploadZipTask(Task):
    abstract = True

    def on_failure(self, *args, **kwargs):
        """If there is an error, set the index status to UPLOAD FAILURE."""
        self.index.status = "UPLOAD FAILURE"
        self.index.save()

    def on_success(self, *args, **kwargs):
        """
        If the upload task succeeded, change index status to UPLOAD SUCCESS.

        If we are in deployment mode, create the corresponding index after the task
        has succeeded.
        """
        self.index.status = "UPLOAD SUCCESS"
        self.index.num_files = len(os.listdir(self.get_dumped_data_path()))
        self.index.save()
        create_index.delay(self.index)


@shared_task(bind=True, base=UploadZipTask)
def upload_zip(self, index, *args, **kwargs):
    """
    Celery task which unzips files in a .zip archive and ignores folder
    structure, taking each file to the top level of the output folder.
    """
    self.index = index
    self.index.status = "STARTED"
    self.index.save()
    if not os.path.exists(self.index.data_folder):
        os.mkdir(self.index.data_folder)
    with zipfile.ZipFile(self.index.uploaded_data.name) as archive:
        for x in archive.namelist():
            filename = os.path.basename(x).decode("utf-8")
            if not filename:
                continue
            source = archive.open(x)
            target = open(os.path.join(self.index.data_folder, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)
    return "success"
