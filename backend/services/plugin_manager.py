import inspect
import importlib
import pkgutil

from benchmarks.benchmark import Benchmark


class PluginManager:

    @staticmethod
    def discover():
        """
        Discover every benchmark class inside the benchmarks package.
        """

        benchmark_classes = []

        package = importlib.import_module("benchmarks")

        for _, module_name, _ in pkgutil.iter_modules(package.__path__):

            # Ignore the abstract base class
            if module_name == "benchmark":
                continue

            module = importlib.import_module(
                f"benchmarks.{module_name}"
            )

            for _, obj in inspect.getmembers(
                module,
                inspect.isclass
            ):

                if (
                    issubclass(obj, Benchmark)
                    and obj is not Benchmark
                ):
                    benchmark_classes.append(obj)

        return benchmark_classes