"""
存档读写
"""

import json
import os

from game.settings import SAVE_FILE


def has_save():
    return os.path.exists(SAVE_FILE)


def delete_save():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)


def write_save(level_index, elapsed_ms, mistakes, arrows):
    """写入存档

    arrows: Arrow 对象列表（只保存静止的）
    """

    arrow_data = []

    for arrow in arrows:
        if not arrow.flying:
            arrow_data.append({
                "row": arrow.row,
                "col": arrow.col,
                "direction": arrow.direction,
            })

    data = {
        "level_index": level_index,
        "elapsed_ms": elapsed_ms,
        "mistakes": mistakes,
        "arrows": arrow_data,
    }

    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_save():

    if not has_save():
        return None

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None