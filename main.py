
import httpx
from mcp.server.fastmcp import FastMCP
from tabulate import tabulate
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

mcp = FastMCP(
    "Crypto Funds MCP",
    dependencies=["httpx", "tabulate"],
)

@mcp.tool()
async def search_funds(
    tier: Optional[List[int]] = None,
    type: Optional[List[str]] = None,
    sortBy: str = "tier",
    sortDirection: str = "ASC",
    limit: int = 100,
    skip: int = 0
) -> str:
    """
    Fetch a sortable and filterable list of funds and investors with key metrics from Cryptorank API.
    Returns an ASCII table string of the data.

    Parameters:
    - tier: List of tier numbers (1-5) to filter by.
    - type: List of fund types (e.g., "Angel Investor", "Venture") to filter by.
    - sortBy: Field to sort by ("tier", "fundingRounds", "leadInvestments", "portfolio", "retailRoi").
    - sortDirection: Sort direction ("ASC" or "DESC").
    - limit: Number of results to return (100, 200, or 300).
    - skip: Number of results to skip.
    """
    api_key = os.getenv("CRYPTORANK_API_KEY")
    if not api_key:
        raise ValueError("CRYPTORANK_API_KEY environment variable is required in .env file.")

    url = "https://api.cryptorank.io/v2/funds"
    headers = {"X-Api-Key": api_key}
    params = {
        "sortBy": sortBy,
        "sortDirection": sortDirection,
        "limit": limit,
        "skip": skip
    }

    # Add optional filters if provided
    if tier:
        params["tier"] = tier
    if type:
        params["type"] = type

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Extract the 'data' field, which is the list of funds
            funds_data = data.get("data", [])

            if not funds_data:
                return "No funds data available for the specified filters."

            # Prepare data for table
            table_data = [
                {
                    "ID": fund.get("id", "N/A"),
                    "Key": fund.get("key", "N/A"),
                    "Name": fund.get("name", "N/A"),
                    "Tier": fund.get("tier", "N/A"),
                    "Type": fund.get("type", "N/A"),
                    "Jurisdiction": fund.get("jurisdiction", "N/A"),
                    "Portfolio": fund.get("portfolio", "N/A"),
                    "Funding Rounds": fund.get("fundingRounds", "N/A"),
                    "Retail ROI": fund.get("retailRoi", "N/A"),
                    "Lead Investments": fund.get("leadInvestments", "N/A"),
                }
                for fund in funds_data
            ]

            # Format as ASCII table
            return tabulate(
                table_data,
                headers="keys",
                tablefmt="grid",
                stralign="left",
                numalign="center",
            )
    except httpx.HTTPError as e:
        raise ValueError(f"Failed to fetch funds: {str(e)}") from e

@mcp.tool()
async def get_all_funds() -> str:
    """
    Fetch the complete list of investors and funds from Cryptorank API.
    Returns an ASCII table string of the data.
    """
    api_key = os.getenv("CRYPTORANK_API_KEY")
    if not api_key:
        raise ValueError("CRYPTORANK_API_KEY environment variable is required in .env file.")

    url = "https://api.cryptorank.io/v2/funds/map"
    headers = {"X-Api-Key": api_key}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Extract the 'data' field, which is the list of funds
            funds_data = data.get("data", [])

            if not funds_data:
                return "No funds data available."

            # Prepare data for table
            table_data = [
                {
                    "ID": fund.get("id", "N/A"),
#                    "Key": fund.get("key", "N/A"),
                    "Name": fund.get("name", "N/A"),
                    "Tier": fund.get("tier", "N/A"),
                    "Type": fund.get("type", "N/A"),
                }
                for fund in funds_data
            ]

            # Format as ASCII table
            return tabulate(
                table_data,
                headers="keys",
                tablefmt="grid",
                stralign="left",
                numalign="center",
            )
    except httpx.HTTPError as e:
        raise ValueError(f"Failed to fetch funds: {str(e)}") from e

@mcp.tool()
async def get_fund_basic(fund_id: int) -> str:
    """
    Fetch basic metrics for a specific fund by ID from Cryptorank API.
    Returns an ASCII table string of the fund metrics.
    """
    api_key = os.getenv("CRYPTORANK_API_KEY")
    if not api_key:
        raise ValueError("CRYPTORANK_API_KEY environment variable is required in .env file.")

    url = f"https://api.cryptorank.io/v2/funds/{fund_id}"
    headers = {"X-Api-Key": api_key}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Extract the 'data' field, which is a list with one fund
            fund_data = data.get("data", [])

            if not fund_data:
                return f"No data available for fund ID {fund_id}."

            fund = fund_data[0]

            # Prepare main fund metrics for table
            main_table_data = [
                {
                    "Field": "ID",
                    "Value": fund.get("id", "N/A"),
                },
                {
                    "Field": "Key",
                    "Value": fund.get("key", "N/A"),
                },
                {
                    "Field": "Name",
                    "Value": fund.get("name", "N/A"),
                },
                {
                    "Field": "Tier",
                    "Value": fund.get("tier", "N/A"),
                },
                {
                    "Field": "Type",
                    "Value": fund.get("type", "N/A"),
                },
                {
                    "Field": "Jurisdiction",
                    "Value": fund.get("jurisdiction", "N/A"),
                },
                {
                    "Field": "Portfolio",
                    "Value": fund.get("portfolio", "N/A"),
                },
                {
                    "Field": "Funding Rounds",
                    "Value": fund.get("fundingRounds", "N/A"),
                },
                {
                    "Field": "Retail ROI",
                    "Value": fund.get("retailRoi", "N/A"),
                },
                {
                    "Field": "Lead Investments",
                    "Value": fund.get("leadInvestments", "N/A"),
                },
            ]

            # Prepare focus areas table
            focus_areas = fund.get("focusArea", [])
            focus_table_data = [
                {
                    "ID": area.get("id", "N/A"),
                    "Name": area.get("name", "N/A"),
                    "Percent": area.get("percent", "N/A"),
                }
                for area in focus_areas
            ]

            # Prepare top investments table
            top_investments = fund.get("topInvestments", [])
            investments_table_data = [
                {
                    "ID": inv.get("id", "N/A"),
                    "Symbol": inv.get("symbol", "N/A"),
                    "Name": inv.get("name", "N/A"),
                    "Logo": inv.get("logo", "N/A"),
                }
                for inv in top_investments
            ]

            # Combine all tables into a single string
            output = "Fund Metrics:\n"
            output += tabulate(
                main_table_data,
                headers="keys",
                tablefmt="grid",
                stralign="left",
                numalign="center",
            )

            if focus_table_data:
                output += "\n\nFocus Areas:\n"
                output += tabulate(
                    focus_table_data,
                    headers="keys",
                    tablefmt="grid",
                    stralign="left",
                    numalign="center",
                )

            if investments_table_data:
                output += "\n\nTop Investments (Last 12 Months):\n"
                output += tabulate(
                    investments_table_data,
                    headers="keys",
                    tablefmt="grid",
                    stralign="left",
                    numalign="center",
                )

            return output
    except httpx.HTTPError as e:
        raise ValueError(f"Failed to fetch metrics for fund ID {fund_id}: {str(e)}") from e

@mcp.tool()
async def get_fund_detail(fund_id: int) -> str:
    """
    Fetch comprehensive metrics and investment data for a specific fund by ID from Cryptorank API.
    Returns an ASCII table string of the fund data.
    """
    api_key = os.getenv("CRYPTORANK_API_KEY")
    if not api_key:
        raise ValueError("CRYPTORANK_API_KEY environment variable is required in .env file.")

    url = f"https://api.cryptorank.io/v2/funds/{fund_id}/full-metadata"
    headers = {"X-Api-Key": api_key}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Extract the 'data' field, which contains the fund details
            fund = data.get("data", {})

            if not fund:
                return f"No data available for fund ID {fund_id}."

            # Prepare main fund metrics for table
            main_table_data = [
                {"Field": "ID", "Value": fund.get("id", "N/A")},
                {"Field": "Key", "Value": fund.get("key", "N/A")},
                {"Field": "Name", "Value": fund.get("name", "N/A")},
                {"Field": "Tier", "Value": fund.get("tier", "N/A")},
                {"Field": "Type", "Value": fund.get("type", "N/A")},
                {"Field": "Jurisdiction", "Value": fund.get("jurisdiction", "N/A")},
                {"Field": "Description", "Value": fund.get("description", "N/A")},
                {"Field": "Portfolio", "Value": fund.get("portfolio", "N/A")},
                {"Field": "Funding Rounds", "Value": fund.get("fundingRounds", "N/A")},
                {"Field": "Retail ROI", "Value": fund.get("retailRoi", "N/A")},
                {"Field": "Lead Investments", "Value": fund.get("leadInvestments", "N/A")},
            ]

            # Prepare links table
            links = fund.get("links", [])
            links_table_data = [
                {
                    "Type": link.get("type", "N/A"),
                    "Value": link.get("value", "N/A"),
                }
                for link in links
            ]

            # Prepare focus areas table
            focus_areas = fund.get("focusArea", [])
            focus_table_data = [
                {
                    "ID": area.get("id", "N/A"),
                    "Name": area.get("name", "N/A"),
                    "Percent": area.get("percent", "N/A"),
                }
                for area in focus_areas
            ]

            # Prepare top investments table
            top_investments = fund.get("topInvestments", [])
            investments_table_data = [
                {
                    "ID": inv.get("id", "N/A"),
                    "Symbol": inv.get("symbol", "N/A"),
                    "Name": inv.get("name", "N/A"),
                    "Logo": inv.get("logo", "N/A"),
                }
                for inv in top_investments
            ]

            # Prepare funding locations table
            funding_locations = fund.get("fundingLocations", [])
            locations_table_data = [
                {
                    "Code": loc.get("code", "N/A"),
                    "Count": loc.get("count", "N/A"),
                }
                for loc in funding_locations
            ]

            # Prepare recent rounds table
            recent_rounds = fund.get("recentRounds", [])
            rounds_table_data = [
                {
                    "ID": round.get("id", "N/A"),
                    "Name": round.get("name", "N/A"),
                    "Logo": round.get("logo", "N/A"),
                    "Raise": round.get("raise", "N/A"),
                    "Date": round.get("date", "N/A"),
                }
                for round in recent_rounds
            ]

            # Prepare average rounds raise table
            avg_rounds_raise = fund.get("avgRoundsRaise", [])
            avg_raise_table_data = [
                {
                    "Raise From": raise_data.get("raiseFrom", "N/A"),
                    "Raise To": raise_data.get("raiseTo", "N/A"),
                    "Percent": raise_data.get("percent", "N/A"),
                }
                for raise_data in avg_rounds_raise
            ]

            # Prepare investment stages table
            investment_stages = fund.get("investmentStages", [])
            stages_table_data = [
                {
                    "Type": stage.get("type", ["N/A"])[0] if stage.get("type") else "N/A",
                    "Percent": stage.get("percent", "N/A"),
                }
                for stage in investment_stages
            ]

            # Combine all tables into a single string
            output = "Comprehensive Fund Data:\n"
            output += tabulate(
                main_table_data,
                headers="keys",
                tablefmt="grid",
                stralign="left",
                numalign="center",
            )

            if links_table_data:
                output += "\n\nLinks:\n"
                output += tabulate(
                    links_table_data,
                    headers="keys",
                    tablefmt="grid",
                    stralign="left",
                    numalign="center",
                )

            if focus_table_data:
                output += "\n\nFocus Areas:\n"
                output += tabulate(
                    focus_table_data,
                    headers="keys",
                    tablefmt="grid",
                    stralign="left",
                    numalign="center",
                )

            if investments_table_data:
                output += "\n\nTop Investments (Recent):\n"
                output += tabulate(
                    investments_table_data,
                    headers="keys",
                    tablefmt="grid",
                    stralign="left",
                    numalign="center",
                )

            if locations_table_data:
                output += "\n\nFunding Locations:\n"
                output += tabulate(
                    locations_table_data,
                    headers="keys",
                    tablefmt="grid",
                    stralign="left",
                    numalign="center",
                )

            if rounds_table_data:
                output += "\n\nRecent Funding Rounds:\n"
                output += tabulate(
                    rounds_table_data,
                    headers="keys",
                    tablefmt="grid",
                    stralign="left",
                    numalign="center",
                )

            if avg_raise_table_data:
                output += "\n\nAverage Rounds Raise:\n"
                output += tabulate(
                    avg_raise_table_data,
                    headers="keys",
                    tablefmt="grid",
                    stralign="left",
                    numalign="center",
                )

            if stages_table_data:
                output += "\n\nInvestment Stages:\n"
                output += tabulate(
                    stages_table_data,
                    headers="keys",
                    tablefmt="grid",
                    stralign="left",
                    numalign="center",
                )

            return output
    except httpx.HTTPError as e:
        raise ValueError(f"Failed to fetch comprehensive data for fund ID {fund_id}: {str(e)}") from e
        


@mcp.tool()
async def get_fund_team(fund_id: int) -> str:
    """
    Fetch detailed team information for a specific fund by ID from Cryptorank API.
    Returns an ASCII table string of the team data.
    """
    api_key = os.getenv("CRYPTORANK_API_KEY")
    if not api_key:
        raise ValueError("CRYPTORANK_API_KEY environment variable is required in .env file.")

    url = f"https://api.cryptorank.io/v2/funds/{fund_id}/team"
    headers = {"X-Api-Key": api_key}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Extract the 'data' field, which contains the team details
            team_data = data.get("data", [])

            if not team_data:
                return f"No team data available for fund ID {fund_id}."

            # Prepare team table
            team_table_data = [
                {
                    "ID": member.get("id", "N/A"),
                    "Name": member.get("name", "N/A"),
                    "Jobs": ", ".join(member.get("jobs", ["N/A"])),
                    "Priority": member.get("priority", "N/A"),
                }
                for member in team_data
            ]

            # Prepare links table
            links_table_data = []
            for member in team_data:
                member_name = member.get("name", "N/A")
                for link in member.get("links", []):
                    links_table_data.append({
                        "Member Name": member_name,
                        "Link Type": link.get("type", "N/A"),
                        "Link Value": link.get("value", "N/A"),
                    })

            # Combine tables into a single string
            output = "Fund Team Details:\n"
            output += tabulate(
                team_table_data,
                headers="keys",
                tablefmt="grid",
                stralign="left",
                numalign="center",
            )

            if links_table_data:
                output += "\n\nTeam Social Links:\n"
                output += tabulate(
                    links_table_data,
                    headers="keys",
                    tablefmt="grid",
                    stralign="left",
                    numalign="center",
                )

            return output
    except httpx.HTTPError as e:
        raise ValueError(f"Failed to fetch team data for fund ID {fund_id}: {str(e)}") from e
        

if __name__ == "__main__":
    mcp.run()
