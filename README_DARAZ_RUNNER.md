# Daraz-only product research runner

This wrapper uses your existing `daraz_fetcher.py`; it does not search other websites.

## Install

From your `~/pk-collector` directory:

```bash
cp product_research.py product_research_cross_site_backup.py
cp /path/to/new/product_research.py ./product_research.py
```

If you downloaded the ZIP, extract it and copy the contained `product_research.py` into `~/pk-collector`.

## Run

```bash
conda activate laya
cd ~/pk-collector
python product_research.py --seed-url 'PASTE_DARAZ_PRODUCT_URL_HERE'
```

Defaults: one Daraz search page, up to 5 listings, one review page per star rating, page size 50, and a 2-second request delay.

Example with more results:

```bash
python product_research.py \
  --seed-url 'PASTE_DARAZ_PRODUCT_URL_HERE' \
  --daraz-pages 2 \
  --max-products 20 \
  --review-pages 2
```

Skip review collection:

```bash
python product_research.py --seed-url 'PASTE_DARAZ_PRODUCT_URL_HERE' --skip-reviews
```

## Output

The run creates `data/research/<product-title-slug>/` with input details, the seed product details, Daraz search results, one collection export, a SQLite database, logs, and `summary.json`. Collection runs once to avoid duplicate review collection for the seed listing.

The script does not delete your existing database, prior research folders, or other files. Review availability depends on what Daraz returns.
