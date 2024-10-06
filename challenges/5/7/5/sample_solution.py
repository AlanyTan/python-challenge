##### Start condition #####
round_robin_rounds = 2
groups = {
    'A': ['Argentina', 'Brazil', 'Chile', 'Denmark'],
    'B': ['England', 'France', 'Greece', 'Hungary'],
    'C': ['Italy', 'Japan', 'Kuwait', 'Luxembourg'],
    'D': ['Mongolia', 'Nigeria', 'Oman', 'Poland']
}
time_field_availability = {
    'day_1_am': ['east', 'north', 'south'],
    'day_1_pm': ['east', 'west', 'north',],
    'day_2_am': ['east', 'west', 'south'],
    'day_2_pm': ['west', 'north', 'south'],
    'day_3_am': ['east', 'west', 'north', 'south'],
    'day_3_pm': ['east', 'west', 'north', 'south'],
    'day_4_am': ['east', 'west', 'north', 'south'],
    'day_4_pm': ['east', 'north', 'south'],
    'day_5_am': ['east', 'west', 'north',],
    'day_5_pm': ['east', 'west', 'south'],
    'day_6_am': ['west', 'north', 'south'],
    'day_6_pm': ['east', 'west', 'north', 'south'],
    'day_7_am': ['east', 'west', 'north', 'south'],
    'day_7_pm': ['east', 'west', 'north', 'south'],
}

# number of teams that will be play playoff games
no_of_playoff_teams = 8

# typically winning team get 2 points, lossing team gets 0, if game is tied
# both team get 1 point
game_points = {"win": 2, "tie": 1, "loss": 0}

# This is used to simulate game play results
# Use this function to "play" the games


def match_result(team_guest: str, team_host: str) -> dict:
    # simulate a match result using len of team names
    lg = len(team_guest)
    lh = len(team_host)
    return {"result": "tie" if lg == lh else "host" if lg < lh else "guest",
            "host_score": lh,
            "guest_score": lg
            }

# This is used to rank teams, sum the items of this tuple per team,
# Within each group, the teams are ranked by the accumulated ranking facotrs.
# i.e. the higher points rank higher, if points are tied, compare their total
# score_differential, if still tied, compare the total score out of all group
# games played.


def team_ranking_factors(game_result: dict) -> list[tuple[int]]:
    # calculate values of ranking factors
    # will use the total of: points, score_differential, my_score
    results = []
    winner = game_result.get("result")
    results.append((
        game_points.get("win" if winner == "guest" else "loss" if winner == "host"
                   else "tie"),
        game_result.get("guest_score", 0) - game_result.get("host_score", 0),
        game_result.get("guest_score", 0)
    ))
    results.append((
        game_points.get("win" if winner == "host" else "loss" if winner == "guest"
                   else "tie"),
        game_result.get("host_score", 0) - game_result.get("guest_score", 0),
        game_result.get("host_score", 0)
    ))
    return (results)

# This is used to break ties if after taking into all ranking factors two teams
# are still tied, call this func with the team names of the two tied teams


def tie_breaker(team_a: str, team_b: str) -> str:
    return min(team_a, team_b)

##### End of Start conditions #####


# Convert time_field_availability dict to list[(time,field)] sequence
fields_available = ((time, field) for time in time_field_availability
                    for field in time_field_availability[time] if field)


def schedule_matches(groups: dict, fields_available: list[dict],
                     round_robin_rounds: int = 2) -> dict:
    """The core scheduling functionality for group matches

    Args: 
        groups: dict of groud_name:list[teams]
        fields_available: a list of tuples of (time, field)
        round_robin_rounds: int of number of intra-group games to play each
                            opponent, default is 2.

    Returns:
        a dict, keys are tuples of (tuple(guest_team,host_team), # of times 
        these two teams played each other, the group_name); the value is the
        field these two teams will be playing on
    """
    field = None
    match_schedule = {}
    team_schedule = {team: [] for group in groups.values() for team in group}
    all_teams_by_group = [(team, group_name) for group_name in groups
                          for team in groups[group_name]]
    while any(((len(team_schedule[team])
                < (len(group) - 1) * round_robin_rounds)
               for group in groups.values() for team in group)):
        teams_sorted_by_round_played = sorted(all_teams_by_group, key=lambda x:
                                              (len(team_schedule[x[0]]), max(
                                                  team_schedule[x[0]], [''])))
        current_round_paired = []
        for home_team, home_group in teams_sorted_by_round_played:
            if field is None:
                field = next(fields_available)

            if home_team in current_round_paired or (
                    field[0] in team_schedule.get(home_team)):
                continue

            sorted_guest_group = sorted(
                filter(lambda x: x != home_team and x not in
                       current_round_paired, groups[home_group][::-1]),
                key=lambda x: (len(team_schedule[x]),
                               max(team_schedule[x], [''])))
            while sorted_guest_group:
                guest_team = sorted_guest_group.pop(0)

                match_ = tuple(sorted([guest_team, home_team])
                               ) if round_robin_rounds % 2 else (
                                   guest_team, home_team)
                match_count = [m[0] for m in match_schedule.keys()
                               ].count(match_)
                if (match_count >= (round_robin_rounds /
                                        (2 - round_robin_rounds % 2))
                        ) or field[0] in team_schedule.get(guest_team):
                    continue

                match_schedule[(match_, match_count + 1, home_group)] = field
                team_schedule[home_team].append(field[0])
                team_schedule[guest_team].append(field[0])
                current_round_paired.extend(match_)
                # we had a match, no need to check the rest of the group
                sorted_guest_group = []
                # this field had been used by this match,
                field = None

        if not current_round_paired:
            # no teams can use this field, skip this field for now...
            field = None

    return match_schedule


# call the schedule_matches function
match_schedule = schedule_matches(groups, fields_available, round_robin_rounds)


# output schedule with list formst
group_name_width = max([len(group_name) for group_name in groups])
print("\nBy time and field:")
team_standing = {team: [(0, 0, 0), group]
                 for group, teams in groups.items() for team in teams}

for seq, match_ in enumerate(match_schedule):
    guest_team = match_[0][0]
    host_team = match_[0][1]
    match_result_ = match_result(guest_team, host_team)
    points = team_ranking_factors(match_result_)
    team_standing[guest_team][0] = [z[0] + z[1] for z in
                                    zip(team_standing[guest_team][0], points[0])]
    team_standing[host_team][0] = [z[0] + z[1] for z in
                                   zip(team_standing[host_team][0], points[1])]

    print(f"{seq:3}, {match_schedule.get(match_)}\t "
          f"{match_[2]:{group_name_width}}"
          f"{match_[0:2]}\t {match_result_}"
          f"\t{team_standing[guest_team]}, \t{team_standing[host_team]}")

print(*list(sorted(team_standing.items(), key=lambda x: x[1])), sep='\n')

teams_from_each_group = no_of_playoff_teams // len(groups)
wildcard_teams = no_of_playoff_teams % len(groups)

playoff_teams = []
for g in groups:
    group_sorted = sorted(filter(lambda x: x[1][1] == g, team_standing.items()),
                          key=lambda t: t[1], reverse=True)
    for tn in range(teams_from_each_group):
        playoff_teams.append(team_standing.get(group_sorted[tn]))

# sort by points, score diff, winning goals
sorted_team_standing = sorted(team_standing.items(), key=lambda x: x[1],
                              reverse=True)

# need to add logic for wildcard teams and tie breakers

teams_left = no_of_playoff_teams
while (teams_left):
    playoff_teams

    teams_left >>= 1


def schedule_playoff_matches() -> None:
    # your challenge is complete this function, and return a dict
    # similar to the schedule_matches function
    pass
