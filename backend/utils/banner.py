from services.plugin_manager import PluginManager
from core.config import DEFAULT_MODEL


def print_banner():

    benchmarks = PluginManager.discover()

    print("=" * 100)
    print("LLM RELIABILITY BENCHMARK PLATFORM")
    print("=" * 100)

    print(f"Loaded Benchmarks : {len(benchmarks)}")
    print(f"Default Model     : {DEFAULT_MODEL}")
    print("=" * 100)