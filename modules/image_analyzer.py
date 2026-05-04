from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)

try:
    import pyewf  # type: ignore
except ImportError:  # pragma: no cover
    pyewf = None

try:
    import pytsk3  # type: ignore
except ImportError:  # pragma: no cover
    pytsk3 = None


class ImageAnalyzer:
    def detect_format(self, image_path: str | Path) -> str:
        path = Path(image_path)
        suffix = path.suffix.lower()
        if suffix == ".e01":
            return "E01"
        return "RAW"

    def summarize_image(self, image_path: str | Path) -> dict[str, Any]:
        path = Path(image_path)
        return {
            "path": str(path),
            "format": self.detect_format(path),
            "size": path.stat().st_size if path.exists() else 0,
            "read_only": True,
            "mountless": True,
            "pyewf_available": pyewf is not None,
            "pytsk3_available": pytsk3 is not None,
        }

    def enumerate_filesystem_roots(self, image_path: str | Path) -> list[str]:
        summary = self.summarize_image(image_path)
        LOGGER.info("Image summary: %s", summary)
        return [str(image_path)]
