from typing import Callable, List
from a2_skills import MageAttack, MageSpecial, RogueAttack, RogueSpecial


class SkillDecisionTree:
    """
    A class representing the SkillDecisionTree used by Sorcerer's in A2.

    value - the skill that this SkillDecisionTree contains.
    condition - the function that this SkillDecisionTree will check.
    priority - the priority number of this SkillDecisionTree.
               You may assume priority numbers are unique (i.e. no two
               SkillDecisionTrees will have the same number.)
    children - the subtrees of this SkillDecisionTree.
    """
    value: 'Skill'
    condition: Callable[['Character', 'Character'], bool]
    priority: int
    children: List['SkillDecisionTree']

    def __init__(self, value: 'Skill',
                 condition: Callable[['Character', 'Character'], bool],
                 priority: int,
                 children: List['SkillDecisionTree'] = None):
        """
        Initialize this SkillDecisionTree with the value value, condition
        function condition, priority number priority, and the children in
        children, if provided.

        >>> from a2_skills import MageAttack
        >>> def f(caster, target):
        ...     return caster.hp > 50
        >>> t = SkillDecisionTree(MageAttack(), f, 1)
        >>> t.priority
        1
        >>> type(t.value) == MageAttack
        True
        """
        self.value = value
        self.condition = condition
        self.priority = priority
        self.children = children[:] if children else []


    def collector(self, caster, target):

        """
        collects all possible moves for a caster and its priorities

        >>> from a2_characters import Rogue
        >>> from a2_battle_queue import BattleQueue


        >>> k = Rogue('x', BattleQueue(), "pop")
        >>> j = Rogue('x', BattleQueue(), "pop")

        >>> p = create_default_tree()

        >>> k.enemy = j
        >>> j.enemy = k

        >>> k._hp = 95
        >>> k._sp = 30
        >>> j._hp = 20
        >>> j._sp = 50

        >>> len(p.collector(k,j)) == 3
        True
        """

        k = []
        if not self.condition(caster, target):
            k += [[self.value, self.priority]]
        else:
            for i in self.children:
                k += i.collector(caster, target)
        return k






    def pick_skill(self, caster, target):

        """
        picks and returns a skill for self

        >>> from a2_characters import Rogue
        >>> from a2_battle_queue import BattleQueue


        >>> k = Rogue('x', BattleQueue(), "pop")
        >>> j = Rogue('x', BattleQueue(), "pop")

        >>> p = create_default_tree()

        >>> k.enemy = j
        >>> j.enemy = k

        >>> k._hp = 95
        >>> k._sp = 30
        >>> j._hp = 20
        >>> j._sp = 50

        >>> type(p.pick_skill(k,j))
        <class 'a2_skills.RogueAttack'>


        """

        x = self.collector(caster, target)

        k1 = [i[1] for i in x]
        k2 = [i[0] for i in x]

        if k1 == []:
            return []
        oj = k1.index(min(k1))
        return k2[oj]




def create_default_tree() -> SkillDecisionTree:
    """
    Return a SkillDecisionTree that matches the one described in a2.pdf.

    >>> type(create_default_tree())
    <class '__main__.SkillDecisionTree'>

    """
    # TODO: Return a SkillDecisionTree that matches the one in a2.pdf.

    t2 = SkillDecisionTree(MageAttack(), checker2, 3,
                           [SkillDecisionTree(RogueSpecial(),
                                              checker3,
                                              4,
                                              [SkillDecisionTree
                                               (RogueAttack(),
                                                general, 6)])])
    t3 = SkillDecisionTree\
        (MageSpecial(), checker4, 2,
         [SkillDecisionTree(RogueAttack(),
                            general, 8)])
    t4 = SkillDecisionTree(
        RogueAttack(), checker5, 1,
        [SkillDecisionTree(RogueSpecial(),
                           general, 7)])

    t1 = SkillDecisionTree(MageAttack(), checker1, 5, [t2, t3, t4])
    return t1




def checker1(caster: 'Character', _):

    """
    checks if caster hp above 50
    >>> from a2_characters import Rogue
    >>> from a2_battle_queue import BattleQueue


    >>> k = Rogue('x', BattleQueue(), "pop")
    >>> j = Rogue('x', BattleQueue(), "pop")
    >>> checker1(k, j)
    True
    """

    return caster.get_hp() > 50

def checker2(caster: 'Character', _):
    """
    checks if caster above 20
    >>> from a2_characters import Rogue
    >>> from a2_battle_queue import BattleQueue


    >>> k = Rogue('x', BattleQueue(), "pop")
    >>> j = Rogue('x', BattleQueue(), "pop")
    >>> checker2(k, j)
    True
    """
    return caster.get_sp() > 20


def checker3(_, target: 'Character'):
    """
    checks if caster hp above 30
    """
    return target.get_hp() < 30


def checker4(_, target: 'Character'):
    """
    checks if caster sp above 40
    >>> from a2_characters import Rogue
    >>> from a2_battle_queue import BattleQueue


    >>> k = Rogue('x', BattleQueue(), "pop")
    >>> j = Rogue('x', BattleQueue(), "pop")
    >>> checker4(k, j)
    True
    """
    return target.get_sp() > 40


def checker5(caster: 'Character', _):
    """
    checks if caster hp above 90

    >>> from a2_characters import Rogue
    >>> from a2_battle_queue import BattleQueue


    >>> k = Rogue('x', BattleQueue(), "pop")
    >>> j = Rogue('x', BattleQueue(), "pop")
    >>> checker5(k, j)
    True
    """
    return  caster.get_hp() > 90

def general(_, __):
    """
    returns False

    >>> general(1,2)
    False

    """
    return False
