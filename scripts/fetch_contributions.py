# =============================================================================
# fetch_contributions.py — scrape GitHub contribution heatmap -> JSON
# No token or GraphQL required; uses the public HTML activity page.
# Note: GitHub's static HTML only exposes data-level (0-4), not raw counts.
# We map level -> representative count for heatmap coloring purposes.
# =============================================================================
import json
import sys
from datetime import date, timedelta
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import requests
from bs4 import BeautifulSoup

from utils import repo_path

# ---------------------------------------------------------------------------
USERNAME = "akshitap30"
URL = f"https://github.com/users/{USERNAME}/contributions"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; profile-readme-bot/1.0; "
        "+https://github.com/akshitap30)"
    ),
    "X-Requested-With": "XMLHttpRequest",
}
OUTPUT = repo_path("data", "contributions.json")

# Map GitHub's data-level (0-4) -> representative count for palette mapping.
# Level 0 = no activity; 1-4 = increasingly active.
LEVEL_TO_COUNT = {
    "0": 0,
    "1": 2,    # maps to palette[1]: 1-3 contributions
    "2": 6,    # maps to palette[2]: 4-9
    "3": 15,   # maps to palette[3]: 10-19
    "4": 30,   # maps to palette[4]: 20-49
}
# ---------------------------------------------------------------------------


def fetch_html() -> str:
    resp = requests.get(URL, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.text


def parse_contributions(html: str) -> dict:
    """Parse the contribution calendar HTML -> {date_str: count} dict.

    GitHub's static HTML only has data-level (0-4) -- not raw counts.
    We convert level -> representative count so the heatmap palette
    renders correctly.
    """
    soup = BeautifulSoup(html, "html.parser")

    daily: dict[str, int] = {}
    for td in soup.find_all("td", attrs={"data-date": True}):
        day_str = td["data-date"]
        level   = td.get("data-level", "0")
        daily[day_str] = LEVEL_TO_COUNT.get(level, 0)

    if not daily:
        print("WARNING: No contribution cells found -- check if GitHub changed markup.")

    return daily


def compute_stats(daily: dict[str, int]) -> dict:
    """Derive streaks, best day, and monthly totals from daily counts."""
    if not daily:
        return {}

    sorted_days = sorted(daily.keys())
    counts = [daily[d] for d in sorted_days]

    # Current streak (from today backwards)
    today = date.today()
    current_streak = 0
    d = today
    skip_today_once = True   # grace: today may not be committed yet
    while True:
        ds = d.isoformat()
        c = daily.get(ds, 0)
        if c > 0:
            current_streak += 1
            d -= timedelta(days=1)
            skip_today_once = False
        elif skip_today_once:
            skip_today_once = False
            d -= timedelta(days=1)
        else:
            break

    # Longest streak
    longest_streak = 0
    streak = 0
    for c in counts:
        if c > 0:
            streak += 1
            longest_streak = max(longest_streak, streak)
        else:
            streak = 0

    # Best single day (by level-mapped count)
    best_day_date  = max(daily, key=daily.get)
    best_day_level = daily[best_day_date]

    # Monthly totals
    monthly: dict[str, int] = {}
    for day_str, cnt in daily.items():
        ym = day_str[:7]   # "YYYY-MM"
        monthly[ym] = monthly.get(ym, 0) + cnt

    active_days = sum(1 for c in counts if c > 0)

    return {
        "total_active_days": active_days,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": {"date": best_day_date, "level": best_day_level},
        "monthly_totals": monthly,
    }


def main():
    print(f"Fetching {URL} ...")
    html = fetch_html()

    daily = parse_contributions(html)
    print(f"  Parsed {len(daily)} days.")

    stats = compute_stats(daily)
    print(
        f"  Active days: {stats.get('total_active_days', 0)}  |  "
        f"Current streak: {stats.get('current_streak', 0)}  |  "
        f"Longest: {stats.get('longest_streak', 0)}"
    )

    payload = {
        "username": USERNAME,
        "fetched_at": date.today().isoformat(),
        "note": "data-level used (0-4); GitHub JS hides raw counts from static HTML",
        "daily": daily,
        "stats": stats,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Written -> {OUTPUT}")


if __name__ == "__main__":
    main()
