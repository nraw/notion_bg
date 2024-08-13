from datetime import datetime
from pathlib import Path

from jinja2 import Template

from notion_bg.get_essen import get_my_essen_games


def create_my_essen_site():
    # populate the jinja2 template in /notion_bg/essen.thml with my_essen_games
    # render the template and save it to /notion_bg/essen.html
    my_essen_games = get_my_essen_games()

    jinja_template = Path("notion_bg/essen.html").read_text()
    template = Template(jinja_template)
    timestamp = datetime.now()
    output = template.render(my_essen_games=my_essen_games, timestamp=timestamp)
    Path("site/essen.html").write_text(output)
