"""
Unit Tests for Mandatory PDF Deliverables
------------------------------------------
STRICT BRIEF REQUIREMENT:
'Content beyond one page will not be read.'

Validates:
1. docs/architecture.pdf exists and has page_count == 1.
2. docs/solution_overview.pdf exists and has page_count == 1.
"""

from pathlib import Path
import pypdf
import pytest

from src.generate_docs import generate_all_docs


@pytest.fixture(scope="module", autouse=True)
def ensure_docs_generated():
    arch_pdf = Path("docs/architecture.pdf")
    sol_pdf = Path("docs/solution_overview.pdf")
    if not arch_pdf.exists() or not sol_pdf.exists():
        generate_all_docs()


def test_architecture_pdf_strictly_one_page():
    """Asserts that docs/architecture.pdf is exactly 1 page."""
    pdf_path = Path("docs/architecture.pdf")
    assert pdf_path.exists(), "docs/architecture.pdf does not exist."
    reader = pypdf.PdfReader(str(pdf_path))
    assert len(reader.pages) == 1, f"architecture.pdf has {len(reader.pages)} pages (must be exactly 1)."


def test_solution_overview_pdf_strictly_one_page():
    """Asserts that docs/solution_overview.pdf is exactly 1 page."""
    pdf_path = Path("docs/solution_overview.pdf")
    assert pdf_path.exists(), "docs/solution_overview.pdf does not exist."
    reader = pypdf.PdfReader(str(pdf_path))
    assert len(reader.pages) == 1, f"solution_overview.pdf has {len(reader.pages)} pages (must be exactly 1)."
