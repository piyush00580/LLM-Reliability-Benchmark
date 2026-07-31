from pathlib import Path
import time
from services.platform_runner import PlatformRunner
from services.dataset_runner import DatasetRunner
from services.report_service import ReportService
from services.llm_factory import LLMFactory
from utils.banner import print_banner
from flask_cors import CORS



def create_models():
    """
    Create the list of LLMs to benchmark.
    """
    models = [
        LLMFactory.create("gemini"),
        LLMFactory.create("mock")
    ]

    print("\nActive Models")

    for model in models:
        print(f"• {model.get_model_name()}")

    return models


def custom_text_mode():
    """
    Benchmark custom user input.
    """

    text = input("\nEnter text:\n\n").strip()

    if not text:
        print("\n Input text cannot be empty.")
        return

    start = time.perf_counter()
    
    platform = PlatformRunner()

    try:
        results = platform.run(
            text=text,
            llm_services=create_models()
        )

        ReportService.print_platform_results(results)
        elapsed = time.perf_counter() - start
        print(f"\nExecution Time : {elapsed:.2f} sec")
        print("\n✓ Benchmark completed successfully.")

    

    except Exception as e:
        print(f"\n Benchmark failed.\nReason: {e}")



def dataset_mode():
    """
    Run benchmark on dataset(s).
    """

    datasets_path = Path("datasets")

    if not datasets_path.exists():
        print("\n 'datasets' folder not found.")
        return

    datasets = sorted([
        folder
        for folder in datasets_path.iterdir()
        if folder.is_dir()
    ])

    if not datasets:
        print("\n No datasets found.")
        return

    print("\nAvailable Datasets\n")

    for index, dataset in enumerate(datasets, start=1):
        print(f"{index}. {dataset.name.title()}")

    print(f"{len(datasets) + 1}. Run All")

    choice = input("\nSelect option: ").strip()

    if not choice.isdigit():
        print("\n Please enter a valid number.")
        return

    choice = int(choice)

    if choice < 1 or choice > len(datasets) + 1:
        print("\n Invalid dataset selection.")
        return

    start = time.perf_counter()

    runner = DatasetRunner()

    try:

        if choice == len(datasets) + 1:

            runner.run(
                datasets_path,
                create_models()
            )

        else:

            runner.run(
                datasets[choice - 1],
                create_models()
            )

        elapsed = time.perf_counter() - start
        print(f"\nExecution Time : {elapsed:.2f} sec")
        print("\n✓ Benchmark completed successfully.")

    except Exception as e:
        print(f"\n Dataset Benchmark Failed.\nReason: {e}")



def main():

    while True:
        print_banner()

        print("\n1. Benchmark Custom Text")
        print("2. Run Dataset Benchmark")
        print("0. Exit")

        choice = input("\nSelect option: ").strip()

        if choice == "1":

            custom_text_mode()

        elif choice == "2":

            dataset_mode()

        elif choice == "0":

            print("\nGoodbye!")
            break

        else:

            print("\n Invalid option. Please enter 0, 1 or 2.")


if __name__ == "__main__":
    main()