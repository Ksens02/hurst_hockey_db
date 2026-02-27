from typing import List, Optional
import csv
import os

from models import Stats


def _int(val: Optional[str]) -> Optional[int]:
    if val is None:
        return None
    s = val.strip()
    if s == "":
        return None
    try:
        return int(s)
    except ValueError:
        return None


def _float(val: Optional[str]) -> Optional[float]:
    if val is None:
        return None
    s = val.strip()
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def generate_stats_instances(csv_path: str | None = None) -> List[Stats]:
    """Read `csv_path` (defaults to ./stats.csv) and return a list of `Stats` instances."""
    if csv_path is None:
        csv_path = os.path.join(os.path.dirname(__file__), "stats.csv")

    instances: List[Stats] = []
    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            # normalize keys to lowercase for flexible column names
            norm = {(k or "").lower(): (v or "").strip() for k, v in row.items()}

            first = norm.get("first_name") or norm.get("first") or ""
            last = norm.get("last_name") or norm.get("last") or ""

            number = _int(norm.get("number"))

            stat = Stats(
                first_name=first,
                last_name=last,
                number=number,
                gp=_int(norm.get("gp")),
                g=_int(norm.get("g")),
                a=_int(norm.get("a")),
                pts=_int(norm.get("pts")),
                sh=_int(norm.get("sh")),
                sh_pct=_float(norm.get("sh_pct")),
                plus_minus=_int(norm.get("plus_minus")),
                ppg=_int(norm.get("ppg")),
                shg=_int(norm.get("shg")),
                fg=_int(norm.get("fg")),
                gwg=_int(norm.get("gwg")),
                gtg=_int(norm.get("gtg")),
                otg=_int(norm.get("otg")),
                htg=_int(norm.get("htg")),
                uag=_int(norm.get("uag")),
                pn_pim=norm.get("pn-pim") or norm.get("pn_pim") or None,
                minutes=_int(norm.get("min")) or _int(norm.get("minutes")),
                maj=_int(norm.get("maj")),
                oth=_int(norm.get("oth")),
                blk=_int(norm.get("blk")),
            )
            instances.append(stat)

    return instances


__all__ = ["generate_stats_instances"]
