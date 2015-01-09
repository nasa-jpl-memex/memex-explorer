from . import app, db
from .models import Image
import os
from flask import send_from_directory, render_template, url_for
from db_api import get_uploaded_image_names

def lost_camera_retreive(serial_num):
    camera_dir = app.config['LOST_CAMERA_DIR']
    path = os.path.join(camera_dir, serial_num)
    static_dir_path = os.path.join(os.path.dirname(__file__), "static")

    list_of_pics = []
    if os.path.exists(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, static_dir_path)
                if 'stolen' in relative_path:
                    list_of_pics.append((relative_path, file, 'stolencamera'))
                else:
                    list_of_pics.append((relative_path, file, 'cameratrace'))

    return list_of_pics


def image_retrieve(filename, size=None):
    # if size == None or size == 'full':

    for x in (app.config['UPLOAD_DIR'],
              app.config['STATIC_IMAGE_DIR'],
              app.config['LOST_CAMERA_DIR']):
        if os.path.exists(os.path.join(x, filename)):
            return send_from_directory(x, filename)


def serve_upload_page():
    """Returns response to upload an image and lists other uploaded images"""
    image_names = get_uploaded_image_names()
    image_pages = [ {"name":filename, "url":url_for('compare', image=filename) } \
                    for filename in image_names]
    return render_template('upload.html', image_pages=image_pages)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def process_exif(exif_data, img_dir, filename, image_space):
    # Get the EXIF data from the image
    LSVN = getattr(exif_data.get('EXIF LensSerialNumber'), 'values', None)
    MSNF = getattr(exif_data.get('MakerNote SerialNumberFormat'), 'values', None)
    BSN = getattr(exif_data.get('EXIF BodySerialNumber'), 'values', None)
    MISN = getattr(exif_data.get('MakerNote InternalSerialNumber'), 'values', None)
    MSN = getattr(exif_data.get('MakerNote SerialNumber'), 'values', None)
    IBSN = getattr(exif_data.get('Image BodySerialNumber'), 'values', None)

    image = Image(directory=img_dir,
                  filename = filename,
                  EXIF_LensSerialNumber = LSVN,
                  MakerNote_SerialNumberFormat = MSNF,
                  EXIF_BodySerialNumber = BSN,
                  MakerNote_InternalSerialNumber = MISN,
                  MakerNote_SerialNumber = MSN,
                  Image_BodySerialNumber = IBSN,
                  uploaded = 1,
                  )

    image_space.images.append(image)
    # Add uploaded image to the database

    # Add uploaded image to the database
    db.session.add(image)
    db.session.commit()