import argparse
import csv
import json
import sys
from collections import defaultdict
from typing import Dict, List, NamedTuple, Set

MAX_REDIRECTS = 10


class PageError(NamedTuple):
    page: str
    link: str
    error: str


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


def pages_add_item(item, pages: Dict[str, Set[str]]):
    if item["type"] == "link":
        status = item["status"]
        if 200 >= int(status) < 300:
            src = item["url"]
            dst = item["target"]
            pages[dst].add(src)


def to_page_error_list(
    errors: Dict[str, Set], pages: Dict[str, Set[str]]
) -> List[PageError]:
    res: List[PageError] = []

    for link, vs in errors.items():
        for page in pages[link]:
            for error in vs:
                res.append(PageError(page=page, link=link, error=error))

    return sorted(res)


def print_csv(errors: Dict[str, Set], pages: Dict[str, Set[str]]) -> None:
    writer = csv.writer(sys.stdout)
    writer.writerow(PageError._fields)

    for page_error in to_page_error_list(errors, pages):
        writer.writerow(page_error)


def print_grouped(errors: Dict[str, Set], pages: Dict[str, Set[str]]) -> None:
    for link, vs in sorted(errors.items()):
        print(link)
        print("\terrors:", sorted(vs))
        print("\tfound in pages:")
        for page in sorted(pages[link]):
            print("\t{0}".format(page))
        print()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--output_format",
        required=True,
        choices=["csv", "friendly"],
        help="output format",
    )

    args = parser.parse_args()

    errors: Dict[str, Set] = defaultdict(set)
    pages: Dict[str, Set[str]] = defaultdict(set)

    for line in sys.stdin:
        item = json.loads(line)
        error_add_item(item, errors)
        pages_add_item(item, pages)

    if args.output_format == "friendly":
        print_grouped(errors, pages)
    else:
        print_csv(errors, pages)
