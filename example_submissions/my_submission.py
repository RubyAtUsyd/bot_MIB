from collections import defaultdict, deque
import random
from typing import Optional, Tuple, Union, cast
from risk_helper.game import Game
from risk_shared.models.card_model import CardModel
from risk_shared.queries.query_attack import QueryAttack
from risk_shared.queries.query_claim_territory import QueryClaimTerritory
from risk_shared.queries.query_defend import QueryDefend
from risk_shared.queries.query_distribute_troops import QueryDistributeTroops
from risk_shared.queries.query_fortify import QueryFortify
from risk_shared.queries.query_place_initial_troop import QueryPlaceInitialTroop
from risk_shared.queries.query_redeem_cards import QueryRedeemCards
from risk_shared.queries.query_troops_after_attack import QueryTroopsAfterAttack
from risk_shared.queries.query_type import QueryType
from risk_shared.records.moves.move_attack import MoveAttack
from risk_shared.records.moves.move_attack_pass import MoveAttackPass
from risk_shared.records.moves.move_claim_territory import MoveClaimTerritory
from risk_shared.records.moves.move_defend import MoveDefend
from risk_shared.records.moves.move_distribute_troops import MoveDistributeTroops
from risk_shared.records.moves.move_fortify import MoveFortify
from risk_shared.records.moves.move_fortify_pass import MoveFortifyPass
from risk_shared.records.moves.move_place_initial_troop import MovePlaceInitialTroop
from risk_shared.records.moves.move_redeem_cards import MoveRedeemCards
from risk_shared.records.moves.move_troops_after_attack import MoveTroopsAfterAttack
from risk_shared.records.record_attack import RecordAttack
from risk_shared.records.types.move_type import MoveType


# We will store our enemy in the bot state.
class BotState():
    def __init__(self):
        self.enemy: Optional[int] = None


def main():
    
    # Get the game object, which will connect you to the engine and
    # track the state of the game.
    game = Game()
    bot_state = BotState()
   
    # Respond to the engine's queries with your moves.
    while True:

        # Get the engine's query (this will block until you receive a query).
        query = game.get_next_query()

        # Based on the type of query, respond with the correct move.
        def choose_move(query: QueryType) -> MoveType:
            match query:
                case QueryClaimTerritory() as q:
                    return handle_claim_territory(game, bot_state, q)

                case QueryPlaceInitialTroop() as q:
                    return handle_place_initial_troop(game, bot_state, q)

                case QueryRedeemCards() as q:
                    return handle_redeem_cards(game, bot_state, q)

                case QueryDistributeTroops() as q:
                    return handle_distribute_troops(game, bot_state, q)

                case QueryAttack() as q:
                    return handle_attack(game, bot_state, q)

                case QueryTroopsAfterAttack() as q:
                    return handle_troops_after_attack(game, bot_state, q)

                case QueryDefend() as q:
                    return handle_defend(game, bot_state, q)

                case QueryFortify() as q:
                    return handle_fortify(game, bot_state, q)
        
        # Send the move to the engine.
        game.send_move(choose_move(query))
                

def handle_claim_territory(game: Game, bot_state: BotState, query: QueryClaimTerritory) -> MoveClaimTerritory:
    """At the start of the game, you can claim a single unclaimed territory every turn 
    until all the territories have been claimed by players."""
    """
    Try to claim territories that aim for continets early % of the continent
    """
    unclaimed_territories = game.state.get_territories_owned_by(None)
    my_territories = game.state.get_territories_owned_by(game.state.me.player_id)
    adjacent_territories = game.state.get_all_adjacent_territories(my_territories)
    available = list(set(unclaimed_territories) & set(adjacent_territories))
    
    # Get continents and their territories
    continents = game.state.map.get_continents()
    
    # Function to get continents with the fewest countries
    def get_continents_with_fewest_countries():
        continent_country_counts = [(continent, len(countries)) for continent, countries in continents.items()]
        sorted_continents = sorted(continent_country_counts, key=lambda x: x[1])
        continents_with_fewest_countries = [continent for continent, _ in sorted_continents]
        return continents_with_fewest_countries
    
    # Get the continents with the fewest countries
    continents_with_fewest_countries = get_continents_with_fewest_countries()
    
    # Find unclaimed territories in the preferred continents
    for continent in continents_with_fewest_countries:
        unclaimed_in_continent = [territory for territory in continents[continent] if territory in unclaimed_territories]
        
        if unclaimed_in_continent:
            # Prefer adjacent territories within the preferred continents
            available_in_continent = list(set(unclaimed_in_continent) & set(adjacent_territories))
            if available_in_continent:
                # Pick the territory with the most connections to our territories
                def count_adjacent_friendly(x: int) -> int:
                    return len(set(my_territories) & set(game.state.map.get_adjacent_to(x)))

                selected_territory = sorted(available_in_continent, key=lambda x: count_adjacent_friendly(x), reverse=True)[0]
                return game.move_claim_territory(query, selected_territory)
            
            # If no adjacent territories, pick any unclaimed territory in the continent
            selected_territory = sorted(unclaimed_in_continent, key=lambda x: len(game.state.map.get_adjacent_to(x)), reverse=True)[0]
            return game.move_claim_territory(query, selected_territory)
    
    # Fallback: If no territories in preferred continents are available, use the original strategy
    if available:
        def count_adjacent_friendly(x: int) -> int:
            return len(set(my_territories) & set(game.state.map.get_adjacent_to(x)))

        selected_territory = sorted(available, key=lambda x: count_adjacent_friendly(x), reverse=True)[0]
    else:
        selected_territory = sorted(unclaimed_territories, key=lambda x: len(game.state.map.get_adjacent_to(x)), reverse=True)[0]

    return game.move_claim_territory(query, selected_territory)


def handle_place_initial_troop(game: Game, bot_state: BotState, query: QueryPlaceInitialTroop) -> MovePlaceInitialTroop:
    """After all the territories have been claimed, you can place a single troop on one
    of your territories each turn until each player runs out of troops."""
    
    # We will place troops along the territories on our border.
    border_territories = game.state.get_all_border_territories(
        game.state.get_territories_owned_by(game.state.me.player_id)
    )

    # We will place a troop in the border territory with the least troops currently
    # on it. This should give us close to an equal distribution.
    border_territory_models = [game.state.territories[x] for x in border_territories]
    min_troops_territory = min(border_territory_models, key=lambda x: x.troops)

    return game.move_place_initial_troop(query, min_troops_territory.territory_id)


def handle_redeem_cards(game: Game, bot_state: BotState, query: QueryRedeemCards) -> MoveRedeemCards:
    """After the claiming and placing initial troops phases are over, you can redeem any
    cards you have at the start of each turn, or after killing another player."""

    # We will always redeem the minimum number of card sets we can until the 12th card set has been redeemed.
    # This is just an arbitrary choice to try and save our cards for the late game.

    # We always have to redeem enough cards to reduce our card count below five.
    card_sets: list[Tuple[CardModel, CardModel, CardModel]] = []
    cards_remaining = game.state.me.cards.copy()

    while len(cards_remaining) >= 5:
        card_set = game.state.get_card_set(cards_remaining)
        # According to the pigeonhole principle, we should always be able to make a set
        # of cards if we have at least 5 cards.
        assert card_set != None
        card_sets.append(card_set)
        cards_remaining = [card for card in cards_remaining if card not in card_set]

    # Remember we can't redeem any more than the required number of card sets if 
    # we have just eliminated a player.
    if game.state.card_sets_redeemed > 12 and query.cause == "turn_started":
        card_set = game.state.get_card_set(cards_remaining)
        while card_set != None:
            card_sets.append(card_set)
            cards_remaining = [card for card in cards_remaining if card not in card_set]
            card_set = game.state.get_card_set(cards_remaining)

    return game.move_redeem_cards(query, [(x[0].card_id, x[1].card_id, x[2].card_id) for x in card_sets])


def handle_distribute_troops(game: Game, bot_state: BotState, query: QueryDistributeTroops) -> MoveDistributeTroops:
    """After you redeem cards (you may have chosen to not redeem any), you need to distribute
    all the troops you have available across your territories. This can happen at the start of
    your turn or after killing another player.
    """

    total_troops = game.state.me.troops_remaining
    distributions = defaultdict(lambda: 0)
    my_territories = game.state.get_territories_owned_by(game.state.me.player_id)
    border_territories = game.state.get_all_border_territories(my_territories)

    # We need to remember we have to place our matching territory bonus
    # if we have one.
    if len(game.state.me.must_place_territory_bonus) != 0:
        assert total_troops >= 2
        distributions[game.state.me.must_place_territory_bonus[0]] += 2
        total_troops -= 2

    # Identify critical territories (e.g., between continents, adjacent to enemies with many troops)
    critical_territories = set()
    for territory in border_territories:
        adjacent_territories = game.state.map.get_adjacent_to(territory)
        for adj_territory in adjacent_territories:
            if game.state.territories[adj_territory].occupier != game.state.me.player_id:
                if game.state.territories[adj_territory].troops >= 3:  # Consider as critical if enemy has 3 or more troops
                    critical_territories.add(territory)
                    break

    # Distribute troops with a focus on critical territories
    critical_border_territories = list(critical_territories & set(border_territories))
    normal_border_territories = list(set(border_territories) - critical_territories)

    # Distribute more troops to critical territories
    if critical_border_territories:
        troops_per_critical_territory = total_troops // len(critical_border_territories)
        for territory in critical_border_territories:
            distributions[territory] += troops_per_critical_territory
            total_troops -= troops_per_critical_territory

    # Distribute remaining troops equally among other border territories
    if normal_border_territories and total_troops > 0:
        troops_per_normal_territory = total_troops // len(normal_border_territories)
        leftover_troops = total_troops % len(normal_border_territories)
        for territory in normal_border_territories:
            distributions[territory] += troops_per_normal_territory
            total_troops -= troops_per_normal_territory

        # Distribute leftover troops to any territory (we don't care which one)
        if leftover_troops > 0:
            distributions[normal_border_territories[0]] += leftover_troops
            total_troops -= leftover_troops

    # Ensure all troops are distributed
    if total_troops > 0:
        all_border_territories = critical_border_territories + normal_border_territories
        distributions[all_border_territories[0]] += total_troops

    return game.move_distribute_troops(query, distributions)



def handle_attack(game: Game, bot_state: BotState, query: QueryAttack) -> Union[MoveAttack, MoveAttackPass]:
    """After the troop phase of your turn, you may attack any number of times until you decide to
    stop attacking (by passing). After a successful attack, you may move troops into the conquered
    territory. If you eliminated a player you will get a move to redeem cards and then distribute troops."""
    
    my_territories = game.state.get_territories_owned_by(game.state.me.player_id)
    bordering_territories = game.state.get_all_adjacent_territories(my_territories)

    def can_attack(attacker: int, defender: int) -> bool:
        attacker_troops = game.state.territories[attacker].troops
        defender_troops = game.state.territories[defender].troops

        # Calculate a basic win probability (simplified, for example purposes)
        win_probability = min(1, attacker_troops / (attacker_troops + defender_troops))  # This is a very simplified win probability

        return attacker_troops >= 4 and attacker_troops > defender_troops and win_probability > 0.6

    def find_enemy_to_eliminate() -> Optional[int]:
        for player in game.state.players.values():
            if player.player_id == game.state.me.player_id:
                continue
            if len(game.state.get_territories_owned_by(player.player_id)) == 1:
                return player.player_id
        return None

    def find_critical_continent_territory() -> Optional[int]:
        for continent, territories in game.state.map.get_continents().items():
            for territory in territories:
                occupier = game.state.territories[territory].occupier
                if occupier != game.state.me.player_id and len(set(territories) & set(game.state.get_territories_owned_by(occupier))) == len(territories) - 1:
                    return territory
        return None

    def attack_weakest(territories: list[int]) -> Optional[MoveAttack]:
        territories = sorted(territories, key=lambda x: game.state.territories[x].troops)
        for candidate_target in territories:
            candidate_attackers = sorted(list(set(game.state.map.get_adjacent_to(candidate_target)) & set(my_territories)), key=lambda x: game.state.territories[x].troops, reverse=True)
            for candidate_attacker in candidate_attackers:
                if can_attack(candidate_attacker, candidate_target):
                    return game.move_attack(query, candidate_attacker, candidate_target, min(3, game.state.territories[candidate_attacker].troops - 1))
        return None

    # First priority: Eliminate an enemy
    enemy_to_eliminate = find_enemy_to_eliminate()
    if enemy_to_eliminate is not None:
        enemy_territories = list(set(bordering_territories) & set(game.state.get_territories_owned_by(enemy_to_eliminate)))
        move = attack_weakest(enemy_territories)
        if move is not None:
            return move

    # Second priority: Disrupt continent control
    critical_territory = find_critical_continent_territory()
    if critical_territory is not None:
        move = attack_weakest([critical_territory])
        if move is not None:
            return move

    # General strategy: Attack with advantage
    move = attack_weakest(bordering_territories)
    if move is not None:
        return move

    return game.move_attack_pass(query)


def handle_troops_after_attack(game: Game, bot_state: BotState, query: QueryTroopsAfterAttack) -> MoveTroopsAfterAttack:
    """After conquering a territory in an attack, you must move troops to the new territory."""
    
    # First we need to get the record that describes the attack, and then the move that specifies
    # which territory was the attacking territory.
    record_attack = cast(RecordAttack, game.state.recording[query.record_attack_id])
    move_attack = cast(MoveAttack, game.state.recording[record_attack.move_attack_id])

    # We will always move the maximum number of troops we can.
    return game.move_troops_after_attack(query, game.state.territories[move_attack.attacking_territory].troops - 1)


def handle_defend(game: Game, bot_state: BotState, query: QueryDefend) -> MoveDefend:
    """If you are being attacked by another player, you must choose how many troops to defend with."""

    # We will always defend with the most troops that we can.

    # First we need to get the record that describes the attack we are defending against.
    move_attack = cast(MoveAttack, game.state.recording[query.move_attack_id])
    defending_territory = move_attack.defending_territory
    
    # We can only defend with up to 2 troops, and no more than we have stationed on the defending
    # territory.
    defending_troops = min(game.state.territories[defending_territory].troops, 2)
    return game.move_defend(query, defending_troops)


def handle_fortify(game: Game, bot_state: BotState, query: QueryFortify) -> Union[MoveFortify, MoveFortifyPass]:
    """At the end of your turn, after you have finished attacking, you may move a number of troops between
    any two of your territories (they must be adjacent)."""


    # We will always fortify towards the most powerful player (player with most troops on the map) to defend against them.
    my_territories = game.state.get_territories_owned_by(game.state.me.player_id)
    total_troops_per_player = {}
    for player in game.state.players.values():
        total_troops_per_player[player.player_id] = sum([game.state.territories[x].troops for x in game.state.get_territories_owned_by(player.player_id)])

    most_powerful_player = max(total_troops_per_player.items(), key=lambda x: x[1])[0]

    # If we are the most powerful, we will pass.
    if most_powerful_player == game.state.me.player_id:
        return game.move_fortify_pass(query)
    
    # Otherwise we will find the shortest path between our territory with the most troops
    # and any of the most powerful player's territories and fortify along that path.
    candidate_territories = game.state.get_all_border_territories(my_territories)
    most_troops_territory = max(candidate_territories, key=lambda x: game.state.territories[x].troops)

    # To find the shortest path, we will use a custom function.
    shortest_path = find_shortest_path_from_vertex_to_set(game, most_troops_territory, set(game.state.get_territories_owned_by(most_powerful_player)))
    # We will move our troops along this path (we can only move one step, and we have to leave one troop behind).
    # We have to check that we can move any troops though, if we can't then we will pass our turn.
    if len(shortest_path) > 0 and game.state.territories[most_troops_territory].troops > 1:
        return game.move_fortify(query, shortest_path[0], shortest_path[1], game.state.territories[most_troops_territory].troops - 1)
    else:
        return game.move_fortify_pass(query)


def find_shortest_path_from_vertex_to_set(game: Game, source: int, target_set: set[int]) -> list[int]:
    """Used in move_fortify()."""

    # We perform a BFS search from our source vertex, stopping at the first member of the target_set we find.
    queue = deque()
    queue.appendleft(source)

    current = queue.pop()
    parent = {}
    seen = {current: True}

    while len(queue) != 0:
        if current in target_set:
            break

        for neighbour in game.state.map.get_adjacent_to(current):
            if neighbour not in seen:
                seen[neighbour] = True
                parent[neighbour] = current
                queue.appendleft(neighbour)

        current = queue.pop()

    path = []
    while current in parent:
        path.append(current)
        current = parent[current]

    return path[::-1]

if __name__ == "__main__":
    main()