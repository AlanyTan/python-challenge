#### Do not change this section ##### 

# number of teams that will be play playoff games
# for now, we only handle no_of_playoff_teams = 2**n, which means all teams
# have equal chances and same expected path to win (other number of playoff
# teams will require some teams to skip certain rounds, which we won't worry
# about for this challenge)
no_of_playoff_teams = 8

# Usually, out of all the playoff_teams, they will be ranked by points they
# earned during group round robin games, and the highest ranked team will
# play the lowest ranked team, the following is a simulation of the teams:
playoff_teams = [f"Team_{t}" for t in range(no_of_playoff_teams)]

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
##### End do-not-change section #####
##### End do-not-change section #####


# Convert time_field_availability dict to list[(time,field)] sequence
fields_available = ((time, field) for time in time_field_availability
                    for field in time_field_availability[time] if field)

def schedule_playoff_matches(playoff_teams: list) -> dict:
    # replace the below pass with your code to finish this function
    pass

##### Use the following code to test your solution
# 
