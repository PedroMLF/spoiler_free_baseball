from datetime import datetime

from src.mappings import Mappings


class Validator:
    """Class Validator that allows the validation of all input arguments.
    """

    def __init__(self, args):
        self.args = args

    def validate_args(self):
        """Validates all the input arguments.

        Raises:
            ValueError
        """

        # Convert dates
        date = self._format_date(self.args.date)

        # Validate the input date
        self._validate_date(date)

        # Validate several things related to end date
        if self.args.end_date:
            end_date = self._format_date(self.args.end_date)
            self._validate_date(end_date)
            if end_date < date:
                raise ValueError("End Date should be earlier than Date")
            if (end_date - date).days > 7:
                raise ValueError("Restrict the timedelta to 7 days")

        # Validate the filter team
        if self.args.filter_by_team:
            self._validate_team(self.args.filter_by_team)

    def _format_date(self, date):
        """Formats the date into a defined datetime format.

        Args:
            date (str): Input date using the defined format d/m/y.

        Returns:
            [datetime.datetime]: Formatted input date.
        """
        return datetime.strptime(date, "%d/%m/%Y")

    def _validate_date(self, date):
        """Validates the input dates. It raises a ValueError if it finds a
        date from the future, and prevents fetching games from the ongoing day.

        Args:
            date ([datetime.datetime]): Date formatted into the correct format.

        Raises:
            ValueError
        """
        date_today = datetime.today()

        if date.year > date_today.year:
            raise ValueError("Invalid Year", date.year)

        elif date.year == date_today.year:
            if date.month > date_today.month:
                raise ValueError("Invalid Month", date.month)
            elif date.month == date_today.month:
                if date.day > date_today.day:
                    raise ValueError("Invalid Day", date.day)
                elif date.day == date_today.day:
                    raise ValueError("Wait at least a day for the links :)")

    def _validate_team(self, team):
        """Validates that the team user in filter_by_team exists in
        the mappings.

        Args:
            team (str): Team used in the filter.

        Raises:
            ValueError.
        """
        mappings = Mappings()
        if team not in mappings.team_cg_map:
            raise ValueError("Invalid team name: ", team)
