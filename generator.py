import argparse
from datetime import datetime
from datetime import timedelta

from src.color import Color
from src.mappings import Mappings
from src.parser import Parser
from src.validator import Validator


def main(args):

    # Rename some variable to be smaller
    team = args.filter_by_team

    # Create the necessary objects
    color = Color()
    mappings = Mappings()
    parser = Parser()

    # Parse dates
    date = datetime.strptime(args.date, "%d/%m/%Y")

    if args.end_date:
        end_date = datetime.strptime(args.end_date, "%d/%m/%Y")
        dates = [date + timedelta(days=i) for i in range((end_date - date).days + 1)]
    else:
        dates = [date]

    total_games = 0

    for date in dates:

        # Get list of games
        games = parser.get_teams_day(date)

        # Print info about the day
        print()
        print(color.UNDERLINE + "Presenting Games for:" + color.END)
        print(color.BOLD + "Day  : " + color.END + date.strftime("%d (%A)"))
        print(color.BOLD + "Month: " + color.END + date.strftime("%m (%B)"))
        print(color.BOLD + "Year : " + color.END + date.strftime("%Y"))
        print()

        base_link = "https://www.mlb.com/unified-player/embed/"

        aux_total_games = total_games

        for game in games:

            # Parse info
            away, home, bs_link = game

            # Search for full name (e.g. New York Yankees)
            if args.filter_by_team and team not in [away, home]:
                continue

            total_games += 1

            print(color.YELLOW + "{} @ {}".format(away, home) + color.END)

            # Build condensed game link
            cg_at = mappings.team_cg_map[away]
            cg_ht = mappings.team_cg_map[home]
            cg_dt = date.strftime("%-m-%-d-%-y")
            cg = base_link + "cg-{}-{}-{}".format(cg_at, cg_ht, cg_dt)

            # Build highlights link
            hl_at = mappings.team_hl_map[away]
            hl_ht = mappings.team_hl_map[home]
            hl_dt = date.strftime("%-m-%-d")
            hl = base_link + "{}-vs-{}-recap-{}".format(hl_at, hl_ht, hl_dt)

            # Check if all links exist
            cg_exists = True
            hl_exists = True
            bs_exists = True

            if args.run_checks:
                for url in [cg, hl, bs_link]:
                    if not parser.url_exists(url):
                        if url == cg:
                            # Remove the year part
                            aux_cg = cg[:-3]
                            if not parser.url_exists(aux_cg):
                                cg_exists = False
                            else:
                                cg = aux_cg

                            # Check if it is condensed-game instead of cg
                            if not cg_exists:
                                aux_cg = cg.replace("cg", "condensed-game")
                                if not parser.url_exists(aux_cg):
                                    cg_exists = False
                                else:
                                    cg_exists = True
                                    cg = aux_cg

                        elif url == hl:
                            # Check if highlights exists instead of recap
                            aux_hl = hl.replace("recap", "highlights")
                            if not parser.url_exists(aux_hl):
                                hl_exists = False
                            else:
                                hl = aux_hl

                        elif url == bs_link:
                            bs_exists = False

            # Print everything
            if cg_exists:
                print(color.BOLD + "Condensed Game: " + color.END + cg)
            if hl_exists:
                print(color.BOLD + "Highlights    : " + color.END + hl)
            if bs_exists:
                print(color.BOLD + "Box Score     : " + color.END + bs_link)
            print()

        # If no games are added for a given date, print a message
        if aux_total_games == total_games:
            print(color.BOLD + "No games available :(\n" + color.END)

    if games:
        print("Found {} games!\n".format(total_games))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Example of usage: python3 mlb_cg_generator.py 23/07/2020 --end_date 26/07/2020"
    )
    parser.add_argument(
        "date",
        type=str,
        help="Expects the following format: day/month/year, e.g. 01/11/2020",
    )
    parser.add_argument(
        "--end_date",
        type=str,
        help="Expects the following format: day/month/year, e.g. 01/11/2020",
    )
    parser.add_argument(
        "--filter_by_team",
        type=str,
        help='Expects the full name: eg. "New York Yankees", "St. Louis Cardinals", etc.',
    )
    parser.add_argument(
        "--run_checks",
        action="store_true",
        help="If a lot of links fail, run this option. Use also for older dates. WARNING: Slow.",
    )
    args = parser.parse_args()

    validator = Validator(args)
    validator.validate_args()

    main(args)
