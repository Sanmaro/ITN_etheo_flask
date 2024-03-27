import os
import unittest
from unittest.mock import call, MagicMock, mock_open, patch
from classes.Event import Event, EventManager

class TestEvent(unittest.TestCase):
    def setUp(self):
        self.mock_file = MagicMock()
        self.mock_file.filename = "test_file.pdf"

    def test_upload_document(self):
        event = Event(
            description="Test Event",
            date="2022-01-01",
            location="Test Location",
            document=self.mock_file,
            insurance_id=1,
            event_id=1
        )
        event.upload_document()
        expected_path = os.path.join(Event.UPLOAD_FOLDER, "event1_file.pdf")
        self.mock_file.save.assert_called_once_with(expected_path)

    @patch("os.remove")
    @patch("os.scandir")
    def test_delete_document(self, mock_scandir, mock_remove):
        mock_entry = MagicMock()
        mock_entry.name = "event1_file.pdf"
        mock_scandir.return_value = [mock_entry]
        Event.delete_document(1)
        expected_path = os.path.join("static/docs/events/event1_file.pdf")
        mock_remove.assert_called_once_with(os.path.normpath(expected_path))


class TestEventManager(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock()
        self.event_manager = EventManager(self.db)
        self.event = Event(
            "Test Event", "2022-01-01", "Test Location", 
            document=MagicMock(filename="test_file.pdf"), 
            insurance_id=1, event_id=1
            )

    @patch.object(Event, "upload_document")
    @patch("os.scandir")
    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_save(self, mock_open, mock_scandir, mock_rename_document):
        mock_file = mock_open.return_value
        mock_upload_document = MagicMock()
        mock_upload_document.return_value = "temp_file.pdf"
        self.db.execute.return_value = 1
        mock_entry = MagicMock()
        mock_entry.name = "temp_file.pdf"
        mock_scandir.return_value = [mock_entry]
        mock_rename_document.return_value = "event1_file.pdf"
        self.event_manager.save(self.event)

        # Assert that db.execute was called twice
        self.assertEqual(len(self.db.execute.call_args_list), 2)

        # Assert the first call (insert event) was with the expected arguments
        self.assertEqual(self.db.execute.call_args_list[0], call(
            "INSERT INTO events (description, date, location, documents, insurance, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
            self.event.description, self.event.date, self.event.location, "event1_file.pdf", self.event.insurance_id, self.event.timestamp
        ))

        # Assert the second call (update event with the renamed document) was with the expected arguments
        self.assertEqual(self.db.execute.call_args_list[1], call(
            "UPDATE events SET documents=? WHERE event_id=?",
            "", 1
        ))
    
    def test_delete(self):
        self.event_manager.delete(1)
        self.db.execute.assert_called_once_with("DELETE FROM events WHERE event_id=?", 1)

    @patch.object(Event, "upload_document")
    def test_update(self, mock_upload_document):
        mock_upload_document.return_value = "event1_file.pdf"
        self.event_manager.update(self.event)
        self.db.execute.assert_called_once_with("UPDATE events SET description=?, date=?, location=?, documents=?, timestamp=? WHERE event_id=?", self.event.description, self.event.date, self.event.location, "event1_file.pdf", self.event.timestamp, self.event.event_id)

if __name__ == "__main__":
    unittest.main()
