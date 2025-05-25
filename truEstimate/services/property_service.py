import json

class PropertyService:
    def __init__(self, json_file, preprocessor=None):
        self.json_file = json_file
        self.preprocessor = preprocessor  # Optional preprocessing function/class

    def _load_data(self):
        try:
            with open(self.json_file, "r") as f:
                return json.load(f)
        except:
            return []

    def _save_data(self, data):
        with open(self.json_file, "w") as f:
            json.dump(data, f, indent=4)

    def preprocess_property(self, prop):
        if self.preprocessor:
            return self.preprocessor.process(prop)  # Assuming preprocessor has a process() method
        # else return property as is
        return prop

    def add_property(self, new_property):
        new_property = self.preprocess_property(new_property)
        data = self._load_data()
        for prop in data:
            if prop.get('id') == new_property.get('id'):
                return False
        data.append(new_property)
        self._save_data(data)
        return True

    def update_property(self, property_id, update_data):
        update_data = self.preprocess_property(update_data)
        data = self._load_data()
        for prop in data:
            if prop.get('id') == property_id:
                prop.update(update_data)
                self._save_data(data)
                return True
        return False

    def delete_property(self, property_id):
        data = self._load_data()
        new_data = [p for p in data if p.get('id') != property_id]
        if len(new_data) == len(data):
            return False
        self._save_data(new_data)
        return True
