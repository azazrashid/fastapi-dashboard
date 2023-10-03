import subprocess
from datetime import datetime, timezone


def utcnow() -> datetime:
    """
    Returns the current time in UTC but with tzinfo set, as opposed
    to datetime.utcnow which does not.
    """
    return datetime.now(timezone.utc)


def get_month_abbr(month):
    """
    Get the abbreviated month name from a numeric month value (1-12).

    Args:
        month (int): Numeric month value (1-12).

    Returns:
        str: Abbreviated month name (e.g., 'Jan' for January).
    """
    month_abbr = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    return month_abbr[month - 1] if 1 <= month <= 12 else ""


def run_alembic_upgrade():
    try:
        # Use subprocess to run Alembic upgrade
        subprocess.run(["alembic", "upgrade", "head"])
    except Exception as e:
        print(f"Error running Alembic upgrade: {str(e)}")
