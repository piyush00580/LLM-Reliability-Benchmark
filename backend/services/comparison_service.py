class ComparisonService:

    def compare(
        self,
        text,
        llm_services,
        benchmark_class
    ):

        reports = []

        for llm in llm_services:

            benchmark = benchmark_class(llm)

            report = benchmark.run(text)

            reports.append(report)

        return reports