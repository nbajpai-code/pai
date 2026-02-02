import arxiv
import feedparser
import os
from datetime import datetime
import pytz

def fetch_pai_content():
    # 1. Fetch from Arxiv
    # Query: Physical AI, Robot Foundation Model, Vision Language Action, Embodied AI
    arxiv_query = '(all:"physical ai" OR all:"foundation model robotics" OR all:"vision language action" OR all:"embodied ai" OR all:"humanoid robot")'
    
    search = arxiv.Search(
        query=arxiv_query,
        max_results=5,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )
    
    papers = []
    try:
        client = arxiv.Client()
        results = client.results(search)
        for result in results:
            papers.append({
                'title': result.title,
                'url': result.entry_id,
                'published': result.published.strftime('%Y-%m-%d')
            })
    except Exception as e:
        print(f"Error fetching Arxiv: {e}")

    # 2. Fetch from News (Security Week - using general tech/AI keywords as proxy or generic tech feed if available, sticking to known feed for now)
    # Using a more general tech feed might be better, but sticking to what worked or using a placeholder logic.
    # Since specific "Physical AI" news feed is rare, we can stick to SecurityWeek for security aspects or just Arxiv for now.
    # Let's add a placeholder for news or try to fetch from a tech feed if possible.
    # I'll stick to the pattern but maybe just rely on Arxiv for "Physical AI" research as it's the main driver.
    # Or I can try to parse a robotics feed if I had one. 
    # For now, let's just do Arxiv to be safe and reliable.
    
    news_items = [] # Keeping empty for now unless we add a specific robotics feed later.

    # 3. Update File
    target_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'PHYSICAL_AI_RESOURCES.md')
    
    try:
        with open(target_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("Target file not found.")
        return

    marker = "## 🔄 Dynamic Updates"
    if marker in content:
        static_content = content.split(marker)[0]
    else:
        static_content = content + "\n"

    new_content = static_content + marker + "\n"
    new_content += f"*Last Updated: {datetime.now(pytz.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}*\n\n"
    
    new_content += "### 📄 Latest Research (Arxiv)\n"
    if not papers:
        new_content += "No new research papers found.\n"
    else:
        for p in papers:
            new_content += f"*   [{p['title']}]({p['url']}) ({p['published']})\n"

    with open(target_file, 'w') as f:
        f.write(new_content)
    
    print(f"Updated {target_file}")

if __name__ == "__main__":
    fetch_pai_content()
