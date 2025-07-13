from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("tfl")

# Constants
TFL_API_BASE = "https://api.tfl.gov.uk"
USER_AGENT = "tfl-mcp/1.0"


async def make_tfl_request(resource: str, params: dict[str, Any] | None = None) -> dict[str, Any] | None:
    """Make a request to the TFL API with proper error handling."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{TFL_API_BASE}/{resource}", headers=headers, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return None


def format_status(statuses: list[dict[str, Any]]) -> str:
    """Format a status into a readable string."""

    line_statuses = []
    for status in statuses:
        line_statuses.append(f"## {status['name']}\n")
        line_statuses.append("")
        for line_status in status["lineStatuses"]:
            line_statuses.append(f"### {line_status['statusSeverityDescription']}\n")
            line_statuses.append(f"Reason: {line_status['reason']}")

            # Validity period
            validity_periods = line_status["validityPeriods"]
            if validity_periods:
                line_statuses.append(
                    f"Validity Period: {validity_periods[0]['fromDate']} to {validity_periods[0]['toDate']}"
                )
            else:
                line_statuses.append("No validity period")

            # Disruption type
            disruption = line_status["disruption"]
            line_statuses.append(f"Type: {disruption['categoryDescription']}")
            line_statuses.append(f"Description: {disruption['description']}")
            additional_info = disruption.get("additionalInfo", None)
            if additional_info:
                line_statuses.append(f"Additional Information: {additional_info}")

            line_statuses.append("")

    return "\n".join(line_statuses)


@mcp.tool()
async def get_line_status(lines: str) -> str:
    """Get status for a given TfL line identifier.

    The line identifier must be one of the following:
    - "bakerloo"
    - "central"
    - "circle"
    - "district"
    - "elizabeth-line"
    - "hammersmith-city"
    - "jubilee"
    - "metropolitan"
    - "northern"
    - "piccadilly"
    - "windrush""
    - "mildmay"
    - "victoria"
    - "waterloo-city"

    Args:
        lines: A comma-separated list of TfL line identifiers.
    """
    data = await make_tfl_request(f"line/{lines}/status")
    return format_status(data)


if __name__ == "__main__":
    mcp.run(transport="stdio")
