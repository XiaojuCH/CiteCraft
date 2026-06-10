from pathlib import Path

from workbench.pipeline.run import run_project, write_outputs


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOTS = [
    ROOT / "examples" / "academia" / "demo-01",
    ROOT / "examples" / "research" / "demo-01",
]


def test_demo_project_generates_all_deliverables(tmp_path):
    for project_root in PROJECT_ROOTS:
        run = run_project(project_root)
        assert set(run.deliverables.keys()) == {"brief", "literature_matrix", "slides"}
        assert run.documents

        output_dir = tmp_path / project_root.parent.name
        write_outputs(run, output_dir)
        assert (output_dir / "brief.json").exists()
        assert (output_dir / "literature_matrix.md").exists()
        assert (output_dir / "slides.html").exists()


def test_factual_matrix_cells_have_traces():
    for project_root in PROJECT_ROOTS:
        run = run_project(project_root)
        matrix = run.deliverables["literature_matrix"]
        factual_cells = [cell for cell in matrix.cells if cell.value and cell.is_factual]
        assert factual_cells
        assert all(cell.trace_refs for cell in factual_cells)


def test_claim_bullets_have_traces():
    for project_root in PROJECT_ROOTS:
        run = run_project(project_root)
        slides = run.deliverables["slides"]
        claim_bullets = [
            bullet
            for slide in slides.slides
            for bullet in slide.bullets
            if bullet.kind == "claim"
        ]
        assert claim_bullets
        assert all(bullet.trace_refs for bullet in claim_bullets)
