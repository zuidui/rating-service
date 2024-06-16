import json
from datetime import datetime, timezone
from random import randint


def generate_score_rating_data():
    with open("players.json", "r") as f:
        players = json.load(f)

    scores = []
    player_ratings = []
    now = datetime.now(timezone.utc)

    for player in players:
        player_id = player["player_id"]
        team_id = player["team_id"]
        player_scores = [randint(1, 10) for _ in range(3)]  # Each player gets 3 scores

        for score in player_scores:
            scores.append(
                {
                    "player_id": player_id,
                    "team_id": team_id,
                    "score": score,
                    "created_at": now.isoformat(),
                }
            )

        average_score = sum(player_scores) / len(player_scores)
        player_ratings.append(
            {
                "player_id": player_id,
                "team_id": team_id,
                "average_score": average_score,
                "total_of_scores": len(player_scores),
                "last_updated": now.isoformat(),
            }
        )

    with open("scores.json", "w") as f:
        json.dump(scores, f, indent=4)

    with open("player_ratings.json", "w") as f:
        json.dump(player_ratings, f, indent=4)


if __name__ == "__main__":
    generate_score_rating_data()
