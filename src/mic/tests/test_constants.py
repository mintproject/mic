from mic.constants import ModelCatalogTypes


def test_model_catalog_types():
    assert ModelCatalogTypes("Model Configuration") == ModelCatalogTypes.MODEL_CONFIGURATION
    assert ModelCatalogTypes("Data Transformation") == ModelCatalogTypes.DATA_TRANSFORMATION
