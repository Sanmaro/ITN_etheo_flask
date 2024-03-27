import os
from datetime import datetime
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename

class Event:
    EXTENSIONS = {"doc", "docx", "jpg", "jpeg", "pdf", "png"}
    UPLOAD_FOLDER = os.path.normpath("static/docs/events")

    def __init__(self, description, date, location, document, insurance_id=None, event_id=None):
        self.event_id = event_id
        self.description = description
        self.date = date
        self.location = location
        self.timestamp = datetime.now()
        self.document = document
        self.insurance_id = insurance_id

    def upload_document(self):
        """Upload the document associated with the event."""
        if not self.document:
            return ""

        file_extension = self.document.filename.split(".")[-1]
        filename_full = f"event{self.event_id}_file.{secure_filename(file_extension)}"
        self.document.save(os.path.join(self.UPLOAD_FOLDER, filename_full))
        return filename_full

    @classmethod    
    def rename_document(cls, temp_name, event_id):
        full_name = ""
        for file in os.scandir(cls.UPLOAD_FOLDER):
            if file.name.startswith(temp_name):
                final_name = f"event{event_id}_file"
                file_extension = os.path.splitext(file.name)[-1]
                source_path = os.path.join(cls.UPLOAD_FOLDER, file.name)
                full_name = f"{final_name}{file_extension}"
                destination_path = os.path.join(cls.UPLOAD_FOLDER, full_name)
                os.rename(source_path, destination_path)
                break
        return full_name

    @classmethod
    def check_document_extension(cls, filename):
        """Check if the event document's extension is allowed."""
        return "." in filename and filename.rsplit(".", 1)[1].lower() in cls.EXTENSIONS

    @classmethod
    def delete_document(cls, event_id):
        """Delete the document associated with the event."""
        filenames = os.scandir(cls.UPLOAD_FOLDER)
        for file in filenames:
            if str(event_id) in file.name:
                os.remove(os.path.join(cls.UPLOAD_FOLDER, file.name))


class EventManager:
    def __init__(self, db):
        self.db = db

    def get_all(self, insurance_id):
        return self.db.execute("SELECT * FROM events WHERE insurance=?", insurance_id)

    def get_details(self, event_id):
        return self.db.execute("SELECT * FROM events WHERE event_id=?", event_id)[0]
        

    def save(self, event):
        """Insert or update an event in the database."""
        if event.document and not Event.check_document_extension(event.document.filename):
            return False

        Event.delete_document(f"event{event.event_id}_file")
        filename_full = event.upload_document()
        event_id = self.db.execute("INSERT INTO events (description, date, location, documents, insurance, timestamp) VALUES (?, ?, ?, ?, ?, ?)", event.description, event.date, event.location, filename_full, event.insurance_id, event.timestamp)

        # Rename the saved file to match event ID
        full_name = Event.rename_document("eventNone_file", event_id)
        self.db.execute("UPDATE events SET documents=? WHERE event_id=?", full_name, event_id)
        return True
    
    def delete(self, event_id):
        Event.delete_document(event_id)
        self.db.execute("DELETE FROM events WHERE event_id=?", event_id)

    def update(self, event):
        filename_full = f"event{event.event_id}_file"
        if event.document:
            if not Event.check_document_extension(event.document.filename):
                return False
            Event.delete_document(filename_full)
            filename_full = event.upload_document()
        self.db.execute("UPDATE events SET description=?, date=?, location=?, documents=?, timestamp=? WHERE event_id=?", event.description, event.date, event.location, filename_full, event.timestamp, event.event_id)
        return True
    
