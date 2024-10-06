from typing import Iterator
import pytest
import os
import importlib

# from utils.logger_contextman import get_logger
# logger = get_logger(__name__, "DEBUG")


@pytest.fixture(scope="module")
def user_submission(request: pytest.FixtureRequest) -> str:
    """fixture to read user submitted code"""
    user_file: str = str(request.config.getoption("--user_file"))
    user_file_dir, user_module = os.path.split(user_file)
    user_module = user_module.removesuffix(".py")
    while user_file_dir:
        user_file_dir, user_package = os.path.split(user_file_dir)
        user_module = user_package + "." + user_module
    return user_module


# number of teams that will be play playoff games
# for now, we only handle no_of_playoff_teams = 2**n, which means all teams
# have equal chances and same expected path to win (other number of playoff
# teams will require some teams to skip certain rounds, which we won't worry
# about for this challenge)
no_of_playoff_teams = 8

# Usually, out of all the playoff_teams, they will be ranked by points they
# earned during group round robin games, and the highest ranked team will
# play the lowest ranked team, the following is a simulation of the teams:
playoff_teams = [f"Team_{t+65:c}" for t in range(no_of_playoff_teams)]

time_field_availability = {
    'day_8_am': ['east', 'west', 'north', 'south'],
    'day_8_pm': ['east', 'west', 'north', 'south'],
    'day_9_am': ['east', 'west', 'north', 'south'],
    'day_9_pm': ['east', 'west', 'north', 'south'],
}


# function similate game report which team won their game
def winner_of(team_a: str, team_b: str) -> str:
    """report game results, who won"""
    game_played = True
    if game_played:
        return max(team_a, team_b)
    else:
        return f"winner between {team_a, team_b}"
##### End do-not-change section #####


def solution(playoff_teams, time_field_availability) -> dict:
    # Convert time_field_availability dict to list[(time,field)] sequence
    fields_available = ((time, field) for time in time_field_availability
                        for field in time_field_availability[time] if field)
    return schedule_playoff_matches(playoff_teams, fields_available)


def schedule_playoff_matches(playoff_teams: list, fields_available: Iterator
                             ) -> dict:
    """scheduling playoff teams

    Will take a ranked list of teams, arrange matches, and return a list of 
        scheduled games. 

    Args:
        playoff_teams: list of team names sorted by group stage ranking

    Returns:
        {"round": [list of winning teams of this round]}
        round is represented as a fraction, i.e. quarter final it is "1/4", 
        for semi-final it is "1/2", final is called "1/1.
    """
    playoff_match_schedule = {}
    no_of_playoff_teams = len(playoff_teams)
    games = {
        f"1/{no_of_playoff_teams}": playoff_teams}
    teams_left = no_of_playoff_teams
    while (teams_left := teams_left >> 1):
        current_round_games = []
        for g in range(teams_left):
            # games are pair of teams that will play,
            # i.e. (1, 8) means top ranked team will play the 8th ranked team
            match_ = (g + 1, teams_left * 2 - g)
            current_round_games.append(match_)
            playoff_match_schedule[next(fields_available)] = (match_,
                                                              f"1/{teams_left}")
        games[f"1/{teams_left}"] = current_round_games

    return playoff_match_schedule


def test_user_solutions(user_submission: str) -> None:
    user_module = importlib.import_module(user_submission)
    #logger.debug(f"{user_module.schedule_playoff_matches(playoff_teams)=}")
    #logger.debug(f"{schedule_playoff_matches(playoff_teams)=}")
    assert solution(playoff_teams, time_field_availability) == \
        user_module.solution(playoff_teams, time_field_availability)


if __name__ == "__main__":
    # playoff_matches are:
    # {((prev_round_match_#1, prev_round_match_#2), round): (time, field)}
    playoff_matches = solution(playoff_teams, time_field_availability)

    # output schedule with list formst
    print("\nBy time and field:")
    for seq, match_ in enumerate(playoff_matches):
        print(f"{seq:3}, {playoff_matches.get(match_)}\t "
              f"{match_[1]}\t"
              f"{match_[0]}")

    # played_games are ((prev_round_match_#1, prev_round_match_#2), round)
    played_games = {m[1]: [] for m in playoff_matches.values()}
    for m in playoff_matches.values():
        played_games[m[1]].append(m[0])
    rounds = list(played_games)
    for rn, (_, rnd_games) in enumerate(played_games.items()):
        if rn:
            last_round_game = played_games[rounds[rn - 1]]
        else:
            last_round_game = playoff_teams
        rnd_games[:] = map(lambda x: winner_of(
            last_round_game[x[0] - 1], last_round_game[x[1] - 1]), rnd_games)

    print(*played_games.items(), sep="\n")
