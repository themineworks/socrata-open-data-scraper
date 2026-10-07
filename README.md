# Socrata Open Data API Scraper: CDC, NYC, Gov Data (No Key)

Search and pull datasets from any Socrata-powered government open-data portal: CDC, HHS, CMS, NY, NYC, Texas, and hundreds more. Discovery search plus SoQL-filtered data pull. Structured JSON, no anti-bot measures.

**Run it on Apify:** [apify.com/themineworks/socrata-open-data](https://apify.com/themineworks/socrata-open-data)
**Docs, FAQ and pricing:** [themineworks.com/actors/socrata-open-data](https://themineworks.com/actors/socrata-open-data/)

**Price:** From $0.60 per 1,000 records on Apify's higher plans ($1.00 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged.

## What it returns

* CDC, HHS, CMS, NYC, Texas and 200+ portals
* Discovery search across all datasets
* SoQL filtering for precise data pulls
* Structured JSON output, no authentication
* Empty results are never charged

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/socrata-open-data").call(run_input={
    "searchQuery": "covid deaths",
    "domain": "data.cdc.gov",
    "datasetId": "9bhg-hcku",
    "where": "state='New York' AND covid_19_deaths > 100"
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/socrata-open-data').call({
    "searchQuery": "covid deaths",
    "domain": "data.cdc.gov",
    "datasetId": "9bhg-hcku",
    "where": "state='New York' AND covid_19_deaths > 100"
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~socrata-open-data/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchQuery": "covid deaths", "domain": "data.cdc.gov", "datasetId": "9bhg-hcku", "where": "state='\''New York'\'' AND covid_19_deaths > 100"}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 socrata_open_data_scraper.py --token YOUR_APIFY_TOKEN --search-query "covid deaths" --domain "data.cdc.gov" --dataset-id "9bhg-hcku" --where "state='New York' AND covid_19_deaths > 100"
node socrata_open_data_scraper.mjs --token YOUR_APIFY_TOKEN --search-query "covid deaths" --domain "data.cdc.gov" --dataset-id "9bhg-hcku" --where "state='New York' AND covid_19_deaths > 100"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `searchQuery` | string |  | Find datasets across ALL Socrata portals by keyword (for example covid deaths, restaurant inspections, trade) |
| `domain` | string |  | The Socrata portal domain to pull rows from, for example data.cdc.gov, data.ny.gov, data.cityofnewyork.us |
| `datasetId` | string |  | The dataset's 4x4 identifier, for example 9bhg-hcku |
| `where` | string |  | Optional SoQL filter, for example state='New York' AND covid_19_deaths > 100 |
| `select` | string |  | Optional comma-separated fields to return, for example state,sex,age_group,covid_19_deaths |
| `order` | string |  | Optional sort, for example covid_19_deaths DESC |
| `maxResults` | integer | `1000` | Maximum number of records (rows or datasets) to return |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `_type` | string | Record type: 'dataset' for discovery mode results |
| `domain` | string | Socrata portal domain (for example data.cdc.gov) |
| `dataset_id` | string | Socrata dataset four-by-four identifier |
| `name` | string | Dataset name (discovery mode) |
| `description` | string | Dataset description (discovery mode) |
| `dataset_type` | string | Dataset type (for example dataset, map, chart) |
| `rows_count` | number | Number of rows in the dataset |
| `updated_at` | string | Date the dataset was last updated |
| `permalink` | string | Permanent link to the dataset on the portal |
| `_domain` | string | Source portal domain (data pull mode) |
| `_dataset_id` | string | Source dataset ID (data pull mode) |
| `_scraped_at` | string | ISO timestamp when this record was scraped |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/socrata-open-data
```

## FAQ

### What is Socrata?

Socrata is the platform that powers open data portals for the CDC, HHS, New York City, Chicago, Los Angeles, Texas, and 200+ other government entities. One API, one query language, all portals.

### What is SoQL?

SoQL (Socrata Query Language) is a SQL-like query syntax built into every Socrata dataset. Use $select, $where, $order, $limit, $offset, and $group to filter and aggregate data.

### How do I find the dataset ID?

Every Socrata dataset URL contains a 4x4 identifier (like xxxx-yyyy). This is the dataset ID used in all API calls. It appears in the URL after /d/ or at the end of the dataset page URL.

### Do I need an API key?

No key is needed for basic access (500 requests/hour per IP). A free Socrata app token raises this to 1,000 requests/hour and removes throttling on large dataset downloads.

### What are some high-value Socrata datasets?

CDC mortality statistics, NYC 311 complaint data, HHS hospital quality ratings, Chicago crime data, Texas open expenditures, and LA building permits are among the most-used.

### How much does the Socrata Open Data API Scraper cost?

From $0.60 per 1,000 records on Apify's higher plans ($1.00 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged. You can cap what a single run may spend with the maximum cost setting on Apify.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [India Gov Data](https://themineworks.com/actors/india-data-gov-scraper/): Trade, prices, and thousands of datasets from data.gov.in
* [CourtListener Scraper](https://themineworks.com/actors/courtlistener-court-records/): US court opinions, dockets, and case law as structured JSON
* [US State Business Registry](https://themineworks.com/actors/us-state-business-registry/): Officers, registered agents and status from official state registries

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
