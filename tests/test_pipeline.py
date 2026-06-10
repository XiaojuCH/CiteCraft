from pathlib import Path

from workbench.pipeline.run import run_project, write_outputs


PROJECT_ROOT = Path(__file__).resolve().parents[1] / "examples" / "academia" / "demo-01"


def test_demo_project_generates_all_deliverables(tmp_path):
    run = run_project(PROJECT_ROOT)
    assert set(run.deliverables.keys()) == {"brief", "literature_matrix", "slides"}
    assert run.project.project_id == "demo-01"
    assert run.documents

    write_outputs(run, tmp_path)
    assert (tmp_path / "brief.json").exists()
    assert (tmp_path / "literature_matrix.md").exists()
    assert (tmp_path / "slides.html").exists()


def test_factual_matrix_cells_have_traces():
    run = run_project(PROJECT_ROOT)
    matrix = run.deliverables["literature_matrix"]
    factual_cells = [cell for cell in matrix.cells if cell.value and cell.is_factual]
    assert factual_cells
    assert all(cell.trace_refs for cell in factual_cells)


def test_claim_bullets_have_traces():
    run = run_project(PROJECT_ROOT)
    slides = run.deliverables["slides"]
    claim_bullets = [
        bullet
        for slide in slides.slides
        for bullet in slide.bullets
        if bullet.kind == "claim"
    ]
    assert claim_bullets
    assert all(bullet.trace_refs for bullet in claim_bullets)
