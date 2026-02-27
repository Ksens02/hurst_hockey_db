import csv
import os
from typing import List

from models import Bio


def generate_bio_instances(csv_path: str | None = None) -> List[Bio]:
    """Read the roster CSV and return a list of `Bio` instances.

    The function looks for `roster.csv` next to this file by default.
    """
    if csv_path is None:
        csv_path = os.path.join(os.path.dirname(__file__), "roster.csv")

    bios: List[Bio] = []
    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            # Skip empty rows
            first = (row.get("first_name") or "").strip()
            last = (row.get("last_name") or "").strip()
            if not (first or last):
                continue

            number_raw = (row.get("number") or "").strip()
            number = int(number_raw) if number_raw else None

            weight_raw = (row.get("weight") or "").strip()
            weight = int(weight_raw) if weight_raw else None

            position = (row.get("position") or "").strip() or None
            height = (row.get("height") or "").strip() or None
            hometown = (row.get("hometown") or "").strip() or None
            academic_class = (row.get("class") or "").strip() or None
            high_school = (row.get("high_school") or "").strip() or None

            bio = Bio(
                first_name=first,
                last_name=last,
                number=number,
                position=position,
                height=height,
                weight=weight,
                academic_class=academic_class,
                hometown=hometown,
                high_school=high_school,
            )
            bios.append(bio)

    return bios


__all__ = ["generate_bio_instances"]
