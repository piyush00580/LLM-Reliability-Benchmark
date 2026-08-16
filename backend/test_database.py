from services.benchmark_history_service import BenchmarkHistoryService


history = BenchmarkHistoryService()

history.save_run(
    model="mock_average",
    benchmark="Consistency",
    score=1.0,
    latency=0.6,
    input_text="Artificial Intelligence is transforming healthcare."
)

print("Benchmark run saved successfully!")