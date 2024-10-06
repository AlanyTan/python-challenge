"""generating test cases of problem,solution pairs"""

from utils.generate_problem_json import generate_problem_json, print_result

problem: dict = {
    "title": "Scheduling playoff matches",
    "goal": "Leverage data structure, flow control and data types to solve"
            "practical schedule playoff matches problem",
    "description": "Design a function that schedule playoff (elimination) "
            "games. \nThe returned value should be a dictionary like:"
            "{('day_8_am', 'east'): ((1,8), '1/4')} \n"
            "where the key is a tuple of (time, field), \n and the value is "
            "a tuple that contains another tuple and a string, \n  where the "
            "inner tuple is (guest, host),\n   guest is the game# from which "
            "the guest team should come from,\n   and host is the game# from "
            "which the host team should come from; \n"
            " the string is the round name of which the teams are drawn from.\n"
            "i.e. for quarter final, the string is '1/4', and first game \n"
            " should be (1, 8) where 1 means team had highest standing from \n"
            " the previous round, and 8 means the team had 8th standing from \n"
            " the previous round;"
            "for semi-final, the round string should be '1/2', and the first \n"
            " game should be (1, 4) where 1 means game #1 of quarter-final \n"
            " (where highest ranked team played), and 4 means game #4 of \n"
            " quarter-final, (where 4th) ranked team played the 5th ranked team",
    "notes": "\n1) you don't need to use winner_of() function for the actual "
            "solution, it is proivided for testing your solution to see if the "
            "games scheduled played out as expected; \n2) you can create and "
            "use other functions as you wish, but the one we will test is "
            "solution(playoff_teams, time_field_availability)",
    "condition_code": '''
# number of teams that will be playing playoff games
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
    #report game results, who won
    game_played = True
    if game_played:
        return max(team_a, team_b)
    else:
        return f"winner between {team_a, team_b}"
''',
    "starting_code": '''

def schedule_playoff_matches(playoff_teams: list) -> dict:
    # replace the below pass with your code to finish this function
    # return a dict like {('day_8_am', 'east'): ((1,8), '1/4'), 
    # ('day_8_pm', 'west'): ((2,7), '1/4')...}
    pass

    
def solution(playoff_teams, time_field_availability):
    # Convert time_field_availability dict to list[(time,field)] sequence
    fields_available = ((time, field) for time in time_field_availability
                    for field in time_field_availability[time] if field)
    return schedule_playoff_matches(playoff_teams, fields_available)

if __name__ == "__main__":
    # playoff_matches are:
    #
    playoff_matches = schedule_playoff_matches(playoff_teams)
''',
}
starting_condition = []


def solution() -> str:
    """the actual solution that will generate the expected output"""
    #from utils.generate_problem_json import print

    return print_result()


if __name__ == '__main__':
    generate_problem_json(__file__, problem, starting_condition, solution,
                          globals())
