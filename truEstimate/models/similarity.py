import numpy as np


class SimilarityCalculator:
    def __init__(self, max_values={'devTier': 4, 'projectArea': 4, 'micromarket': '', 'lat_long_radius_km': 741,
                 'projectLandArea': 1, 'cagr': 1}):
        """
        max_values: dict containing max differences or ranges for normalization:
        {
            'devTier': int,
            'micromarket': str,
            'projectArea': int,
            'lat_long_radius_km': float,  
            'projectLandArea': float,
            'commonPricePerSqft': float,
            'cagr': float
        }
        """
        self.max_values = max_values

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great-circle distance between two points
        on the Earth surface specified in decimal degrees.
        Returns distance in kilometers.
        """
        # convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

        # haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat / 2)**2 + np.cos(lat1) * \
            np.cos(lat2) * np.sin(dlon / 2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        r = 6371  # Radius of Earth in kilometers
        return c * r

    def nominal_distance(self, v1, v2):
        return 0 if v1 == v2 else 1

    def ordinal_distance(self, v1, v2, max_diff):
        return abs(v1 - v2) / max_diff if max_diff != 0 else 0

    def numeric_distance(self, v1, v2, max_range):
        return abs(v1 - v2) / max_range if max_range != 0 else 0

    def geospatial_distance(self, lat1, lon1, lat2, lon2, max_radius_km):
        dist_km = self.haversine_distance(lat1, lon1, lat2, lon2)
        return dist_km / max_radius_km if max_radius_km != 0 else 0

    def euclidean_distance(self, vals1, vals2, max_ranges):
        # vals1, vals2: list of numeric features
        # max_ranges: list of max ranges for each numeric feature
        dist_sq_sum = 0
        for i, (v1, v2) in enumerate(zip(vals1, vals2)):
            max_range = max_ranges[i]
            if max_range == 0:
                norm_diff = 0
            else:
                norm_diff = (v1 - v2) / max_range
            dist_sq_sum += norm_diff**2
        return np.sqrt(dist_sq_sum)

    def compute_similarity(self, prop1, prop2):
        """
        prop1, prop2: dicts with keys:
            devTier (int),
            assetType (str),
            micromarket (int),
            lat (float),
            long (float),
            projectArea (int),
            projectLandArea (float),
            area (str),
            commonPricePerSqft (float),
            cagr (float)
        Returns similarity score between 0 (totally different) and 1 (identical)
        """

        # Ordinal categorical distances (normalized)
        devTier_dist = self.ordinal_distance(
            prop1['devTier'], prop2['devTier'], self.max_values['devTier'])
        projectArea_dist = self.ordinal_distance(
            prop1['projectArea'], prop2['projectArea'], self.max_values['projectArea'])

        # Nominal categorical distances (0 or 1)
        assetType_dist = self.nominal_distance(
            prop1['assetType'], prop2['assetType'])
        area_dist = self.nominal_distance(prop1['area'], prop2['area'])
        micromarket_dist = self.nominal_distance(
            prop1['micromarket'], prop2['micromarket'])

        # Geospatial distance normalized
        geo_dist = self.geospatial_distance(
            prop1['lat'], prop1['long'], prop2['lat'], prop2['long'], self.max_values['lat_long_radius_km'])

        # Numeric Euclidean distance for projectLandArea, commonPricePerSqft, cagr
        numeric_features1 = [
            prop1['projectLandArea'],
            prop1['cagr']
        ]
        numeric_features2 = [
            prop2['projectLandArea'],
            prop2['cagr']
        ]
        max_ranges = [
            self.max_values['projectLandArea'],
            self.max_values['cagr']
        ]
        numeric_dist = self.euclidean_distance(
            numeric_features1, numeric_features2, max_ranges)

        # Combine distances with weights
        total_dist = (
            # average ordinal
            0.3*(devTier_dist + micromarket_dist+projectArea_dist) / 3 +
            # average nominal
            0.1 * (assetType_dist + area_dist) / 2 +
            0.4 * geo_dist +
            0.3 * numeric_dist
        )

        # similarity = 1 - normalized_distance (clamped 0 to 1)
        similarity = max(0, 1 - total_dist)
        return similarity
