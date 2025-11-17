# Publication Fetcher Script

This script fetches publications from your Google Scholar profile and generates a JSON file for the website to load dynamically.

## Setup

1. Install Python dependencies:
```bash
pip install -r scripts/requirements.txt
```

## Usage

Run the script from the repository root:

```bash
python scripts/fetch_publications.py
```

This will:
1. Fetch all publications from your Google Scholar profile
2. Categorize them (journals, conferences, patents, thesis)
3. Save the data to `assets/data/publications.json`
4. The website will automatically load and display this data

## Scheduling

You can run this script manually whenever you publish new papers, or set it up to run automatically:

### Option 1: Manual Updates
Just run the script whenever you want to update your publications:
```bash
python scripts/fetch_publications.py
git add assets/data/publications.json
git commit -m "Update publications"
git push
```

### Option 2: GitHub Actions (Automated)
Create `.github/workflows/update-publications.yml`:

```yaml
name: Update Publications

on:
  schedule:
    # Run weekly on Mondays at 9am UTC
    - cron: '0 9 * * 1'
  workflow_dispatch:  # Allow manual trigger

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install -r scripts/requirements.txt

      - name: Fetch publications
        run: python scripts/fetch_publications.py

      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add assets/data/publications.json
          git diff --quiet && git diff --staged --quiet || git commit -m "Auto-update publications from Google Scholar"
          git push
```

## Configuration

To use this for a different Google Scholar profile, edit `fetch_publications.py`:

```python
SCHOLAR_ID = 'your-scholar-id-here'
```

You can find your Scholar ID in your Google Scholar profile URL:
`https://scholar.google.com/citations?user=YOUR_ID_HERE`

## Troubleshooting

- **Rate limiting**: Google Scholar may rate limit requests. The script includes delays between requests.
- **Missing publications**: Ensure all publications are added to your Google Scholar profile
- **Categorization issues**: The script categorizes based on venue names. You may need to adjust the categorization logic in `categorize_publications()` function.
