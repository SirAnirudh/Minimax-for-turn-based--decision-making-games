from typing import Any, List
import random
from stack import Stack

class Playstyle:
    """
    The Playstyle superclass.

    is_manual - Whether the class is a manual Playstyle or not.
    battle_queue - The BattleQueue corresponding to the game this Playstyle is
                   being used in.
    """
    is_manual: bool
    battle_queue: 'BattleQueue'

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this Playstyle with BattleQueue as its battle queue.
        """
        self.battle_queue = battle_queue
        self.is_manual = True

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.
        """
        raise NotImplementedError

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this Playstyle which uses the BattleQueue
        new_battle_queue.
        """
        raise NotImplementedError

class ManualPlaystyle(Playstyle):
    """
    The ManualPlaystyle. Inherits from Playstyle.
    """

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        parameter represents a key pressed by a player.

        Return 'X' if a valid move cannot be found.
        """
        if parameter in ['A', 'S']:
            return parameter

        return 'X'

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this ManualPlaystyle which uses the
        BattleQueue new_battle_queue.
        """
        return ManualPlaystyle(new_battle_queue)

class RandomPlaystyle(Playstyle):
    """
    The Random playstyle. Inherits from Playstyle.
    """
    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this RandomPlaystyle with BattleQueue as its battle queue.
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.
        """
        actions = self.battle_queue.peek().get_available_actions()

        if not actions:
            return 'X'

        return random.choice(actions)

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this RandomPlaystyle which uses the
        BattleQueue new_battle_queue.
        """
        return RandomPlaystyle(new_battle_queue)

def get_state_score(battle_queue: 'BattleQueue') -> int:
    """
    Return an int corresponding to the highest score that the next player in
    battle_queue can guarantee.

    For a state that's over, the score is the HP of the character who still has
    HP if the next player who was supposed to act is the winner. If the next
    player who was supposed to act is the loser, then the score is -1 * the
    HP of the character who still has HP. If there is no winner (i.e. there's
    a tie) then the score is 0.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Rogue, Mage
    >>> bq = BattleQueue()
    >>> r = Rogue("r", bq, ManualPlaystyle(bq))
    >>> m = Mage("m", bq, ManualPlaystyle(bq))
    >>> r.enemy = m
    >>> m.enemy = r
    >>> bq.add(r)
    >>> bq.add(m)
    >>> m.set_hp(3)
    >>> get_state_score(bq)
    100
    >>> r.set_hp(40)
    >>> get_state_score(bq)
    40
    >>> bq.remove()
    r (Rogue): 40/100
    >>> bq.add(r)
    >>> get_state_score(bq)
    -10
    """

    first_player = battle_queue.peek().get_name()

    j = battle_queue.copy()
    return max(producer(j, first_player))




def producer(battle_queue, first_player) -> List:

    """
    returns the scores of each move for first_player

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Rogue, Mage

    >>> bq = BattleQueue()
    >>> r = Rogue("r", bq, ManualPlaystyle(bq))
    >>> mage = Mage("m", bq, ManualPlaystyle(bq))
    >>> r.enemy = mage
    >>> mage.enemy = r

    >>> r.set_hp(30)
    >>> r.set_sp(3)
    >>> mage.set_hp(7)
    >>> mage.set_sp(30)

    >>> bq.add(mage)
    >>> bq.add(r)
    >>> producer(bq, bq.peek().get_name())
    [-20, 7]
    """


    if battle_queue.is_over():
        if not battle_queue.get_winner():
            return [0]
        elif battle_queue.get_winner().get_name() == first_player:

            return [battle_queue.get_winner().get_hp()]

        return [battle_queue.get_winner().get_hp() * -1]
    accumulator = []

    o = battle_queue.peek()

    actions = o.get_available_actions()
    copy_cat = [battle_queue.copy()] * len(actions)
    m = [j.copy() for j in copy_cat]

    for i in range(len(actions)):
        m2 = m[i].peek()



        mover(actions[i], m2)

        #m[i]._content = m[i]._content[1::]

        if not m[i].is_empty():
            m[i].remove()



    for i in m:
        accumulator += [max(producer(i, first_player))]

    return accumulator

def mover(action, character) -> None:
    """
    maakes the appropriate move for character based on action

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Rogue, Mage

    >>> bq = BattleQueue()
    >>> r = Rogue("r", bq, ManualPlaystyle(bq))
    >>> mage = Mage("m", bq, ManualPlaystyle(bq))
    >>> r.enemy = mage
    >>> mage.enemy = r
    >>> mover('A', r)
    >>> r.get_sp() == 97
    True
    """

    if action == 'A':
        character.attack()
    elif action == 'S':
        character.special_attack()





def itarate_the_recursion(battle_queue) -> List:

    """
    returns a list containing all state scores in every level

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Rogue, Mage
    >>> bq = BattleQueue()
    >>> r = Rogue("r", bq, ManualPlaystyle(bq))
    >>> mage = Mage("m", bq, ManualPlaystyle(bq))
    >>> r.enemy = mage
    >>> mage.enemy = r
    >>> r.set_hp(30)
    >>> r.set_sp(3)
    >>> mage.set_hp(7)
    >>> mage.set_sp(30)
    >>> bq.add(mage)
    >>> bq.add(r)
    >>> itarate_the_recursion(bq)[1]
    7
    """

    score = None
    name = 1
    children = []
    m = [name, score, battle_queue, children]
    thing = Stack()
    thing.add(m)
    first_player = battle_queue.peek().get_name()


    while not thing.is_empty():

        x = thing.remove()


        if x[2].is_over():
            if x[2].get_winner():
                winner_hp = x[2].get_winner().get_hp()
                x[1] = winner_hp if x[2].get_winner().get_name() \
                                    == first_player else winner_hp * -1
            else:
                x[1] = 0

        elif x[1] is None and x[3] != []:
            j = []
            for i in x[3]:
                j += [i[1]]
            x[1] = max(j)


        elif not x[2].is_over():
            thing.add(x)

            moves = x[2].peek().get_available_actions()

            for i in moves:
                name += 1

                clone = x[2].copy()
                next_char = clone.peek()

                mover(i, next_char)

                if not clone.is_empty():
                    clone.remove()

                new_tree = [name, None, clone, []]

                x[3].append(new_tree)
                thing.add(new_tree)
    return m


class RecursiveMiniMax(Playstyle):
    """
    The Recursive Playstyle. Inherits from Playstyle.
    """

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this RecursiveMinimax with BattleQueue as its battle queue.
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        parameter represents a key pressed by a player.

        Return 'X' if a valid move cannot be found.
        """
        move = get_state_score(self.battle_queue)
        potentials = self.battle_queue.peek().get_available_actions()

        if (potentials) == []:
            return 'X'

        who = producer(self.battle_queue.copy(),
                       self.battle_queue.peek().get_name())

        x = who.index(move)

        return potentials[x]

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this Recursive Minimax which uses the
        BattleQueue new_battle_queue.
        """
        return RecursiveMiniMax(new_battle_queue)

class IterativeMiniMax(Playstyle):
    """
    The Itarative Playstyle. Inherits from Playstyle.
    """

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this Iterative minimax with BattleQueue as its battle queue.
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        parameter represents a key pressed by a player.

        Return 'X' if a valid move cannot be found.
        """
        move = itarate_the_recursion(self.battle_queue)[1]

        potentials = self.battle_queue.peek().get_available_actions()

        if (potentials) == []:
            return potentials[0]
        elif (potentials) == []:
            return 'X'

        m = []
        for i in itarate_the_recursion(self.battle_queue)[3]:
            m += [i[1]]
        return potentials[m.index(move)]



    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this Itarative minimax which uses the
        BattleQueue new_battle_queue.
        """
        return IterativeMiniMax(new_battle_queue)
