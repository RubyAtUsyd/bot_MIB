import random
import shutil
from typing import Tuple
from collections import deque

from risk_engine.config.gameconfig import MAX_GAME_RECORDING_SIZE
from risk_engine.config.ioconfig import CORE_DIRECTORY
from risk_engine.connection.player_connection import PlayerConnection
from risk_engine.exceptions import PlayerException
from risk_engine.game.record_factory import record_attack_factory, record_banned_factory, record_drew_card_factory, record_player_eliminated_factory, record_start_turn_factory
from risk_engine.game.state import State
from risk_engine.game.state_mutator import StateMutator
from risk_engine.output.game_result import GameBanResult, GameSuccessResult
from risk_engine.output.recording_inspector import RecordingInspector
from risk_engine.validation.move_validator import MoveValidator
from risk_shared.models.player_model import PlayerModel
from risk_shared.records.record_shuffled_cards import RecordShuffledCards
from risk_shared.records.record_start_game import RecordStartGame
from risk_shared.records.record_territory_conquered import RecordTerritoryConquered
from risk_shared.records.record_winner import RecordWinner

def get_next_turn(state: State, connections: dict[int, PlayerConnection], turn_order: deque[int]) -> Tuple[PlayerModel, PlayerConnection]:
        player_id = turn_order.pop()
        turn_order.appendleft(player_id)
        player = state.players[player_id]
        connection = connections[player_id]

        return (player, connection)


class GameEngine:
    def __init__(self):
        self.state = State()
        self.mutator = StateMutator(self.state)
        self.validator = MoveValidator(self.state)
        self.connections: dict[int, PlayerConnection]

    def start(self):
        try:
            self._connect()
            self._run_game()
        except PlayerException as e:
            record = record_banned_factory(e)
            self.mutator.commit(record)

        self._finish()


    def _connect(self):
        self.connections = dict([(x, PlayerConnection(player_id=x)) for x in self.state.players.keys()])


    def _finish(self):

        # Write the result.
        inspector = RecordingInspector(self.state.recording)
        result = inspector.get_result()

        with open(f"{CORE_DIRECTORY}/output/results.json", "w") as f:
            f.write(result.model_dump_json())

        # Write the game log.
        with open(f"{CORE_DIRECTORY}/output/game.log", "w") as f:
            f.write(inspector.get_recording_json())

        def copy_stdout_stderr_player(player: int):
            stderr_path = f"{CORE_DIRECTORY}/submission{player}/io/submission.err"
            stderr_path_new = f"{CORE_DIRECTORY}/output/submission_{player}.err"
            stdout_path = f"{CORE_DIRECTORY}/submission{player}/io/submission.log"
            stdout_path_new = f"{CORE_DIRECTORY}/output/submission_{player}.log"

            try:
                shutil.copy(stderr_path, stderr_path_new, follow_symlinks=False)
            except (FileNotFoundError, IsADirectoryError, FileExistsError):
                with open(stderr_path_new, "w") as f:
                    f.write("Your submission.err file is either missing or is a directory.")
            
            try:
                shutil.copy(stdout_path, stdout_path_new, follow_symlinks=False)
            except (FileNotFoundError, IsADirectoryError, FileExistsError):
                with open(stdout_path_new, "w") as f:
                    f.write("Your submission.log file is either missing or is a directory.")


        # Only copy for the player who was banned, otherwise copy for all players.
        match result:
            case GameBanResult() as x:
                copy_stdout_stderr_player(player=x.player)

            case GameSuccessResult():
                for player in self.state.players.keys():
                    copy_stdout_stderr_player(player)


    def _run_game(self):
        
        # Emit RecordStartGame.
        turn_order = list(self.state.players.keys())
        random.shuffle(turn_order)
        self.state.turn_order = turn_order
        record_start_game = RecordStartGame(turn_order=self.state.turn_order.copy(), players=list(self.state.players.values()))
        self.mutator.commit(record_start_game)

        # Emit RecordShuffledCards.
        record_shuffled_cards = RecordShuffledCards()
        self.mutator.commit(record_shuffled_cards)

        # Run the initial phases.
        self._start_claim_territories_phase()
        self._start_place_initial_troops_phase()

        # Run the main game.
        turn_order = deque(self.state.turn_order.copy())
        while len(list(filter(lambda x: x.alive == True, self.state.players.values()))) > 1 and len(self.state.recording) < MAX_GAME_RECORDING_SIZE:
            
            player, connection = get_next_turn(self.state, self.connections, turn_order)
            if not player.alive: continue

            self._troop_phase(player, connection)
            self._attack_phase(player, connection)
            self._fortify_phase(player, connection)

        # Emit RecordWinner.
        winner = filter(lambda x: x.alive == True, self.state.players.values()).__next__().player_id
        record = RecordWinner(player=winner)
        self.mutator.commit(record)



    def _start_claim_territories_phase(self):
        turn_order = deque(self.state.turn_order.copy())

        while len(list(filter(lambda x: x.occupier == None, self.state.territories.values()))) > 0:
            player, connection = get_next_turn(self.state, self.connections, turn_order)
            response = connection.query_claim_territory(self.state, self.validator)
            self.mutator.commit(response)


    def _start_place_initial_troops_phase(self):
        turn_order = deque(self.state.turn_order.copy())

        while len(list(filter(lambda x: x.troops_remaining > 0, self.state.players.values()))) > 0:
            player, connection = get_next_turn(self.state, self.connections, turn_order)

            if player.troops_remaining == 0:
                continue

            response = connection.query_place_initial_troop(self.state, self.validator)
            self.mutator.commit(response)


    def _troop_phase(self, player: PlayerModel, connection: PlayerConnection):
        
        # Emit a RecordStartTurn.
        record = record_start_turn_factory(self.state, player.player_id)
        self.mutator.commit(record)

        # Let the player redeem cards.
        response = connection.query_redeem_cards(self.state, self.validator, cause="turn_started")
        self.mutator.commit(response)

        # Let the player distribute troops.
        response = connection.query_distribute_troops(self.state, self.validator, cause="turn_started")
        self.mutator.commit(response)


    def _attack_phase(self, player: PlayerModel, connection: PlayerConnection):

        conquered_territory = False
        while (True):

            # Get the attack move.
            attack = connection.query_attack(self.state, self.validator)
            self.mutator.commit(attack)
            move_attack_id = len(self.state.recording) - 1

            # If the player passes, move to the next phase.
            if attack.move == "pass":
                break
            
            defending_player = self.state.territories[attack.move.defending_territory].occupier
            if defending_player == None:
                raise RuntimeError("Tried to attack unoccupied territory.")

            # Get the defend move.
            defend = self.connections[defending_player].query_defend(self.state, self.validator, move_attack_id)
            self.mutator.commit(defend)
            move_defend_id = len(self.state.recording) - 1

            # Emit the RecordAttack.
            record_attack = record_attack_factory(state=self.state, move_attack_id=move_attack_id, move_defend_id=move_defend_id)
            self.mutator.commit(record_attack)
            record_attack_id = len(self.state.recording) - 1

            # Emit a RecordTerritoryConquered and then allow player to move troops.
            if record_attack.territory_conquered:
                conquered_territory = True

                record = RecordTerritoryConquered(record_attack_id=record_attack_id)
                self.mutator.commit(record)

                response = connection.query_troops_after_attack(self.state, self.validator, record_attack_id)
                self.mutator.commit(response)

            # Emit a RecordPlayerEliminated and then allow player to redeem cards and distribute troops if required.
            if record_attack.defender_eliminated:
                record = record_player_eliminated_factory(self.state, move_defend_id, defending_player)
                self.mutator.commit(record)

                if len(player.cards) > 6:
                    response = connection.query_redeem_cards(self.state, self.validator, cause="player_eliminated")
                    self.mutator.commit(response)

                    response = connection.query_distribute_troops(self.state, self.validator, cause="player_eliminated")
                    self.mutator.commit(response)

        # If the player conquered any territories this turn, they draw a card.
        # Shuffle the deck first if necessary.
        if len(self.state.deck) == 0:
            record = RecordShuffledCards()
            self.mutator.commit(record)
        
        record = record_drew_card_factory(self.state, player.player_id)
        self.mutator.commit(record)


    def _fortify_phase(self, player: PlayerModel, connection: PlayerConnection):
        response = connection.query_fortify(self.state, self.validator)
        self.mutator.commit(response)
        