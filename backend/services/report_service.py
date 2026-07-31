class ReportService:

    @staticmethod
    def print_platform_results(results):

        print("\n" + "=" * 100)
        print("LLM RELIABILITY BENCHMARK PLATFORM")
        print("=" * 100)

        for model, data in results.items():

            print("\n" + "=" * 100)
            print(f"MODEL : {model}")
            print("=" * 100)

            overall = data["overall_reliability"]

            print(
                f"\nOverall Reliability Score : "
                f"{overall['overall_score']:.2f}/100"
            )

            print("\nBreakdown")

            for benchmark, score in overall["breakdown"].items():

                print(f"{benchmark:<30}: {score:.2f}")

            print("\nDetailed Benchmark Reports")

            for report in data["benchmark_reports"]:

                print("-" * 80)

                print(f"Benchmark : {report['benchmark']}")

                primary = report["primary_metric"]

                print(
                    f"{primary['name']:<25}: "
                    f"{primary['score']:.4f}"
                )

                print(
                    f"Average Latency         : "
                    f"{report['average_latency']:.3f} sec"
                )

            print("=" * 100)