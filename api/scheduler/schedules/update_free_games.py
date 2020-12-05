from django.conf import settings
import api.helper as helper
import api.commons as commons
import re
from linebot.models import TextSendMessage
from api.models import Game, Listener


# Simplify bot variables
BOT = settings.BOT
BOT_HANDLER = settings.BOT_HANDLER


def extract_free_games(
    raw_games,
    extract_url,
    extract_id,
    extract_name,
    extract_discount,
):
    free_games = []
    for raw_game in raw_games:
        discount = extract_discount(raw_game)
        # UNCOMMENT THIS DEBUG IF YOU NEED IT, DON'T FORGET TO COMMENT IT AGAIN BEFORE GO TO PRODUCTION
        # print({
        #     "url": extract_url(raw_game),
        #     "id": extract_id(raw_game),
        #     "name": extract_name(raw_game),
        #     "discount": discount,
        # })
        if discount >= 100:
            free_games.append(
                {
                    "url": extract_url(raw_game),
                    "id": extract_id(raw_game),
                    "name": extract_name(raw_game),
                    "discount": discount,
                }
            )

    return free_games


def get_steam_free_games():
    def extract_url(raw_game):
        return "https://store.steampowered.com/app/" + raw_game["data-appid"]

    def extract_id(raw_game):
        return raw_game["data-appid"]

    def extract_name(raw_game):
        return raw_game.select_one('td:nth-child(3) a[href^="/app/"]').get_text()

    def extract_discount(raw_game):
        raw_discount = raw_game.select_one("td:nth-child(4)").get_text()
        return float(re.search(r"([0-9\.]+)%", raw_discount).group(1))

    raw_games = helper.load_page(
        "https://steamdb.info/sales/?min_discount=95&min_rating=0"
    ).select(".app")
    games = extract_free_games(
        raw_games,
        extract_url,
        extract_id,
        extract_name,
        extract_discount,
    )

    return [{"provider_name": "Steam", **game} for game in games]


def get_humble_free_games():
    def extract_url(raw_game):
        return "https://www.humblebundle.com/store/" + raw_game["human_url"]

    def extract_id(raw_game):
        return raw_game["human_url"]

    def extract_name(raw_game):
        return raw_game["human_name"]

    def extract_discount(raw_game):
        current_price = raw_game["current_price"]["amount"]
        full_price = raw_game["full_price"]["amount"]

        if full_price == 0:
            return 100

        return (1 - (current_price / full_price)) * 100

    raw_games = helper.load_json(
        "https://www.humblebundle.com/store/api/search?sort=discount&filter=all&request=1"
    )["results"]

    games = extract_free_games(
        raw_games,
        extract_url,
        extract_id,
        extract_name,
        extract_discount,
    )

    return [{"provider_name": "Humble", **game} for game in games]


def get_epic_free_games():
    def extract_url(raw_game):
        return (
            "https://www.epicgames.com/store/en-US/product/" + raw_game["productSlug"]
        )

    def extract_id(raw_game):
        return raw_game["id"]

    def extract_name(raw_game):
        return raw_game["title"]

    def extract_discount(raw_game):
        current_price = raw_game["price"]["totalPrice"]["discountPrice"]
        full_price = raw_game["price"]["totalPrice"]["originalPrice"]

        if full_price == 0:
            return 0

        return (1 - (current_price / full_price)) * 100

    raw_games = helper.load_json(
        "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=ID&allowCountries=ID"
    )
    raw_games = raw_games["data"]["Catalog"]["searchStore"]["elements"]

    games = extract_free_games(
        raw_games,
        extract_url,
        extract_id,
        extract_name,
        extract_discount,
    )
    return [{"provider_name": "Epic", **game} for game in games]


def notify_new_free_games(new_free_games):
    message_text = commons.create_free_game_list(new_free_games)
    message = TextSendMessage(text=message_text)

    # Get all listeners
    listeners = Listener.objects.filter(type="FREEGAME")

    # Send to all users
    user_listeners = listeners.filter(chat_type="USER")
    user_listener_ids = []
    for user_listener in user_listeners:
        user_listener_ids.append(user_listener.listener_id)

    if len(user_listener_ids) > 0:
        BOT.multicast(user_listener_ids, message)

    # Send to all groups/rooms
    group_listeners = listeners.exclude(chat_type="USER")
    for group_listener in group_listeners:
        BOT.push_message(group_listener.listener_id, message)


FREE_GAME_EXTRACTORS = [
    get_steam_free_games,
    get_humble_free_games,
    get_epic_free_games,
]


def update_free_games():
    free_games = []
    for extrator in FREE_GAME_EXTRACTORS:
        free_games += extrator()

    new_free_games = []
    for free_game in free_games:
        if (
            helper.get_object_or_none(Game, game_id=free_game["id"], discount=100.0)
            is None
        ):
            game = Game(
                provider_name=free_game["provider_name"],
                name=free_game["name"],
                source_url=free_game["url"],
                game_id=free_game["id"],
                original_price=0.0,
                discount=free_game["discount"],
            )
            game.save()
            new_free_games.append(game)

    # Delete expired free games
    undeleted_free_game_ids = [free_game["id"] for free_game in free_games]
    Game.objects.filter(discount=100.0).exclude(
        game_id__in=undeleted_free_game_ids
    ).delete()

    if len(new_free_games) > 0:
        notify_new_free_games(new_free_games)
