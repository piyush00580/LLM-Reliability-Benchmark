from config.reliability_config import RELIABILITY_WEIGHTS


class ReliabilityService:

    def __init__(self):
        self.weights = RELIABILITY_WEIGHTS

    def compute_overall_score(self, reports):

        weighted_sum = 0.0
        total_weight = 0.0

        breakdown = {}

        for report in reports:

            metric_name = report["primary_metric"]["name"]
            score = report["primary_metric"]["score"]

            benchmark_name = report["benchmark"]

            breakdown[benchmark_name] = round(score * 100, 2)

            weight = self.weights.get(metric_name)

            if weight is None:
                continue

            weighted_sum += score * weight
            total_weight += weight

        overall_score = (
            (weighted_sum / total_weight) * 100
            if total_weight > 0
            else 0
        )

        return {

            "overall_score": round(overall_score, 2),

            "breakdown": breakdown,

            "weights": self.weights

        }