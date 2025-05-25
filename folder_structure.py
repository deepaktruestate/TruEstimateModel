import os

folders = [
    "truEstimate/data",
    "truEstimate/api",
    "truEstimate/services",
    "truEstimate/models",
    "truEstimate/utils",
    "truEstimate/tests"
]

init_files = [
    "truEstimate/api/__init__.py",
    "truEstimate/services/__init__.py",
    "truEstimate/models/__init__.py",
    "truEstimate/utils/__init__.py"
]

files_to_create = [
    "truEstimate/app.py",
    "truEstimate/requirements.txt",
    "truEstimate/config.py",
    "truEstimate/run.py",
    "truEstimate/data/rtm_properties.json",
    "truEstimate/api/property_routes.py",
    "truEstimate/api/estimate_routes.py",
    "truEstimate/services/property_service.py",
    "truEstimate/models/preprocessing.py",
    "truEstimate/models/similarity.py",
    "truEstimate/utils/geo_utils.py",
    "truEstimate/utils/file_utils.py",
    "truEstimate/tests/test_preprocessing.py",
    "truEstimate/tests/test_similarity.py",
    "truEstimate/tests/test_property_service.py",
    "truEstimate/tests/test_routes.py",
]

def create_folders():
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Created folder: {folder}")

def create_init_files():
    for file in init_files:
        with open(file, "w") as f:
            f.write("# Init file\n")
        print(f"Created init file: {file}")

def create_files():
    for file in files_to_create:
        if not os.path.exists(file):
            with open(file, "w") as f:
                f.write("")
            print(f"Created file: {file}")
        else:
            print(f"File already exists: {file}")

if __name__ == "__main__":
    create_folders()
    create_init_files()
    create_files()
    print("Folder structure setup complete!")
