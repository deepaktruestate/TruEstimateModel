# TruEstimate-Model

TruEstimate-Model is a backend service for real estate property price estimation. It uses data preprocessing and similarity-based algorithms to estimate property prices based on comparable properties. The project is built with Python and Flask.

## Features

- Add, update, and delete property data.
- Estimate property price per square foot using similarity models.
- Batch processing and data conversion utilities (CSV/JSON).
- Modular code structure for easy customization.

## Project Structure

```
TruEstimate-Model/
│
├── truEstimate/
│   ├── app.py                      # Flask app entry point
│   ├── config.py                   # Configuration file
│   ├── api/
│   │   ├── __init__.py
│   │   ├── property_routes.py      # Property CRUD API routes
│   │   └── estimate_routes.py      # Price estimation API routes
│   ├── data/
│   │   └── rtm_properties.json     # Main property data (JSON)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── preprocessing.py        # Data preprocessing logic
│   │   └── similarity.py           # Similarity calculation logic
│   ├── services/
│   │   ├── __init__.py
│   │   ├── property_service.py     # Property management logic
│   │   └── estimate_service.py     # Price estimation logic
│   └── utils/
│       ├── __init__.py
│       ├── file_utils.py           # CSV/JSON utilities
│       └── propertyData.csv        # Example property data (CSV)
│
├── requirements.txt                # Python dependencies
```

## Setup

1. **Clone the repository**
   ```sh
   git clone <your-repo-url>
   cd TruEstimate-Model
   ```

2. **Create and activate a virtual environment**
   ```sh
   python -m venv venv
   venv\Scripts\activate   # On Windows
   # source venv/bin/activate   # On macOS/Linux
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the Flask app**
   ```sh
   python truEstimate.app
   ```
   The API will be available at `http://localhost:5000/`.

## API Endpoints

### Property Management

- `POST /property/addProperty`  
  Add a new property (expects JSON body).

- `PUT /property/updateProperty/<property_id>`  
  Update an existing property.

- `DELETE /property/deleteProperty/<property_id>`  
  Delete a property by ID.

### Price Estimation

- `POST /estimate/truestimate`  
  Estimate price per sqft for a property (expects JSON body).

## Utilities

- Convert CSV to JSON and vice versa using functions in `truEstimate/utils/file_utils.py`.
- Batch estimate prices for properties in a CSV using `calculate_true_estimate_for_csv` in `file_utils.py`.

## Data

- Main property data is stored in `truEstimate/data/rtm_properties.json`.
- Example property data in CSV: `truEstimate/utils/propertyData.csv`.

## Customization

- Preprocessing and similarity logic can be customized in `truEstimate/models/preprocessing.py` and `truEstimate/models/similarity.py`.
- Adjust similarity thresholds and neighbor count (`k`) in `truEstimate/services/estimate_service.py`.

---

**Author:** Deepak Goyal  
**Contact:** deepak@truestate.in
