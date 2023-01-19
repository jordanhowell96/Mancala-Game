# Author: Jordan Howell
# GitHub username: jordanhowell96
# Date: 12/4/2022
# Description: Defines a class for a mancala game as well as a player class and an exception,
# both to be used by the mancala class. A mancala object and its methods may be used to play
# through a virtual game of mancala.

class TooManyPlayersException(Exception):
    """Defines exception for when there is an attempt to add more than 2 players to a Mancala object"""
    pass


class Player:
    """Class defining a mancala player"""

    def __init__(self, player_name, player_number):
        self._name = player_name
        if player_number == 1:
            self._store_index = 6
        else:
            self._store_index = 13

    def get_store_index(self):
        """Get method for the player's store index private data member"""
        return self._store_index

    def get_name(self):
        """Get method for the player's name private data member"""
        return self._name


class Mancala:
    def __init__(self):
        self._board = ([4] * 6 + [0]) * 2
        self._adjacent_indices = {index: adjacent for index, adjacent in zip(range(6), range(12, 6, -1))}
        self._adjacent_indices.update({index: adjacent for adjacent, index in self._adjacent_indices.items()})
        self._players = []

    def get_player_name(self, player_number):
        """Returns the name of a given player number"""
        return self._players[player_number - 1].get_name()

    def create_player(self, player_name):
        """Creates a new player object for the game"""
        if len(self._players) < 2:
            new_player = Player(player_name, len(self._players) + 1)
            self._players.append(new_player)
            return new_player
        else:
            raise TooManyPlayersException

    def get_player_store_index(self, player_number):
        """Returns the store index of a given player number"""
        return self._players[player_number - 1].get_store_index()

    def get_player_store(self, player_number):
        """Returns the number of seeds in a given players store"""
        store_index = self.get_player_store_index(player_number)
        return self._board[store_index]

    def get_player_pits(self, player_number):
        """Returns the pits of a given player number"""
        offset = 7 * (player_number - 1)
        return self._board[offset:6 + offset]

    def print_board(self):
        """Prints out the current state of the board"""
        for player_number in (1, 2):
            print(f"player{player_number}:")
            print(f"store: {self.get_player_store(player_number)}")
            print(self.get_player_pits(player_number))

    def capture_seeds(self, player_number, pit_index):
        """
        Performs a capture of another players seeds according to special rule 2
        given a player number and pit index
        """
        self._board[pit_index] = 0
        adjacent_index = self._adjacent_indices[pit_index]
        captured_seeds = self._board[adjacent_index] + 1
        self._board[adjacent_index] = 0

        store_index = self.get_player_store_index(player_number)
        self._board[store_index] += captured_seeds

    def check_special_rule_2(self, player_number, final_pit_index):
        """Checks if a special rule 2 should be triggered given a player number and pit index"""
        # Check if there is only one seed in the pit (implied that this is the last seed of a move)
        if self._board[final_pit_index] == 1:

            # Check if the pit index is on the side of the player who moved
            if player_number == 1 and final_pit_index <= 5 or \
                    player_number == 2 and 7 <= final_pit_index < 13:
                return True
            else:
                return False

    def clear_pits(self):
        """Clears the board by moving the leftover seeds on each players' side to their pit"""
        # Move seeds into the stores
        for player_number in (1, 2):
            self._board[self.get_player_store_index(player_number)] += sum(self.get_player_pits(player_number))
        # Clear the pits
        for index in range(len(self._board)):
            if index not in (6, 13):
                self._board[index] = 0

    def check_game_over(self):
        """Checks if the game has ended by all pits of one or both players being empty"""
        if 0 in (sum(self.get_player_pits(player)) for player in (1, 2)):
            return True

    def move_seeds(self, player_number, pit_index):
        """Moves the seeds in a given pit by a given player"""
        # Get the amount of seeds to move and set the seed count of the initial pit to 0
        seeds_to_move = self._board[pit_index]
        self._board[pit_index] = 0

        # Move the seeds until there are no more seeds to move
        while seeds_to_move > 0:
            # Increment the pit index
            pit_index += 1

            # Skip the other players pit
            if player_number == 1 and pit_index == 13 or player_number == 2 and pit_index == 6:
                pit_index += 1

            # Reset the pit index if greater than the max index of the board
            if pit_index == len(self._board):
                pit_index = 0

            # Add one seed to the pit and decrement the seeds to move
            self._board[pit_index] += 1
            seeds_to_move -= 1

        return pit_index

    def play_game(self, player_number, pit_number):
        """
        Plays the game by calling relevant functions
        given a player number and the pit number of the seeds to be moved
        """
        if 6 < pit_number or pit_number <= 0:
            return "Invalid number for pit index"

        # If the game is over then return "Game is ended"
        if self.check_game_over() is True:
            return "Game is ended"

        # Convert the pit number to a pit index
        pit_index = pit_number - 1
        if player_number == 2:
            pit_index += 7

        # Move the seeds
        final_pit_index = self.move_seeds(player_number, pit_index)

        # Special Rule 2
        if self.check_special_rule_2(player_number, final_pit_index):
            self.capture_seeds(player_number, final_pit_index)

        # Check if the game is over, and if so then clear the remaining seeds in the pits into the stores
        if self.check_game_over() is True:
            self.clear_pits()

        # Special Rule 1
        if player_number == 1 and pit_index == 6:
            print("player 1 take another turn")
        elif player_number == 2 and pit_index == 13:
            print("player 2 take another turn")

        return self._board

    def return_winner(self):
        """Returns the winner of the game or returns that the game is not ended"""
        # If the game is over then return the winner, otherwise return "Game has not ended"
        if self.check_game_over():
            # Get the players' scores
            player_1_score = self.get_player_store(1)
            player_2_score = self.get_player_store(2)

            # Return the winner
            if player_1_score > player_2_score:
                return f"Winner is player 1: {self.get_player_name(1)}"
            elif player_2_score > player_1_score:
                return f"Winner is player 2: {self.get_player_name(2)}"
            else:
                return "It's a tie"

        else:
            return "Game has not ended"
