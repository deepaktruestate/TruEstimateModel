import numpy as np

class Preprocessor:
    def __init__(self, min_max_values):
        self.dev_tier_mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        self.project_area_mapping = {'small': 0, 'medium': 1, 'big': 2}

        # Use externally provided min-max values
        self.min_max = min_max_values
        self.fitted = True  # Mark as fitted since min-max is already given

    def scale(self, x, key):
        min_val, max_val = self.min_max[key]
        return (x - min_val) / (max_val - min_val + 1e-8)  # add epsilon for safety

    def preprocess_property(self, prop):
        if not self.fitted:
            raise Exception("Preprocessor not ready. Provide min-max values first.")

        # Encode devTier and projectArea
        prop['devTier'] = self.dev_tier_mapping.get(prop['devTier'], -1)
        print(prop['devTier'])
        prop['projectArea'] = self.project_area_mapping.get(prop['projectArea'], -1)

        # Scale with provided min-max (log for land area)
        project_land_area_log = np.log1p(float(prop['projectLandArea']))
        prop['projectLandArea'] = self.scale(project_land_area_log, 'projectLandArea')

        prop['cagr'] = self.scale(float(prop['cagr']), 'cagr')

        # Ensure lat and long are float
        prop['lat'] = float(prop['lat'])
        prop['long'] = float(prop['long'])

        return prop
