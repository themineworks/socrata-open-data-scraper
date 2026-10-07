#!/usr/bin/env python3
"""Any government data portal: CDC, HHS, NYC, Texas, and hundreds more. Python, Node.js and cURL clients for the Socrata Open Data API Scraper on Apify, pay per result.

Command-line client for the themineworks/socrata-open-data actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/socrata-open-data/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/socrata-open-data"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--search-query", help="Find datasets across ALL Socrata portals by keyword (for example covid deaths, restaurant…")
    ap.add_argument("--domain", help="The Socrata portal domain to pull rows from, for example data.cdc.gov, data.ny.gov…")
    ap.add_argument("--dataset-id", help="The dataset's 4x4 identifier, for example 9bhg-hcku")
    ap.add_argument("--where", help="Optional SoQL filter, for example state='New York' AND covid_19_deaths > 100")
    ap.add_argument("--select", help="Optional comma-separated fields to return, for example state,sex,age_group,covid_19_deaths")
    ap.add_argument("--order", help="Optional sort, for example covid_19_deaths DESC")
    ap.add_argument("--max-results", type=int, help="Maximum number of records (rows or datasets) to return")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.search_query is not None: run_input["searchQuery"] = a.search_query
    if a.domain is not None: run_input["domain"] = a.domain
    if a.dataset_id is not None: run_input["datasetId"] = a.dataset_id
    if a.where is not None: run_input["where"] = a.where
    if a.select is not None: run_input["select"] = a.select
    if a.order is not None: run_input["order"] = a.order
    if a.max_results is not None: run_input["maxResults"] = a.max_results

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
