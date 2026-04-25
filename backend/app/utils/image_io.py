from __future__ import annotations

from pathlib import Path
from PIL import Image


def _convert_pdf_first_page(path: Path) -> Path:
    try:
        import pypdfium2 as pdfium
    except Exception as exc:  # pragma: no cover - optional dependency path
        raise ValueError(
            "PDF floorplans require pypdfium2. Install backend requirements and retry."
        ) from exc

    output_path = path.with_suffix(".png")
    pdf = pdfium.PdfDocument(str(path))
    page = pdf.get_page(0)
    bitmap = page.render(scale=2)
    pil_img = bitmap.to_pil()
    pil_img.save(output_path)
    page.close()
    pdf.close()
    return output_path


def ensure_image(path: Path) -> tuple[Path, int, int]:
    image_path = path
    if path.suffix.lower() == ".pdf":
        image_path = _convert_pdf_first_page(path)

    with Image.open(image_path) as img:
        width, height = img.size
    return image_path, width, height
