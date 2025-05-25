import json
from truEstimate.models import Preprocessor, SimilarityCalculator
from operator import itemgetter

class EstimateService:
    def __init__(self, json_file, similarity_threshold=0.6, k=5):
        self.json_file = json_file
        self.similarity_threshold = similarity_threshold
        self.k = k
        self.preprocessor = Preprocessor({'cagr':[0,15],'projectLandArea':[0,100]})
        self.similarity_calculator = SimilarityCalculator()

    def _load_data(self):
        try:
            with open(self.json_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def estimate_price(self, new_property):
        data = self._load_data()
        new_prop_processed = self.preprocessor.preprocess_property(new_property)

        scored = []
        for prop in data:
            sim = self.similarity_calculator.compute_similarity(new_prop_processed, prop)
            if sim >= self.similarity_threshold:
                scored.append((sim, prop))

        if not scored:
            return None

        scored.sort(key=itemgetter(0), reverse=True)
        top_k = scored[:self.k]

        prices = [p[1].get("commonPricePerSqft", 0) for p in top_k]
        if not prices or sum(prices) == 0:
            return None

        avg_price = sum(prices) / len(prices)

        risk_discount = new_prop_processed.get("riskDiscount",0.2)
        final_price = avg_price * (1 - risk_discount)

        return round(final_price, 2)
