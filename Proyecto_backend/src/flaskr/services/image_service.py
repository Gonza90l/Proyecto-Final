import os
from werkzeug.utils import secure_filename
from flask import send_from_directory
import uuid

class ImageService:
    def __init__(self):
        self.upload_folder = os.path.join(os.getcwd(), 'uploads')
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    def upload_image(self, file):
        # Debugging the file variable
        print(f"File received: {file}")
        print(f"File name: {file.filename}")
        
        if file and self.allowed_file(file.filename):
            # Generate a unique filename using UUID
            file_ext = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4().hex}{file_ext}"
            filename = secure_filename(unique_filename)
            file_path = os.path.join(self.upload_folder, filename)
            file.save(file_path)
            return filename  # Return only the filename with extension
        else:
            raise ValueError("Invalid file")

    def allowed_file(self, filename):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        is_allowed = '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        print(f"Is allowed file: {is_allowed}")
        return is_allowed

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
            else:
                raise ValueError("File not found")
        else:
            raise ValueError("Invalid file type")