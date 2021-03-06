##############################################
#             Tic Tac Toe                    #
##############################################
# class Board is the class that is responsible for Board printing and
# check if some player won

import time

class Board(object):
    # costructor with board object
    def __init__(self):
        self.board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    # Checks if player has this position
    def HasPosition(self, row, col, player_id):
        return self.board[row][col] == player_id

    # Return row and col for a position
    def ToRow(self, position):
        position = int(position)
        return int(position / 3)

    def ToCol(self, position):
        position = int(position)
        return int(position % 3)

    # Print board  for each round
    def Print(self):
        print("Note the bord:\n"
              "   " +
              "\033[4m" +
              str(self.board[0][0]) +
              "/" +
              str(self.board[0][1]) +
              "/" +
              str(self.board[0][2]) +
              "\n" +
              "\033[0m" +
              "  " +
              "\033[4m" +
              str(self.board[1][0]) +
              "/" +
              str(self.board[1][1]) +
              "/" +
              str(self.board[1][2]) +
              "\n" +
              "\033[0m" +
              " " +
              "\033[4m" +
              str(self.board[2][0]) +
              "/" +
              str(self.board[2][1]) +
              "/" +
              str(self.board[2][2]) +
              "\n" +
              "\033[0m")

    # Checks if position is free
    def IsFree(self, row, col):
        return str(self.board[row][col]).isdigit()

    def PrintMessage(self, row, col):
        print("Position " + str(row * 3 + col) + " is not free")

    # put player_id in a position
    def PlayPosition(self, row, col, player_id):
        if self.IsFree(row, col):
            self.board[row][col] = player_id
            return True
        self.PrintMessage(row, col)
        self.Print()
        return False

    # Check if player won with in line
    def WonWithRow(self, player_id):
        for col in range(3):
            player_has_all_positions = True
            for row in range(3):
                player_has_this_position = (
                    self.HasPosition(row, col, player_id))
                player_has_all_positions &= player_has_this_position
            if player_has_all_positions:
                return True
        return False

    # Check if player won with in col
    def WonWithCol(self, player_id):
        for row in range(3):
            player_has_all_positions = True
            for col in range(3):
                # Call HasPosition().... Here and other places. ok
                player_has_this_position = (
                    self.HasPosition(row, col, player_id))
                player_has_all_positions &= player_has_this_position
            if player_has_all_positions:
                return True
        return False

    # Check if player won with in tranversal
    def WonWithTransversal(self, player_id):
        player_has_all_positions = True
        for transversal in range(3):
            player_has_this_position = (
                self.HasPosition(
                    transversal,
                    transversal,
                    player_id))
            player_has_all_positions &= player_has_this_position
        if player_has_all_positions:
            return True
        player_has_all_positions = True
        for transversal in range(3):
            player_has_this_position = (
                self.HasPosition(
                    transversal,
                    2 - transversal,
                    player_id))
            player_has_all_positions &= player_has_this_position
        if player_has_all_positions:
            return True
        return False

    # Check if player won in any direction
    def PlayerWon(self, player_id):
        return self.WonWithRow(player_id) or self.WonWithCol(
            player_id) or self.WonWithTransversal(player_id)


class Player(object):
    # this class is responsible for manage the plays
    def __init__(self, player_id):
        self.player_id = player_id

    # Get Position, validate, modify tic tac toe
    def Play(self, tic_tac_toe):
        tic_tac_toe.Print()
        is_valid = False
        while not is_valid:
            position = self.ChoicePosition(tic_tac_toe)
            if self.IsValid(tic_tac_toe, position):
                # Row -> row, Col -> col (style guide) ok
                row = tic_tac_toe.ToRow(position)
                col = tic_tac_toe.ToCol(position)
                is_valid = tic_tac_toe.PlayPosition(row, col, self.Id())

    def Id(self):
        return self.player_id

    # Subclasses must implement this.
    def IsValid(self, tic_tac_toe, value):
        return True


# This class is responsible for Human player.
class HumanPlayer(Player):
    def __init__(self, player_id):
        Player.__init__(self, player_id)

    # User input a position
    def ChoicePosition(self, tic_tac_toe):
        return input("Enter a position:\n")

    # Checks if position is a number from 0 to 8
    def IsValid(self, tic_tac_toe, position):  # 0-8
        if not position.isdigit():
            print("\"" + position + "\"" + " is not a number from 0 to 8")
            tic_tac_toe.Print()
            return False
        if int(position) < 0 or int(position) > 8:
            print("\"" + position + "\"" + " is not a number from 0 to 8")
            tic_tac_toe.Print()
            return False
        return True


# This class is responsible for computer player and game computer algorithm.
class ComputerPlayer(Player):
    def __init__(self, computer_id, human_id):
        Player.__init__(self, computer_id)
        self.human_id = human_id

    # retur true only to answer "class player"
    def IsValid(self, tic_tac_toe, posicao):
        return True

    # Check if player has 2 position in row, col or tranversal and return a
    # index where is free
    def HasTwoInThreeAndAFree(self, tic_tac_toe, player_id, row_col_list):
        empty_row = None
        empty_col = None
        positions_computer_have = 0
        for row_col in row_col_list:  # for row, col in row_col_list
            row = row_col[0]
            col = row_col[1]
            if tic_tac_toe.HasPosition(row, col, player_id):
                positions_computer_have += 1
            elif tic_tac_toe.IsFree(row, col):
                empty_row = row
                empty_col = col
        if positions_computer_have == 2 and empty_row is not None \
                and empty_col is not None:
            return True, empty_row, empty_col
        return False, None, None

    # check if someone can win
    # Returns:
    #  - True, row, col
    #  - False, None, None
    def PlayerCanWin(self, tic_tac_toe, player_id):
        groups_of_tree = []
        # rows
        for row in range(3):
            row_col_list = []
            for col in range(3):
                row_col_list.append([row, col])
            groups_of_tree.append(row_col_list)
        # columns
        for col in range(3):
            row_col_list = []
            for row in range(3):
                row_col_list.append([row, col])
            groups_of_tree.append(row_col_list)
        # Traversal
        row_col_list = []
        for traversal in range(3):
            row_col_list.append([traversal, traversal])
        groups_of_tree.append(row_col_list)

        row_col_list = []
        for traversal in range(3):
            row_col_list.append([traversal, 2 - traversal])
        groups_of_tree.append(row_col_list)

        # Verify all.
        for tres_posicoes in groups_of_tree:
            can_win, empty_row, empty_col = self.HasTwoInThreeAndAFree(
                tic_tac_toe, player_id, tres_posicoes)
            if can_win:
                return can_win, empty_row, empty_col

        return False, None, None

    # check if computer can win and retur posion to win the game
    def ComputerCanWin(self, tic_tac_toe):
        can_win, row, col = self.PlayerCanWin(tic_tac_toe, self.player_id)
        if can_win:
            return (row * 3 + col)
        return None

    # check if human can win and retur posion to block the game
    def HumanCanWin(self, tic_tac_toe):
        can_win, row, col = self.PlayerCanWin(tic_tac_toe, self.human_id)
        if can_win:
            return (row * 3 + col)
        return None

    # computer play algorithm
    def ChoicePosition(self, tic_tac_toe):
        # Sleep a little, to make the game play more realistic.
        print("Computer thinking...\n")
        time.sleep(1)  # seconds

        if self.ComputerCanWin(tic_tac_toe) is not None:
            return self.ComputerCanWin(tic_tac_toe)

        if self.HumanCanWin(tic_tac_toe) is not None:
            # More readable if you switch the order: ok
            return self.HumanCanWin(tic_tac_toe)

        from random import randint
        while True:
            i = randint(0, 8)
            Row = tic_tac_toe.ToRow(i)
            Col = tic_tac_toe.ToCol(i)
            if tic_tac_toe.IsFree(Row, Col):
                return i


class GamePlay(object):
    def __init__(self):
        self.tic_tac_toe = Board()
        print("Welcome Tic Tac Toe game")

    def PlayerChoice(self):
        while True:
            choice = input("Enter 'X' or 'O' to choose your player:\n")
            if choice.isdigit():
                print("Value is not valid, please choose \"X\" or \"O\"")
            elif not (choice.upper() == "X" or choice.upper() == "O"):
                print("Value is not valid, please choose \"X\" or \"O\"")
            elif choice.upper() == "X":
                human_id = "\033[4m\033[91mX\033[0m\033[4m"
                human_player = HumanPlayer(human_id)
                computer_player = ComputerPlayer(
                    "\033[4m\033[94mO\033[0m\033[4m", human_id)
                return human_player, computer_player, False
                break
            elif choice.upper() == "O":
                human_id = "\033[4m\033[94mO\033[0m\033[4m"
                human_player = HumanPlayer(human_id)
                computer_player = ComputerPlayer(
                    "\033[4m\033[91mX\033[0m\033[4m", human_id)
                return human_player, computer_player, True
                break

    def TheGame(self, player_x, player_o):
        # main code for game
        players = [player_x, player_o]
        round = 0
        while True:
            current_player = players[round % 2]
            round += 1
            # first step is check if it is game end and nobody won
            if round > 9:
                self.tic_tac_toe.Print()
                print("Nobody won!!")
                break
            current_player.Play(self.tic_tac_toe)
            if self.tic_tac_toe.PlayerWon(current_player.Id()):
                self.tic_tac_toe.Print()
                print(current_player.Id() + " Won!")
                break


def main():
    game = GamePlay()

    human_player, computer_player, human_is_o = game.PlayerChoice()

    if (human_is_o):
        game.TheGame(computer_player, human_player)
    else:
        game.TheGame(human_player, computer_player)


if __name__ == "__main__":
    main()
