import json

def load_config():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

config = load_config()

def choose_option(options, prompt):
    for index, option in enumerate(options, 1):
        print(f"{index}. {option}")
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("תכניס מספר בין 1-4")
        except ValueError:
                print("תכניס מספר בין 1-4")



def choose_team(config) -> dict:
    
    clubs_names = list(config["clubs"].keys())
    chosen_club = choose_option(clubs_names,"תבחר מועדון - מספר בין 1-4")
    print(f"\nYou selected: {chosen_club}\n")

    club_teams = config['clubs'][chosen_club]['club teams']
    team_names = [team['team name'] for team in club_teams]
    chosen_team = choose_option(team_names,"תבחר קבוצה - מספר בין 1-3")
    team_id = None
    for team in club_teams:
        if team['team name'] == chosen_team:
            team_id = team['team id']
            break
    print(f"\nYou selected: {chosen_team}\n")

    team_details = {
        'club name': chosen_club,
        'team name': chosen_team,
        'team id': team_id
    }
    # TODO: delete the print below
    # print(team_details)
    return team_details

