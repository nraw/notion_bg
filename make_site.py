import fire

from notion_bg.essen_site import create_my_essen_site


def main(year=None, user_names: str = "nraw"):
    """Generate Essen site for specified year (defaults to latest)"""
    for user_name in user_names.split(","):
        create_my_essen_site(year=year, user_name=user_name)


if __name__ == "__main__":
    fire.Fire(main)
