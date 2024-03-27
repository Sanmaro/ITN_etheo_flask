import os
from datetime import datetime

from flask import flash, redirect, request, url_for
from werkzeug.utils import secure_filename


# Set global variables for file upload
EXTENSIONS = {"doc", "docx", "jpg", "jpeg", "pdf", "png"}
UPLOAD_FOLDER = "static/docs/events"


def check_event_document(filename):
    """Check if event document's extension is in the allowed extensions"""
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in EXTENSIONS


def upload_event_document(file_name):
    """Upload document selected by user"""
    file = request.files["event_documents"]

    # If user does not select file, skip the rest
    if not file:
        return "" 
    file_extension = file.filename.split(".")[-1]

    # Rename the file to "eventID_file.EXTENSION" format 
    filename_full = f"{file_name}.{secure_filename(file_extension)}"
    
    # Save the document
    file.save(os.path.join(UPLOAD_FOLDER, filename_full))
    return filename_full


def delete_event_document(file_name):
    """Delete user's document"""
    filenames = os.scandir(UPLOAD_FOLDER)
    for filename in filenames:
        if file_name in filename.name:
            os.remove(f"{UPLOAD_FOLDER}/{filename.name}")


def write_into_events(db, query, insurance_id, event_id):
    """Update or insert an insurance event into the database"""
    description = request.form.get("event_description")
    date = request.form.get("event_date")
    location = request.form.get("event_location")
    timestamp = datetime.now()
    document = request.files["event_documents"] 
    if document and not check_event_document(document.filename):
        flash("Invalid type of file.")
        return redirect(url_for('my_events', insurance_id=insurance_id))
    file_name = f"event{event_id}_file"
    delete_event_document(event_id, file_name)
    filename_full = upload_event_document(file_name)

    # Report a new insurance event
    if query.startswith("INSERT"):
        db.execute(query,
                    description, date, location, filename_full, insurance_id, timestamp)    
        flash("New event was successfully reported.")

    # Update the existing event
    elif query.startswith("UPDATE"):
        db.execute(query,
                   description, date, location, filename_full, timestamp, event_id)
        flash("You have successfully updated the insurance event.")
    return redirect(url_for("my_events", insurance_id=insurance_id))