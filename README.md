## site2graph

Utilities for detecting errors in websites and inspecting site graphs.

It might evolve into an open source alternative to [screaming frog](https://www.screamingfrog.co.uk/seo-spider/), at least for some SEO errors.

* [Overview](#Overview)
* [Usage](#Usage)
  * [Install](#Install)
  * [Scrape a site](#Scrape-a-site)
  * [Detect errors](#Detect-errors)
* [Development](#Development)

### Overview

Things you can do with this:

* detect errors in your website: broken links, 500, redirect loops
* crawl a website's links and metadata into a generic json representation that's easy to deal with for further processing

### Usage

#### Install

1. clone this repo
2. create a virtualenv: `python3 -m venv env`
3. install requirements: `env/bin/pip install -r requirements.txt`

#### Scrape a site

This will scrape the https://blog.scrapinghub.com site into a `site.json` file:

If `site.json` already exists scrapy will append lines to it, so delete it to start from a clean slate.

```bash
env/bin/scrapy crawl checks \
    -a start_url=https://blog.scrapinghub.com \
    --output=site.json \
    --output-format jsonlines
```

#### Detect errors

We can pipe the `site.json` file to the `get_errors` utility; this will report things like 404 links, 500 errors and redirect loops:

```bash
cat site.json | env/bin/python -m site2graph.get_errors --output_format friendly
```

### Development

* `make check` runs typechecks and linters
* `make fmt` runs formatters on the source
* `make test` runs unit tests
