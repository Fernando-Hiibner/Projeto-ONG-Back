# import os
# from flask import Flask, flash, request, redirect, url_for
# from werkzeug.utils import secure_filename

# class UploadController:
#     def __init__(self):
#         self.ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "jfif", "gif"}

#     def allowedFile(self, filename):
#         return '.' in filename and \
#             filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

#     def uploadPubFile(self, request):
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and self.allowedFile(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(App.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('download_file', name=filename))

#     def uploadProfilePicture(self, request):
#         ...

#     def uploadBannerPicture(self, request):
#         ...