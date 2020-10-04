import json
import sys
from collections import defaultdict
from typing import Dict, Set

MAX_REDIRECTS = 10


def error_add_item(item, errors: Dict[str, Set]) -> None:
    if item["type"] == "response":
        error_add_response(item, errors)
    elif item["type"] == "dns_lookup_error":
        url = item["request_url"]
        errors[url].add("dns_lookup_error")
    elif item["type"] == "timeout_error":
        url = item["request_url"]
        errors[url].add("timeout_error")
    else:
        pass


def error_add_response(item, errors: Dict[str, Set]) -> None:
    redirect_urls = item["redirect_urls"]
    status = item["status"]

    if redirect_urls == []:
        url = item["request_url"]
    else:
        url = redirect_urls[0]

    if len(redirect_urls) > MAX_REDIRECTS:
        errors[url].add("max_redirects")
    else:
        if 200 < int(status) > 299:
            errors[url].add(status)


def links_add_item(item, links: Dict[str, Set[str]]):
    if item["type"] == "link":
        status = item["status"]
        if 200 >= int(status) < 300:
            src = item["url"]
            dst = item["target"]
            links[dst].add(src)


if __name__ == "__main__":
    errors: Dict[str, Set] = defaultdict(set)
    links: Dict[str, Set[str]] = defaultdict(set)

    for line in sys.stdin:
        item = json.loads(line)
        error_add_item(item, errors)
        links_add_item(item, links)

    for k, vs in sorted(errors.items()):
        print(k)
        print("errors:", sorted(vs))
        print("links:", sorted(links[k]))
        print()
