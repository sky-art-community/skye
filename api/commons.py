from functools import cmp_to_key


def create_free_game_list(games):
    # Add the provider of games
    free_games = list(filter(lambda game: game.discount == 100.0, games))

    # Default message if none
    message_text = "No free games right now"

    # Overwrite the message if there are free games
    if len(free_games) > 0:
        # Set update date
        last_update_date = sorted(
            free_games,
            key=cmp_to_key(lambda a, b: 1 if a.created_at < b.created_at else -1),
        )[0].created_at
        message_text = "Last update date: {}\n".format(
            last_update_date.strftime("%d-%m-%Y %T")
        )

        # Create game list
        message_text += "Free games (100% off):\n"
        for index, game in enumerate(free_games):
            message_text += "{}. [{}] {} - {}\n".format(
                index + 1,
                game.provider_name,
                game.name,
                game.source_url,
            )

    return message_text
