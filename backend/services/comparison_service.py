class ComparisonService:

    def compare(
        self,
        text,
        llm_services,
        benchmark_class
    ):

        reports = []

        for llm in llm_services:

            try:
                benchmark = benchmark_class(llm)

                report = benchmark.run(text)

                reports.append(report)

            except Exception as e:
                model_name = llm.get_model_name()

                reports.append({
                    "benchmark": benchmark_class.__name__.replace(
                        "Benchmark", ""
                    ),
                    "model": model_name,
                    "status": "failed",
                    "error": str(e),
                    "score": 0,
                    "latency": 0,
                    "metrics": {},
                    "results": []
                })

        return reports