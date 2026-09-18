from services.llm_factory import LLMFactory
from services.plugin_manager import PluginManager
from services.benchmark_history_service import BenchmarkHistoryService
from services.export_service import ExportService


def test_llm_factory_available_models():
    models = LLMFactory.available_models()

    assert "gemini" in models
    assert "ollama" in models
    assert "groq" in models
    assert "mistral" in models

    assert "mock_excellent" in models
    assert "mock_average" in models
    assert "mock_poor" in models


def test_llm_factory_creates_mock_model():
    service = LLMFactory.create("mock_excellent")

    assert service is not None
    assert service.get_model_name() == "mock_excellent"


def test_llm_factory_creates_gemini_service():
    service = LLMFactory.create("gemini")

    assert service is not None
    assert service.get_model_name() == "gemini-2.5-flash-lite"


def test_llm_factory_creates_ollama_service():
    service = LLMFactory.create("ollama")

    assert service is not None
    assert service.get_model_name() == "llama3.2:3b"


def test_llm_factory_creates_groq_service():
    service = LLMFactory.create("groq")

    assert service is not None
    assert service.get_model_name() == "openai/gpt-oss-120b"


def test_llm_factory_creates_mistral_service():
    service = LLMFactory.create("mistral")

    assert service is not None
    assert service.get_model_name() == "ministral-3b-2512"


def test_llm_factory_creates_selected_models():
    services = LLMFactory.create_selected(
        ["mock_excellent", "mock_average"]
    )

    assert len(services) == 2

    model_names = [
        service.get_model_name()
        for service in services
    ]

    assert "mock_excellent" in model_names
    assert "mock_average" in model_names


def test_llm_factory_rejects_invalid_model():
    try:
        LLMFactory.create("invalid_model")
        assert False
    except ValueError:
        assert True


def test_plugin_manager_discovers_benchmarks():
    plugins = PluginManager.discover()

    assert len(plugins) >= 4

    plugin_names = [
        plugin.__name__
        for plugin in plugins
    ]

    assert "ConsistencyBenchmark" in plugin_names
    assert "HallucinationBenchmark" in plugin_names
    assert "InformationDecayBenchmark" in plugin_names
    assert "PromptRobustnessBenchmark" in plugin_names


def test_history_database_initializes():
    service = BenchmarkHistoryService()

    runs = service.get_all_runs()

    assert isinstance(runs, list)


def test_export_service_directory_exists():
    ExportService.REPORTS_DIR.mkdir(exist_ok=True)

    assert ExportService.REPORTS_DIR.exists()