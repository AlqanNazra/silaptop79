class NormalizationService:

    @staticmethod
    def normalize_weight(aggregated_weights: dict) -> dict:
        if not aggregated_weights:
            raise ValueError()
        total_weight = sum(aggregated_weights.values())
        
        if total_weight == 0:
            raise ValueError("Total agregasi bobot adalah 0, tidak bisa dinormalisasi.")

        normalized = {}
        for kriteria, weight in aggregated_weights.items():
            if weight < 0:
                raise ValueError()
            normalized[kriteria] = weight / total_weight

        return normalized

    @staticmethod
    def validate_normalization(normalized_weights: dict) -> bool:
        total = sum(normalized_weights.values())
        # Cek toleransi floating point
        return abs(total - 1.0) < 1e-6