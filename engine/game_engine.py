import random
from typing import Tuple
from engine.config.gameconfig import NUM_PLAYERS
from collections import deque

from engine.connection.player_connection import PlayerConnection
from engine.exceptions import EngineException
from engine.game.player import Player
from engine.game.state import State
from engine.game.attackhelper import AttackHelper
from engine.records.record_start_turn import RecordStartTurn

def get_next_turn(state: State, connections: dict[int, PlayerConnection], turn_order: deque[int]) -> Tuple[Player, PlayerConnection]:
        player_id = turn_order.pop()
        turn_order.appendleft(player_id)
        player = state.players[player_id]
        connection = connections[player_id]

        return (player, connection)


class GameEngine:
    def __init__(self):
        self.state = State()
        self.connections = dict([(x, PlayerConnection(player_id=x)) for x in self.state.players.keys()])

        turn_order = list(self.state.players.keys())
        random.shuffle(turn_order)
        self.turn_order = deque(turn_order)


    def start(self):
        try:
            self._run_game()
        except EngineException as e:
            # Terminate with a result.json blaming the faulty player.
            pass


    def _start_claim_territories_phase(self):
        turn_order = self.turn_order.copy()

        while len(list(filter(lambda x: x.occupier == None, self.state.territories.values()))) > 0:
            _, connection = get_next_turn(self.state, self.connections, turn_order)
            response = connection.query_claim_territory(self.state)
            response.commit(self.state)


    def _start_place_initial_troops_phase(self):
        turn_order = self.turn_order.copy()

        while len(list(filter(lambda x: x.troops_remaining > 0, self.state.players.values()))) > 0:
            player, connection = get_next_turn(self.state, self.connections, turn_order)

            if player.troops_remaining == 0:
                continue

            response = connection.query_place_initial_troop(self.state)
            response.commit(self.state)


    def _troop_phase(self, player: Player, connection: PlayerConnection):
        
        # Emit a RecordStartTurn.
        record = RecordStartTurn.factory(self.state, player.player_id)
        record.commit(self.state)

        # Let the player redeem cards.
        response = connection.query_redeem_cards(self.state)
        response.commit(self.state)

        # Let the player distribute troops.
        response = connection.query_distribute_troops(self.state)
        response.commit(self.state)


    def _attack_phase(self, player, connection):

        while (True):
            if not AttackHelper.can_player_attack(player, self.state):
                break
            response = connection.query_attack_territory(self.state)
            if response.is_finished:
                break

            opponent_response = self.connections[response.opponent_id].query_defend(response.target_territory, response.num_troops)
            roll = AttackHelper.roll(response.num_troops, opponent_response.num_troops)
            for result in roll:
                if result:
                    # subtract from opponent
                    self.state.territories[response.opponent_id]
                else:
                    # subtract from player
                    player.t
            
            if response.target_territory.troops == 0:
                query_conquered


    def _fortify_phase(self, player: Player, connection: PlayerConnection):
        if player.troops_remaining == 0:
            return
        
        response = connection.query_fortify(self.state)

        # player moves <troops> number of troops from <source_territory_id> to <target_territory_id
        source_territory = self.state.territories[response.source_territory_id]
        target_territory = self.state.territories[response.target_territory_id]
        troops = response.troops

        source_territory.troops -= troops
        target_territory.troops += troops


    def _run_game(self):

        # Commit the 

        self._start_claim_territories_phase()
        self._start_place_initial_troops_phase()

        print(f"Starting game...")

        # Main game loop phase.
        turn_order = self.turn_order.copy()
        while len(list(filter(lambda x: x.alive == True, self.state.players.values()))) > 1:
            
            player, connection = get_next_turn(self.state, self.connections, turn_order)
            # Troop phase.
            # ...

            # Attack phase.
            # ...

            # Fortification phase.
            self._fortify_phase(player, connection)

        # Game ended.
        winner = filter(lambda x: x.alive == True, self.state.players.values()).__next__().player_id

        # Terminate successfully.

        