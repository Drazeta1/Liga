from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

LEAGUE_FILE = "league_data.json"
SCHEDULE_FILE = "schedule_data.json"

teams = [
    "Motor Łabiszyn", "MKS Kakałko Łabiszyn", "CSŁ Łabiszyn", "Pesa Łabiszyn",
    "Polonia Łabiszyn", "Kujawa Łabiszyn", "Pogoń Łabiszyn", "CSŁ II Łabiszyn"
]

def default_data():
    return {
        team: {
            "Punkty": 0, "Mecze": 0, "Zwycięstwa": 0, "Remisy": 0,
            "Porażki": 0, "Bramki zdobyte": 0, "Bramki stracone": 0, "Bilans": 0
        } for team in teams
    }

def load_data(filename, default):
    if not os.path.exists(filename):
        return default()
    with open(filename) as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)

@app.route("/league", methods=["GET"])
def get_league():
    league = load_data(LEAGUE_FILE, default_data)
    schedule = load_data(SCHEDULE_FILE, lambda: [])
    sorted_teams = sorted(
        league.items(), key=lambda x: (x[1]['Punkty'], x[1]['Bilans'], x[1]['Bramki zdobyte']), reverse=True
    )
    return jsonify({"teams": sorted_teams, "schedule": schedule})

@app.route("/match", methods=["POST"])
def post_match():
    data = request.json
    home = data.get("home")
    away = data.get("away")
    hg = int(data.get("homeGoals", 0))
    ag = int(data.get("awayGoals", 0))

    if home == away or home not in teams or away not in teams:
        return jsonify({"error": "Nieprawidłowe dane"}), 400

    league = load_data(LEAGUE_FILE, default_data)
    schedule = load_data(SCHEDULE_FILE, lambda: [])

    league[home]["Mecze"] += 1
    league[away]["Mecze"] += 1
    league[home]["Bramki zdobyte"] += hg
    league[home]["Bramki stracone"] += ag
    league[away]["Bramki zdobyte"] += ag
    league[away]["Bramki stracone"] += hg

    if hg > ag:
        league[home]["Zwycięstwa"] += 1
        league[away]["Porażki"] += 1
        league[home]["Punkty"] += 3
    elif hg < ag:
        league[away]["Zwycięstwa"] += 1
        league[home]["Porażki"] += 1
        league[away]["Punkty"] += 3
    else:
        league[home]["Remisy"] += 1
        league[away]["Remisy"] += 1
        league[home]["Punkty"] += 1
        league[away]["Punkty"] += 1

    for t in [home, away]:
        league[t]["Bilans"] = league[t]["Bramki zdobyte"] - league[t]["Bramki stracone"]

    schedule.append({
        "Gospodarz": home,
        "Gość": away,
        "Wynik": f"{hg}:{ag}"
    })

    save_data(LEAGUE_FILE, league)
    save_data(SCHEDULE_FILE, schedule)

    return jsonify({"message": "Wynik zapisany!"})

if __name__ == "__main__":
    app.run(debug=True)
