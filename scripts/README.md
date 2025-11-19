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

### Option 2: GitHub Actions (Automated) ✅ **ALREADY CONFIGURED**

The workflow is already set up at `.github/workflows/update-publications.yml`

**How it works:**
- ✅ Runs automatically every **Monday at 9am UTC**
- ✅ Can be triggered **manually** from the Actions tab
- ✅ Fetches publications from Google Scholar
- ✅ Commits and pushes changes if publications are updated
- ✅ Provides a summary of what changed

**To trigger manually:**
1. Go to your repository on GitHub
2. Click on the **Actions** tab
3. Select **"Update Publications from Google Scholar"** workflow
4. Click **"Run workflow"** button
5. Select the branch (usually `redesign`)
6. Click **"Run workflow"**

**To change the schedule:**
Edit `.github/workflows/update-publications.yml` and modify the cron expression:
```yaml
schedule:
  - cron: '0 9 * * 1'  # Every Monday at 9am UTC
```

Common schedules:
- Daily: `'0 9 * * *'`
- Weekly (Monday): `'0 9 * * 1'`
- Monthly (1st): `'0 9 1 * *'`

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
