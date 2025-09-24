# Crypto Funds MCP

An MCP server that provides AI agents with structured, real-time data on cryptocurrency investment funds, enabling deeper due diligence and portfolio intelligence.

![GitHub License](https://img.shields.io/github/license/kukapay/crypto-funds-mcp) 
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## Features

- **Tools for Data Access**:
  - `get_all_funds()`: Retrieve a complete list of all investors and funds.
  - `search_funds(tier, type, sortBy, sortDirection, limit, skip)`: Search and filter funds with sorting and pagination.
  - `get_fund_basic(fund_id)`: Get basic metrics for a specific fund (e.g., tier, portfolio size, ROI).
  - `get_fund_full(fund_id)`: Fetch comprehensive metrics, including investment focus, recent rounds, and stages.
  - `get_fund_team(fund_id)`: Retrieve detailed team information with roles and social links.

- **Formatted Outputs**: All responses are returned as ASCII tables for easy readability in MCP clients.
- **Asynchronous API Calls**: Uses `httpx` for efficient, async HTTP requests.
- **Environment Configuration**: API key management via `.env` file with `dotenv`.
- **Error Handling**: Graceful handling of API errors and missing data.

## Installation

### Prerequisites

- Python 3.10+
- **uv**: Package and virtual environment manager for Python (recommended for dependency management).
- A Cryptorank API key (sign up at [Cryptorank](https://cryptorank.io/api))

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/kukapay/crypto-funds-mcp.git
   cd crypto-funds-mcp
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Create a `.env` file in the root directory and add your API key:
   ```
   CRYPTORANK_API_KEY=your_api_key_here
   ```

4. Install to Claude Desktop:

   Install the server as a Claude Desktop application:
   ```bash
   uv run mcp install main.py --name "Crypto Funds"
   ```

   Configuration file as a reference:

   ```json
   {
      "mcpServers": {
          "Crypto Funds": {
              "command": "uv",
              "args": [ "--directory", "/path/to/crypto-funds-mcp", "run", "main.py" ],
              "env": { "CRYPTORANK_API_KEY": "cryptorank_api_key"}
          }
      }
   }
   ```
   Replace `/path/to/crypto-funds-mcp` with your actual installation path, and replace `cryptorank_api_key` with your API key from Cryptorank.

## Usage

### Tool Usage Examples

Below are examples for each tool, including a natural language prompt (how you might ask an AI client to invoke it), the corresponding tool call, and a sample result (formatted as an ASCII table). Note that actual results depend on your Cryptorank API key and current data; these are illustrative examples based on public information.

#### get_all_funds()

**Prompt:** 
> Show me a complete list of all crypto investors and funds available.

**Tool Call:** 
```
get_all_funds()
```

**Example Result:**
```
+------+--------------------------------+--------+-------------+
|   ID | Name                           |   Tier | Type        |
+======+================================+========+=============+
|    1 | YZi Labs (Prev. Binance Labs)  |      1 | Venture     |
|    2 | Andreessen Horowitz (a16z)     |      1 | Venture     |
|    3 | Pantera Capital                |      1 | Venture     |
|    4 | Coinbase Ventures              |      1 | Venture     |
|    5 | Dragonfly Capital              |      1 | Venture     |
+------+--------------------------------+--------+-------------+
```

#### search_funds(tier, type, sortBy, sortDirection, limit, skip)

**Prompt:** 
> Search for Tier 1 Venture funds, sorted by retail ROI in descending order, and show the top 100 results.

**Tool Call:** 
```
search_funds(tier=[1], type=["Venture"], sortBy="retailRoi", sortDirection="DESC", limit=100, skip=0)
```

**Example Result:**
```
+------+--------------------------------+--------------------------------+--------+-------------+----------------+--------------------+-------------+--------------+-------------+--------------------+
|   ID | Key                            | Name                           |   Tier | Type        | Jurisdiction       | Portfolio   | Funding Rounds | Retail ROI  | Lead Investments   |
+======+================================+================================+========+=============+====================+=============+================+=============+====================+
|    1 | binance-labs                   | YZi Labs (Prev. Binance Labs)  |      1 | Venture     | Cayman Islands     | 200+        | 150+           | 500x        | 50+                |
|    2 | andreessen-horowitz            | Andreessen Horowitz (a16z)     |      1 | Venture     | United States      | 150+        | 120+           | 450x        | 40+                |
|    3 | pantera-capital                | Pantera Capital                |      1 | Venture     | United States      | 100+        | 90+            | 400x        | 30+                |
+------+--------------------------------+--------------------------------+--------+-------------+----------------+--------------------+-------------+--------------+-------------+--------------------+
```

#### get_fund_basic(fund_id)

**Natural Language Prompt:** 
> Give me the basic metrics for the fund with ID 1, like its tier, portfolio, and ROI.

**Tool Call:** 
```
get_fund_basic(1)
```

**Example Result:**
```
Fund Metrics:
+--------------------+-------------------------+
| Field              | Value                   |
+====================+=========================+
| ID                 | 1                       |
| Key                | binance-labs            |
| Name               | YZi Labs (Prev. Binance Labs) |
| Tier               | 1                       |
| Type               | Venture                 |
| Jurisdiction       | Cayman Islands          |
| Portfolio          | 200+                    |
| Funding Rounds     | 150+                    |
| Retail ROI         | 500x                    |
| Lead Investments   | 50+                     |
+--------------------+-------------------------+

Focus Areas:
+------+---------------+-----------+
|   ID | Name          | Percent   |
+======+===============+===========+
|   10 | DeFi          | 40%       |
|   20 | Web3          | 30%       |
|   30 | AI            | 20%       |
+------+---------------+-----------+

Top Investments (Last 12 Months):
+------+----------+----------------------+---------+
|   ID | Symbol   | Name                 | Logo    |
+======+==========+======================+=========+
| 1001 | APT      | Aptos                | url...  |
| 1002 | SUI      | Sui                  | url...  |
+------+----------+----------------------+---------+
```

#### get_fund_full(fund_id)

**Prompt:** 
> Provide comprehensive data and investment details for the fund with ID 2.

**Tool Call:** 
```
get_fund_full(2)
```

**Example Result:**
```
Comprehensive Fund Data:
+--------------------+---------------------------------+
| Field              | Value                           |
+====================+=================================+
| ID                 | 2                               |
| Key                | andreessen-horowitz             |
| Name               | Andreessen Horowitz (a16z)      |
| Tier               | 1                               |
| Type               | Venture                         |
| Jurisdiction       | United States                   |
| Description        | Leading VC in crypto and tech   |
| Portfolio          | 150+                            |
| Funding Rounds     | 120+                            |
| Retail ROI         | 450x                            |
| Lead Investments   | 40+                             |
+--------------------+---------------------------------+

Links:
+-----------+---------------------+
| Type      | Value               |
+===========+=====================+
| website   | https://a16z.com    |
| twitter   | https://x.com/a16z  |
+-----------+---------------------+

Focus Areas:
+------+---------------+-----------+
|   ID | Name          | Percent   |
+======+===============+===========+
|   10 | Blockchain    | 50%       |
|   20 | Gaming        | 25%       |
|   30 | Infrastructure| 25%       |
+------+---------------+-----------+

Top Investments (Recent):
+------+----------+----------------------+---------+
|   ID | Symbol   | Name                 | Logo    |
+======+==========+======================+=========+
| 2001 | FLOW     | Flow                 | url...  |
| 2002 | AXS      | Axie Infinity        | url...  |
+------+----------+----------------------+---------+

Funding Locations:
+---------+---------+
| Code    | Count   |
+=========+=========+
| US      | 80      |
| SG      | 20      |
+---------+---------+

Recent Funding Rounds:
+------+---------------+---------+---------+------------+
|   ID | Name          | Logo    | Raise   |     Date   |
+======+===============+=========+=========+============+
| 3001 | Project A     | url...  | $10M    | 2024-05-01 |
| 3002 | Project B     | url...  | $15M    | 2024-03-15 |
+------+---------------+---------+---------+------------+

Average Rounds Raise:
+----------------+--------------+-----------+
| Raise From     | Raise To     | Percent   |
+================+==============+===========+
| $1M            | $5M          | 40%       |
| $5M            | $20M         | 60%       |
+----------------+--------------+-----------+

Investment Stages:
+---------------+-----------+
| Type          | Percent   |
+===============+===========+
| Seed          | 50%       |
| Series A      | 30%       |
| Series B      | 20%       |
+---------------+-----------+
```

#### get_fund_team(fund_id)

**Prompt:** 
> Who is on the team for the fund with ID 3? Include their roles and social links.

**Tool Call:** 
```
get_fund_team(3)
```

**Example Result:**
```
Fund Team Details:
+------+--------------------+---------------------+------------+
|   ID | Name               | Jobs                |   Priority |
+======+====================+=====================+============+
|   11 | Paul Joey          | CEO, Founder        |          1 |
|   12 | Dan Larimer        | Managing Partner    |          2 |
|   13 | Jill Valentine     | Investment Director |          3 |
+------+--------------------+---------------------+------------+

Team Social Links:
+---------------------+--------------+---------------------+
| Member Name         | Link Type    | Link Value          |
+=====================+==============+=====================+
| Paul Joey           | linkedin     | https://linkedin... |
| Paul Joey           | twitter      | https://x.com/pjoey |
| Dan Larimer         | linkedin     | https://linkedin... |
+---------------------+--------------+---------------------+
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
