from services.comparison_service import ComparisonService
from services.reliability_service import ReliabilityService
from services.plugin_manager import PluginManager


class PlatformRunner:

    def __init__(self):

        self.comparison_service = ComparisonService()
        self.reliability_service = ReliabilityService()

    def run(self, text, llm_services, benchmark_classes=None):

        platform_results = {}

        for llm in llm_services:

            platform_results[llm.get_model_name()] = {
                "benchmark_reports": [],
                "overall_reliability": None
            }

        if benchmark_classes is None:
            benchmark_classes = PluginManager.discover()

        for benchmark_class in benchmark_classes:

            reports = self.comparison_service.compare(
                text=text,
                llm_services=llm_services,
                benchmark_class=benchmark_class
            )

            for report in reports:

                model = report["model"]

                platform_results[model]["benchmark_reports"].append(
                    report
                )

        for model in platform_results:
            reports = platform_results[model]["benchmark_reports"]

            successful_reports = [
                report
                for report in reports
                if report.get("status") != "failed"
            ]

            overall = self.reliability_service.compute_overall_score(
                successful_reports
            )

            platform_results[model]["overall_reliability"] = overall

        return platform_results