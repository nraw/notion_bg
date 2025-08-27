import fire
from notion_bg.essen_site import create_my_essen_site

def main(year=None):
    """Generate Essen site for specified year (defaults to latest)"""
    create_my_essen_site(year)

if __name__ == "__main__":
    fire.Fire(main)
