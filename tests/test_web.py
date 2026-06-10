import importlib.util
from pathlib import Path


def _load_app_module():
    root = Path(__file__).resolve().parents[1]
    app_path = root / "apps" / "web" / "app.py"
    spec = importlib.util.spec_from_file_location("demo_web_app", app_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_demo_routes_return_success():
    module = _load_app_module()
    client = module.APP.test_client()
    for path in ["/", "/sources", "/sources/src_pdf_01", "/deliverables/brief", "/deliverables/literature_matrix", "/deliverables/slides", "/traces/trc_brief_summary_01"]:
        response = client.get(path)
        assert response.status_code == 200


def test_homepage_includes_bilingual_messaging_and_visual_asset():
    module = _load_app_module()
    client = module.APP.test_client()
    response = client.get("/")
    html = response.get_data(as_text=True)
    assert "Turn messy sources into cited deliverables." in html
    assert "把杂乱资料变成带引用、可直接交付的成果。" in html
    assert "hero-workbench.svg" in html
