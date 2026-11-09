
import json
from pathlib import Path

CATALOG_FILE = Path(__file__).with_name(
    "capabilities.json"
)

VALID_CATEGORIES = {
    "ai_automation",
    "cloud_infrastructure",
    "data_analytics",
    "enterprise_integration",
    "all"
}


def lookup_service_capabilities(category: str) -> dict:
    """
    Retrieve example capabilities by category.
    """

    if category not in VALID_CATEGORIES:
        raise ValueError(
            f"Unsupported category: {category}"
        )

    with CATALOG_FILE.open(
        "r", encoding="utf-8"
    ) as file:
        catalog = json.load(file)

    if category == "all":
        matches = catalog
    else:
        matches = [
            item for item in catalog
            if item["category"] == category
        ]

    return {
        "notice": "Illustrative catalog only.",
        "category": category,
        "capabilities": matches
    }