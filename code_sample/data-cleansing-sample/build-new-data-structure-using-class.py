# Advanced example of using class to group data.

import datetime
import numpy as np


class Player(object):
    """
    Player contains given, family_name, set_family_name,
    starting_year, birthdate, and current_salary infomation.

    Function: calculate playing history, calculate age.
    """
    # Part 1: initialization
    def __init__(self, family_name, given_name,
                 starting_year, birthdate, current_salary):
        self.family_name = None
        self.set_family_name(family_name)

        self.given_name = None
        self.set_given_name(given_name)

        self.starting_year = None
        self.set_starting_year(starting_year)

        self.birthdate = None
        self.set_birthdate(birthdate)

        self.current_salary = None
        self.set_salary(current_salary)

    # Part 2: get and set values
    def set_salary(self, current_salary):
        if not (isinstance(current_salary, int) or
                isinstance(current_salary, float)) or \
                current_salary < 0:
            raise ValueError("current salary is not a " +
                             "number or has value less than zero")
        self.current_salary = current_salary

    def set_birthdate(self, birthdate):
        """
        :param birthdate:
        :return: calculate current age
        """
        try:
            self.birthdate = datetime.datetime.strptime(
                             birthdate, '%m/%d/%Y').date()
        except ValueError:
            raise ValueError("date format does not match '/mm/dd/yyyy'")

    def set_starting_year(self, starting_year):
        try:
            self.starting_year = datetime.datetime.strptime(
                                 starting_year, '%m/%d/%Y').date()
        except ValueError:
            raise ValueError("date format does not match '/mm/dd/yyyy'")

    def set_family_name(self, family_name):
        if not isinstance(family_name, str):
            raise ValueError("family name is not a string")
        self.family_name = family_name

    def set_given_name(self, given_name):
        if not isinstance(given_name, str):
            raise ValueError("given name is not a string")
        self.given_name = given_name

    def get_family_name(self):
        return self.family_name

    def get_given_name(self):
        return self.given_name

    def get_starting_year(self):
        return self.starting_year()

    def get_birthdate(self):
        return self.birthdate()

    def get_current_salary(self):
        return self.current_salary

    # Part 3: calculate current age
    # citation: https://stackoverflow.com/questions/2217488
    #           /age-from-birthdate-in-python
    def get_current_age(self):
        today = datetime.date.today()
        return today.year - self.birthdate.year \
               - ((today.month, today.day)
               < (self.birthdate.month, self.birthdate.day))

    def get_play_history(self):
        today = datetime.date.today()
        return today.year - self.starting_year.year \
               - ((today.month, today.day)
               < (self.starting_year.month, self.starting_year.day))

    # Part 4: get full name
    def get_name(self):
        return self.given_name + " " + self.family_name

    # Part 5: show how to reconstruct a player
    def __repr__(self):
        """ how to reconstruct a Player"""
        return "Player(family_name=" + str(self.family_name) + \
               ", given_name=" + str(self.given_name) + \
               ", starting_year=" + str(self.starting_year) + \
               ", birthdate=" + str(self.starting_year) + \
               ", current salary=" + str(self.current_salary) + ")"

    # Part 6: show all the information
    def __str__(self):
        """ shows all information in a human readable sentence"""
        return "Player's family_name is" + str(self.family_name) + \
               ", given_name is" + str(self.given_name) + \
               ", starting_year is" + str(self.starting_year) + \
               ", birthdate is" + str(self.starting_year) + \
               ", current salary is" + str(self.current_salary)

    # Part 7: comparison age
    # if one's age is bigger, his birthday should be earlier
    def __eq__(self, other):
        """ Define equality as same birthdate"""
        return self.birthdate == other.birthdate

    def __lt__(self, other):
        """ Birthdate based '<' """
        return self.birthdate > other.birthdate

    def __ne__(self, other):
        """ Inequality based on different birthdate """
        return self.birthdate != other.birthdate

    def __gt__(self, other):
        """ Birthdate based '>' """
        return self.birthdate < other.birthdate

    def __le__(self, other):
        """ Birthdate based '<=' """
        return self.birthdate >= other.birthdate

    def __ge__(self, other):
        """ Birthdate based '>=' """
        return self.birthdate <= other.birthdate


class Team(object):
    """
    Team contains team_name and a player_list.
    Function: trade players, iteration over the player_list,
              remove players etc.
    """
    # Part 1: initialization
    def __init__(self, team_name):
        self.team_name = None
        self.set_team_name(team_name)
        self.player_list = []

    def set_team_name(self, team_name):
        if not isinstance(team_name, str):
            raise ValueError("team name is not a string")
        self.team_name = team_name

    # Part 2: access team name
    def get_team_name(self):
        return self.team_name

    # Part 3: add players
    def add_players(self, all_player):
        if isinstance(all_player, list) or \
                isinstance(all_player, tuple):
            for player in all_player:
                if isinstance(player, Player):
                    is_dup, _ = self.duplicate_player(player)
                    if is_dup == 1:
                        raise ValueError("this playe is "
                                         "already in the list")
                    self.player_list.append(player)
                else:
                    raise ValueError("there is non-Player "
                                     "type data in the list")

        elif isinstance(all_player, Player):
            is_dup, _ = self.duplicate_player(all_player)
            if is_dup == 1:
                raise ValueError("this playe is"
                                 " already in the list")
            self.player_list.append(all_player)
        else:
            raise ValueError("input is not "
                             "a Player type data")

    def duplicate_player(self, new_player):
        for i in range(len(self.player_list)):
            if (self.player_list[i].get_name()
                    == new_player.get_name() and
                self.player_list[i].birthdate
                    == new_player.birthdate):
                return 1, i
        return 0, None

    # Part 4: remove players
    def remove_players(self, rm_players):
        if isinstance(rm_players, list) or \
                isinstance(rm_players, tuple):
            for player in rm_players:
                if isinstance(player, Player):
                    is_dup, idx = self.duplicate_player(player)
                    if is_dup == 0:
                        raise ValueError("this player "
                                         "is not in the list")
                    self.player_list.pop(idx)
                else:
                    raise ValueError("there is non-Player"
                                     " type data in the list")

        elif isinstance(rm_players, Player):
            is_dup, idx = self.duplicate_player(rm_players)
            if is_dup == 0:
                raise ValueError("this playe "
                                 "is already in the list")
            self.player_list.pop(idx)
        else:
            raise ValueError("there is non-Player "
                             "type data in the input")

    # Part 5: construct len
    def __len__(self):
        """ Length define as number of players """
        return len(self.player_list)

    # Part 6: make str method
    def __str__(self):
        """ some infomation about team name and Number of players"""
        return self.team_name + " has" + \
               len(self.player_list) + " players"

    # Part 7: trade players
    def trade_players(self, other, trade_players):
        if isinstance(trade_players, list) or \
                isinstance(trade_players, tuple):
            for player in trade_players:
                if not isinstance(player, Player):
                    raise ValueError("there is non-Player "
                                     "type data in the input")
                else:
                    is_dup1, _ = self.duplicate_player(player)
                    is_dup2, _ = other.duplicate_player(player)
                    print(is_dup1, is_dup2)

                    if is_dup1 == 0 and is_dup2 == 1:
                        other.remove_players(player)
                        self.add_players(player)

                    elif is_dup1 == 1 and is_dup2 == 0:
                        self.add_players(player)
                        other.remove_players(player)

                    else:
                        raise ValueError("this player can "
                                         "not be trade because"
                                         "he is not in the two teams or"
                                         "he is in both two teams")

        elif not isinstance(trade_players, Player):
            raise ValueError("there is non-Player"
                             " type data in the input")

        else:
            is_dup1, _ = self.duplicate_player(trade_players)
            is_dup2, _ = other.duplicate_player(trade_players)

            if is_dup1 == 0 and is_dup2 == 1:
                other.remove_players(trade_players)
                self.add_players(trade_players)

            elif is_dup1 == 1 and is_dup2 == 0:
                self.add_players(trade_players)
                other.remove_players(trade_players)

            else:
                raise ValueError("this player can not be trade because"
                                 "he is not in the two teams or"
                                 "he is in both two teams")

        return self

    # Part 8: for loop regarding player
    def __iter__(self):
        """ Silly implementation of the first half of iteration """
        self.__index = 0
        return self

    def __next__(self):
        """ Silly implementation of the second half of iteration """
        if self.__index >= len(self.player_list)\
                or self.player_list == []:
            raise StopIteration
        self.__index = self.__index + 1
        return self.player_list[self.__index - 1]

    # Part 9: stats information
    def stats(self):
        salary = [player.current_salary
                  for player in self.player_list]
        total_salary = np.sum(salary)

        age = [player.get_current_age()
               for player in self.player_list]
        mean_age = np.average(age)

        history = [player.get_play_history()
                   for player in self.player_list]
        mean_history = np.average(history)

        return (total_salary, mean_age, mean_history)


if __name__ == '__main__':
    # test class Player
    try:
        player = Player(family_name="AA", given_name="BB",
                        starting_year="2/02/2002",
                        birthdate="2/02/1992",
                        current_salary="100")
    except ValueError:
        print(ValueError)

    player = Player(family_name="AA", given_name="BB",
                    starting_year="2/02/2002",
                    birthdate="2/02/1992",
                    current_salary=100)

    player2 = Player(family_name="CC", given_name="BB",
                     starting_year="2/02/2002",
                     birthdate="2/01/1992",
                     current_salary=100)

    # 16, 26, AA BB, False
    print(player.get_play_history(), player.get_current_age(),
          player.get_name(), player2 < player)

    # test class Team

    team = Team("mayjiang")
    team.add_players([player, player2])

    try:
        team.add_players(player)
    except ValueError:
        print(ValueError)

    player3 = Player(family_name="DD", given_name="BB",
                     starting_year="2/02/2002",
                     birthdate="2/01/1992",
                     current_salary=100)

    team2 = Team("liangliang")
    team2.add_players(player3)

    team.remove_players(player)
    team = team.trade_players(team2, player3)
    print(team.player_list, team2.player_list)
    print(team.stats())  # (200, 26.0, 16.0)

    for player in team:
        print(player.get_name())  # BB CC , BB DD
