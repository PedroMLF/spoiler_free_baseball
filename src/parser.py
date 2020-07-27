import urllib.request
import requests
from datetime import datetime

from bs4 import BeautifulSoup


class Parser:
    """Class Parser used to parse info from outside URLs.
    """

    def __init__(self):
        pass

    def get_teams_day(self, date):
        """Method used to retrieve the info about the games played on a given
        day.

        Args:
            date ([datetime.datetime]): The string formatted as necessary to
            retrieve the games from baseball reference.

        Returns:
            [List[Tuple[str]]]: Returns a list of tuple whose elements are
            (away_team, home_team, boxscore_link).
        """

        # Format the data as necessary for baseball-reference
        date_fmt = date.strftime("%Y-%m-%d")

        # Get the HTML code from the URL
        base_url = "https://www.baseball-reference.com/"
        fp = urllib.request.urlopen(base_url + "boxes/?date=" + date_fmt)
        content = fp.read().decode("utf-8")
        fp.close()

        # Prepare the content for parsing
        soup = BeautifulSoup(content, "html.parser")
        boxscores = soup.find_all("div", {"class": "game_summary nohover"})

        # Get the info about each game
        results = []
        for boxscore in boxscores:
            links = boxscore.find_all("a")
            away = str(links[0]).split(">")[1].split("</a")[0]
            home = str(links[2]).split(">")[1].split("</a")[0]
            bs_aux = str(links[1]).split('"')[1]
            bs_link = "https://www.baseball-reference.com" + bs_aux
            results.append((away, home, bs_link))

        return results

    def url_exists(self, url):
        """Method used to check whether a URL exists or not.

        Args:
            url ([str]): String with the URL to exist-

        Returns:
            [bool]: Returns True if the URL exists, False if it doesn't.
        """
        request = requests.head(url)
        if request.status_code != 200:
            return False
        return True
