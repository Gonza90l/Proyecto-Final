import os
from werkzeug.utils import secure_filename
from flask import send_from_directory

class ImageService:
    def __init__(self):
        self.upload_folder = os.path.join(os.getcwd(), 'uploads')
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    def upload_image(self, file):
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(self.upload_folder, filename)
            file.save(file_path)
            return file_path
        else:
            raise ValueError("Invalid file")

    def allowed_file(self, filename):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def get_image(self, filename):
        if self.allowed_file(filename):
            return send_from_directory(self.upload_folder, filename)
        else:
            raise ValueError("Invalid file type")

    def delete_image(self, filename):
        if self.allowed_file(filename):
            file_path = os.path.join(self.upload_folder, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        return False