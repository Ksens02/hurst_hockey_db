from sqlmodel import SQLModel, Field

class Bio(SQLModel, table=True):
    first_name: str = Field(primary_key=True)
    last_name: str = Field(primary_key=True)
    number: int | None = None
    position: str | None = None
    height: str | None = None
    weight: int | None = None
    academic_class: str | None = None
    hometown: str | None = None
    high_school: str | None = None


class Stats(SQLModel, table=True):
    # Composite primary key linking to Bio
    first_name: str = Field(primary_key=True, foreign_key="bio.first_name")
    last_name: str = Field(primary_key=True, foreign_key="bio.last_name")

    # Basic identifiers
    number: int | None = None

    # Counting/stat columns
    gp: int | None = None
    g: int | None = None
    a: int | None = None
    pts: int | None = None

    # Shots and percentages
    sh: int | None = None
    sh_pct: float | None = None

    # Plus/minus
    plus_minus: int | None = None

    # Goal types / special stats
    ppg: int | None = None
    shg: int | None = None
    fg: int | None = None
    gwg: int | None = None
    gtg: int | None = None
    otg: int | None = None
    htg: int | None = None
    uag: int | None = None

    # Penalties (kept as string because format is e.g. "7-22")
    pn_pim: str | None = None

    # Time and misc
    minutes: int | None = None
    maj: int | None = None
    oth: int | None = None
    blk: int | None = None