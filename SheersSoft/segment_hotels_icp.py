import csv
from pathlib import Path


INPUT_FILE = Path("MAH_Members_Complete_2025.csv")


def normalize_category(raw: str) -> str:
    if not raw:
        return ""
    value = raw.strip().lower()
    # Normalize common variants
    replacements = {
        "5 star": "5 Star",
        "4 star": "4 Star",
        "3 star": "3 Star",
        "2 star": "2 Star",
        "1 star": "1 Star",
        "associate": "Associate",
        "orchid": "Orchid",
        "others": "Others",
    }
    # Return canonical capitalization when matched
    return replacements.get(value, raw.strip())


def to_int_or_none(value: str):
    if value is None:
        return None
    s = str(value).strip()
    if s == "":
        return None
    # Keep only leading digits
    digits = []
    for ch in s:
        if ch.isdigit():
            digits.append(ch)
        else:
            # stop at first non-digit (handles things like "123 rooms")
            break
    if not digits:
        return None
    try:
        return int("".join(digits))
    except ValueError:
        return None


def classify_icp(category: str, rooms: int | None) -> str:
    cat = normalize_category(category)
    # Primary ICPs per user brief
    if cat in {"4 Star", "5 Star"} and (rooms is not None and rooms > 100):
        return "ICP_High_Value_Prospect"
    if cat == "Associate":
        return "ICP_Associate_Partner"

    # Additional useful ICPs for an IT systems integrator
    if cat == "3 Star" and (rooms is not None and rooms >= 80):
        return "ICP_Mid_Tier_Prospect"
    if cat in {"4 Star", "5 Star"} and (rooms is not None and rooms <= 100):
        return "ICP_Boutique_Luxury"
    if cat in {"1 Star", "2 Star", "Orchid", "Others"}:
        # Distinguish a bit by size
        if rooms is not None and rooms > 60:
            return "ICP_Budget_Large"
        return "ICP_Budget_Small"

    # Fallback buckets
    if rooms is not None and rooms <= 40:
        return "ICP_Small_Property"
    if rooms is None or not cat:
        return "ICP_Unknown"
    return "ICP_Other"


def main():
    if not INPUT_FILE.exists():
        raise SystemExit(f"Input file not found: {INPUT_FILE}")

    with INPUT_FILE.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Ensure expected columns exist
    expected_cols = {"unique_id", "name", "membership_number", "state", "category", "rooms", "address", "phone", "email", "website"}
    missing = [c for c in expected_cols if c not in reader.fieldnames]
    if missing:
        raise SystemExit(f"Missing expected columns: {missing}")

    enriched_rows = []
    for row in rows:
        rooms = to_int_or_none(row.get("rooms"))
        category = row.get("category", "")
        icp = classify_icp(category, rooms)
        out = dict(row)
        out["icp_segment"] = icp
        out["category_normalized"] = normalize_category(category)
        out["rooms_int"] = rooms if rooms is not None else ""
        enriched_rows.append(out)

    # Write master segmented file
    master_path = Path("Hotels_ICP_Segmented_Master_v2.csv")
    fieldnames = list(enriched_rows[0].keys()) if enriched_rows else reader.fieldnames + ["icp_segment", "category_normalized", "rooms_int"]
    with master_path.open("w", newline="", encoding="utf-8") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(enriched_rows)

    # Prepare per-segment outputs
    segments = {
        "ICP_High_Value_Prospect": Path("Hotels_ICP_High_Value_Prospects_v2.csv"),
        "ICP_Associate_Partner": Path("Hotels_ICP_Associate_Partners_v2.csv"),
        "ICP_Mid_Tier_Prospect": Path("Hotels_ICP_Mid_Tier_Prospects_v2.csv"),
        "ICP_Boutique_Luxury": Path("Hotels_ICP_Boutique_Luxury_v2.csv"),
        "ICP_Budget_Large": Path("Hotels_ICP_Budget_Large_v2.csv"),
        "ICP_Budget_Small": Path("Hotels_ICP_Budget_Small_v2.csv"),
        "ICP_Small_Property": Path("Hotels_ICP_Small_Properties_v2.csv"),
        "ICP_Other": Path("Hotels_ICP_Other_v2.csv"),
        "ICP_Unknown": Path("Hotels_ICP_Unknown_v2.csv"),
    }

    counts: dict[str, int] = {seg: 0 for seg in segments}
    # Group and write each segment
    for seg, path in segments.items():
        seg_rows = [r for r in enriched_rows if r["icp_segment"] == seg]
        counts[seg] = len(seg_rows)
        if not seg_rows:
            # Still write header for visibility
            with path.open("w", newline="", encoding="utf-8") as f_out:
                writer = csv.DictWriter(f_out, fieldnames=fieldnames)
                writer.writeheader()
            continue
        with path.open("w", newline="", encoding="utf-8") as f_out:
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(seg_rows)

    # Write a simple markdown summary
    summary_path = Path("ICP_SEGMENT_SUMMARY_v2.md")
    with summary_path.open("w", encoding="utf-8") as f_md:
        f_md.write("# ICP Segment Summary\n\n")
        total = len(enriched_rows)
        f_md.write(f"Total records: {total}\n\n")
        # Order with the two primary ICPs first
        order = [
            "ICP_High_Value_Prospect",
            "ICP_Associate_Partner",
            "ICP_Mid_Tier_Prospect",
            "ICP_Boutique_Luxury",
            "ICP_Budget_Large",
            "ICP_Budget_Small",
            "ICP_Small_Property",
            "ICP_Other",
            "ICP_Unknown",
        ]
        for seg in order:
            f_md.write(f"- {seg}: {counts.get(seg, 0)}\n")

    print("Wrote:")
    print(f" - {master_path}")
    for path in segments.values():
        print(f" - {path}")
    print(f" - {summary_path}")


if __name__ == "__main__":
    main()


