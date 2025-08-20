from __future__ import annotations
import logging
import faulthandler
import os
import sys
from pathlib import Path
from typing import Optional


def setup_debug_logging(log_path: Optional[str] = None) -> Path:
    """Configure debug logging and crash reports.

    Parameters
    ----------
    log_path:
        Optional path to log file. If not provided, ``saplings_debug.log``
        will be created in the current working directory.

    Returns
    -------
    Path
        Path to the log file used.
    """
    log_file = Path(log_path or "saplings_debug.log")
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # открываем файл и включаем faulthandler для захвата нативных падений
    fh = open(log_file, "a", encoding="utf-8")
    faulthandler.enable(fh)

    logging.basicConfig(
        level=logging.DEBUG,
        filename=str(log_file),
        filemode="a",
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    def _excepthook(exc_type, exc, tb):
        logging.exception("Uncaught exception", exc_info=(exc_type, exc, tb))

    # перехватываем необработанные исключения
    sys.excepthook = _excepthook

    # выводим дополнительные сообщения Qt о загрузке плагинов
    os.environ.setdefault("QT_DEBUG_PLUGINS", "1")

    logging.debug("Debug logging initialized")
    return log_file
