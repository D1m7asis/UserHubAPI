import logging
from pathlib import Path

from litestar import Controller, get, MediaType

logger = logging.getLogger("app")


class SystemController(Controller):
    @get("/", media_type=MediaType.HTML, include_in_schema=False)
    async def index(self) -> str:
        """Главная страница с приветственной документацией"""
        logger.debug("Accessing index page")
        template_path = Path(__file__).parent.parent / "templates" / "index.html"

        try:
            html_content = template_path.read_text(encoding="utf-8")
            logger.debug("Index page loaded successfully")
            return html_content
        except Exception as e:
            logger.error(f"Failed to load index page: {e}", exc_info=True)
            raise Exception("Failed to load the index page")
