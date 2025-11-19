#!/usr/bin/env python3
"""
Fetch publications from Google Scholar and save to JSON file.

Usage:
    python scripts/fetch_publications.py

Requirements:
    pip install scholarly

This script fetches all publications from Google Scholar profile and saves them
to assets/data/publications.json for the website to load.
"""

import json
import os
from scholarly import scholarly

# Your Google Scholar profile ID
SCHOLAR_ID = 'tOsSkM4AAAAJ'

def fetch_google_scholar_publications():
    """Fetch publications from Google Scholar."""
    print(f"Fetching publications for author ID: {SCHOLAR_ID}")

    try:
        # Search for author
        search_query = scholarly.search_author_id(SCHOLAR_ID)
        author = scholarly.fill(search_query)

        print(f"Found author: {author['name']}")
        print(f"Total publications: {len(author['publications'])}")

        # Extract citation metrics
        import datetime
        current_year = datetime.datetime.now().year
        five_years_ago = current_year - 5

        citedby = author.get('citedby', 0)
        citedby5y = author.get('citedby5y', 0)
        hindex = author.get('hindex', 0)
        hindex5y = author.get('hindex5y', 0)
        i10index = author.get('i10index', 0)
        i10index5y = author.get('i10index5y', 0)

        print(f"Citations: {citedby} (all time), {citedby5y} (since {five_years_ago})")
        print(f"h-index: {hindex} (all time), {hindex5y} (since {five_years_ago})")
        print(f"i10-index: {i10index} (all time), {i10index5y} (since {five_years_ago})")

        metrics = {
            'total_citations': citedby,
            'total_citations_5y': citedby5y,
            'h_index': hindex,
            'h_index_5y': hindex5y,
            'i10_index': i10index,
            'i10_index_5y': i10index5y,
            'five_years_ago': five_years_ago
        }

        publications = []

        # Fetch details for each publication
        for i, pub in enumerate(author['publications'], 1):
            try:
                print(f"Fetching publication {i}/{len(author['publications'])}: {pub['bib']['title'][:50]}...")

                # Fill in complete publication details
                filled_pub = scholarly.fill(pub)

                # Extract relevant information
                bib = filled_pub.get('bib', {})
                pub_data = {
                    'title': bib.get('title', 'Untitled'),
                    'authors': bib.get('author', 'Unknown Authors'),
                    'venue': bib.get('venue', bib.get('journal', bib.get('booktitle', 'Unknown Venue'))),
                    'year': bib.get('pub_year', ''),
                    'abstract': bib.get('abstract', ''),
                    'citations': filled_pub.get('num_citations', 0),
                    'url': filled_pub.get('pub_url', ''),
                    'eprint_url': filled_pub.get('eprint_url', ''),
                    'author_id': filled_pub.get('author_id', []),
                    'pub_type': bib.get('pub_type', 'article')
                }

                publications.append(pub_data)

            except Exception as e:
                print(f"Warning: Failed to fetch details for publication: {e}")
                continue

        print(f"\nSuccessfully fetched {len(publications)} publications")
        return publications, metrics

    except Exception as e:
        print(f"Error fetching publications: {e}")
        return None, None

def categorize_publications(publications):
    """Categorize publications by type."""
    categories = {
        'journals': [],
        'conferences': [],
        'patents': [],
        'thesis': [],
        'other': []
    }

    for pub in publications:
        title_lower = pub['title'].lower()
        title = pub['title']
        venue_lower = pub['venue'].lower()
        url = pub.get('url', '').lower()

        # Categorization logic with improved detection

        # 1. Detect Patents
        if (url and 'patent' in url) or \
           ('patent' in venue_lower) or \
           ('patent' in title_lower) or \
           (title.isupper() and len(title) > 20):  # Patents often in ALL CAPS
            categories['patents'].append(pub)

        # 2. Detect Thesis/Dissertation
        elif any(keyword in title_lower for keyword in ['thesis', 'dissertation', 'pose estimation framework for robots']):
            categories['thesis'].append(pub)

        # 3. Detect Journals
        elif any(keyword in venue_lower for keyword in ['journal', 'ieee access', 'ijars', 'transactions', 'ijscai']):
            categories['journals'].append(pub)

        # 4. Detect Conferences
        elif any(keyword in venue_lower for keyword in ['conference', 'proceedings', 'workshop', 'symposium', 'icpeices', 'indicon', 'icacact']) or \
             any(keyword in title_lower for keyword in ['ml4h', 'neurips', 'cvpr', 'iccv', 'eccv']) or \
             (url and 'ieeexplore.ieee.org' in url and 'journal' not in venue_lower and 'access' not in venue_lower):  # IEEE Xplore papers without journal venue are usually conferences
            categories['conferences'].append(pub)

        # 5. Has venue but unclear type - add to conferences by default
        elif pub['venue'] and pub['venue'] != 'Unknown Venue':
            categories['conferences'].append(pub)

        # 6. Everything else
        else:
            categories['other'].append(pub)

    # Sort each category by year (descending)
    for category in categories:
        categories[category] = sorted(
            categories[category],
            key=lambda x: int(x['year']) if x['year'] else 0,
            reverse=True
        )

    return categories

def save_publications(publications, metrics, output_file):
    """Save publications to JSON file."""
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Categorize publications
    categorized = categorize_publications(publications)

    # Prepare output data
    output_data = {
        'last_updated': __import__('datetime').datetime.now().isoformat(),
        'total_count': len(publications),
        'metrics': metrics,
        'categories': categorized,
        'all_publications': publications
    }

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\nPublications saved to: {output_file}")
    print(f"  - Journal papers: {len(categorized['journals'])}")
    print(f"  - Conference papers: {len(categorized['conferences'])}")
    print(f"  - Patents: {len(categorized['patents'])}")
    print(f"  - Thesis: {len(categorized['thesis'])}")
    print(f"  - Other: {len(categorized['other'])}")

def main():
    """Main function."""
    # Fetch publications
    publications, metrics = fetch_google_scholar_publications()

    if not publications:
        print("Failed to fetch publications")
        return 1

    # Save to JSON file
    output_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'assets', 'data', 'publications.json'
    )

    save_publications(publications, metrics, output_file)
    print("\nDone! You can now load publications from the JSON file on your website.")

    return 0

if __name__ == '__main__':
    exit(main())
