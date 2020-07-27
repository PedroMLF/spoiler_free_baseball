# Spoiler-Free Baseball

### Motivation

[https://www.mlb.com/](https://www.mlb.com/) has highlight videos available for each of their games, as you can see [here](https://www.mlb.com/gameday/yankees-vs-nationals/2020/07/23/630851#game_state=final,lock_state=final,game_tab=videos,game=630851). The issue is that, to get there, you get the score spoiled for you.. Due to the different time zones all over the world not everyone gets the chance of watching the games live, and the condensed games are a good way of having the thrill of following a live game, in a short and always available format. Thus, I've created this very simple tool that allows the user to get the links to those videos and follow the recaps of the games, without having to know the scores of the games beforehand.

---

### How to use it?

> `git clone https://github.com/PedroMLF/spoiler_free_baseball.git`

In case you want to create a specific virtualenv for it:
> `virtualenv -p /python/path env_name`

> `source env_name/bin/activate`

Install the required dependencies (Tested with `python3.7`):
> `pip install -r requirements.txt`

Run it:
> `python generator.py 23/07/2020`

Example output:

```
Presenting Games for:
Day  : 23 (Thursday)
Month: 07 (July)
Year : 2020

San Francisco Giants @ Los Angeles Dodgers
Condensed Game: https://www.mlb.com/unified-player/embed/cg-sf-lad-7-23-20
Highlights    : https://www.mlb.com/unified-player/embed/giants-vs-dodgers-recap-7-23
Box Score     : https://www.baseball-reference.com/boxes/LAN/LAN202007230.shtml

New York Yankees @ Washington Nationals
Condensed Game: https://www.mlb.com/unified-player/embed/cg-nyy-wsh-7-23-20
Highlights    : https://www.mlb.com/unified-player/embed/yankees-vs-nationals-recap-7-23
Box Score     : https://www.baseball-reference.com/boxes/WAS/WAS202007230.shtml

Found 2 games!
```

---

### Arguments

#### Position

* `date` - format day/month/year, eg. `05/08/2020`

#### Optional

* `--end_date` - Used if you want to present links for a time range. Expects the same format as `date`.
* `--filter_by_team` - Show only the games for a given team. It expects the full name surrounded by `"`: `"Team"`.
* `--args_check` - If a lot of URLs fail, use this option to test alternatives, and show only working URLs. It's slow if a lot of links have to be checked.

---

### Examples

1. Getting all games for the 24th of July of 2020:

> `python generator.py 24/07/2020`

2. Getting all games between the 24th and the 26th of July of 2020:

> `python generator.py 24/07/2020 --end_date 26/07/2020`

3. Getting all games between the 24th and the 26th of July of 2020, only for the St. Louis Cardinals:

> `python generator.py 24/07/2020 --end_date 26/07/2020 --filter_by_team "St. Louis Cardinals"`

4. Getting all games between the 24th and the 26th of July of 2020, only for the St. Louis Cardinals, checking if the URL exist and alternative URLs:

> `python generator.py 24/07/2020 --end_date 26/07/2020 --filter_by_team "St. Louis Cardinals" --run_checks`

### Acknowledgements

* [https://www.mlb.com/](https://www.mlb.com/) - Videos.
* [https://www.baseball-reference.com/](https://www.baseball-reference.com/) - Schedule and Boxscores.