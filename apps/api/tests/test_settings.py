import importlib


def test_prod_settings__renderer_is_json_only():
    prod = importlib.import_module("config.settings.prod")

    assert prod.REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] == [
        "rest_framework.renderers.JSONRenderer"
    ]
