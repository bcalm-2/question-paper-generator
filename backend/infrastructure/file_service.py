import os
import json
import logging

logger = logging.getLogger(__name__)

class FileService:
    """
    Service responsible for all file system operations and resource mapping.
    Handles uploads, directory management, and mapping lookups.
    """
    def __init__(self, resource_folder="resources", mapping_file="resources/subject_mapping.json"):
        self.RESOURCE_FOLDER = resource_folder
        self.MAPPING_FILE = mapping_file
        self._ensure_resource_folder()

    def _ensure_resource_folder(self):
        """Ensures the resource storage directory exists."""
        if not os.path.exists(self.RESOURCE_FOLDER):
            os.makedirs(self.RESOURCE_FOLDER)

    def save_file(self, file_obj, subject_name):
        """
        Saves an uploaded file and updates the resource mapping.
        """
        filename = file_obj.filename
        save_path = os.path.join(self.RESOURCE_FOLDER, filename)
        
        logger.info(f"Saving file: {filename} for subject: {subject_name}")
        file_obj.save(save_path)
        
        self._update_mapping(filename, subject_name)
        return save_path

    def _update_mapping(self, filename, subject_name):
        """Updates the mapping.json file with the new resource-subject association."""
        mapping_data = self.get_mapping()
        mapping_data[filename] = subject_name
        
        try:
            with open(self.MAPPING_FILE, "w") as f:
                json.dump(mapping_data, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to update mapping file: {e}")

    def get_mapping(self):
        """Loads and returns the current resource mapping."""
        if not os.path.exists(self.MAPPING_FILE):
            return {}
        try:
            with open(self.MAPPING_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading mapping file: {e}")
            return {}

    def list_files(self):
        """
        Returns a structured list of all files in the resource folder with their subject mappings.
        """
        if not os.path.exists(self.RESOURCE_FOLDER):
            return []

        files = os.listdir(self.RESOURCE_FOLDER)
        mapping = self.get_mapping()

        return [
            {"name": f, "subject": mapping.get(f, "Unassigned")}
            for f in files if os.path.isfile(os.path.join(self.RESOURCE_FOLDER, f))
        ]

    def delete_entry(self, filename):
        """
        Permanently deletes a file from disk and removes its entry from mapping.json.
        """
        file_path = os.path.join(self.RESOURCE_FOLDER, filename)
        if not os.path.exists(file_path):
            return False

        try:
            os.remove(file_path)
            logger.info(f"File deleted: {filename}")
            
            mapping = self.get_mapping()
            if filename in mapping:
                del mapping[filename]
                with open(self.MAPPING_FILE, "w") as f:
                    json.dump(mapping, f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Failed to delete file {filename}: {e}")
            return False

    def get_file_path_for_subject(self, subject_name, fallback_file="general_reference.txt"):
        """
        Locates the physical file path for a given subject name.
        Falls back to a general reference if no specific match is found.
        """
        mapping = self.get_mapping()
        
        # Look for files mapped to this subject
        subject_files = [fname for fname, sub in mapping.items() if sub == subject_name]
        
        if subject_files:
            potential_path = os.path.join(self.RESOURCE_FOLDER, subject_files[0])
            if os.path.exists(potential_path):
                return potential_path
            logger.warning(f"File {subject_files[0]} mapped to {subject_name} missing from disk.")
            
        # Fallback
        fallback_path = os.path.join(self.RESOURCE_FOLDER, fallback_file)
        if os.path.exists(fallback_path):
            logger.info(f"Using fallback reference for {subject_name}: {fallback_file}")
            return fallback_path
            
        return None
