import random
from typing import List, Dict


class Dorms:
    def __init__(self):
        self.dorm_ids = []  # list of dorms (dorm_id)
        self.dorm_ids_to_indexes = {}  # maps of ids to indexes
        self.taken = []  # list of boolean true if dorm is taken
        self.index = -1

    def search_dorm(self, dorm_id):
        return self.dorm_ids.index(dorm_id)

    def ids_to_indexes(self, dorm_ids):
        indexes = []
        for i in dorm_ids:
            indexes.append(self.dorm_ids_to_indexes[i])
        return indexes

    def add_dorm(self, dorm_id: int):
        """
        add a dorm to list of dorms.

        :param dorm_id: id of the dorms.
        :return: None
        """
        self.dorm_ids.append(dorm_id)
        self.dorm_ids_to_indexes[dorm_id] = len(self.dorm_ids) - 1
        self.taken.append(False)

    def is_taken(self, index):
        """
        check if dorm at given index is already taken.

        :param index: index at which id of dorm is present.
        :return: if dorm is taken.
        """
        return self.taken[index]

    def take(self, index):
        """
        take the dorm at index.

        :param index: index at which id of dorm is present.
        :return: None
        """
        self.taken[index] = True

    def get_random_dorm_order(self):
        """
        get random order of dorms.

        :return: random list of dorm ids
        """
        dorm_order = self.dorm_ids[:]
        random.shuffle(dorm_order)
        return dorm_order

    def __getitem__(self, index):
        return self.dorm_ids[index]

    def __repr__(self):
        return ' '.join(map(str, self.dorm_ids))


class Dorm_preference_list:

    def __init__(self, preferences: List[int], ID: int, dorms: Dorms):
        """

        :param preferences: ordered list of indexes of dorm ids in descending order of preferences.
        :param ID: id of object that owns this list.
        """
        self.preference_list_ids = preferences
        self.dorms = dorms
        self.preference_list = dorms.ids_to_indexes(preferences)
        self.id = ID
        self.index = -1

    def get_id(self):
        return self.id

    ID = -1

    @classmethod
    def get_random_preference_list(cls, dorms: Dorms):
        return Dorm_preference_list(dorms.get_random_dorm_order(), Dorm_preference_list.get_ID(), dorms)

    @classmethod
    def get_ID(cls):
        cls.ID += 1
        return cls.ID

    def __getitem__(self, index):
        return self.preference_list[index]

    def __next__(self):
        self.index += 1
        if self.index >= len(self.preference_list):
            self.index = -1
            raise StopIteration
        else:
            return self.preference_list[self.index]

    def __repr__(self):
        return 'id: ' + str(self.get_id()) + '\n' + ' '.join(map(str, self.preference_list_ids))


def draw(dorms: Dorms, preference_lists: List[Dorm_preference_list]) -> (Dict[int, int], List[int]):
    """
    apply draw algorithm on dorms.

    :param dorms: Dorms object
    :param preference_lists: list of dorm preference list
    :return: mapping of id of dorms to id of owners of list. rank order of preferences
    """
    dorm_id_to_owner_id = {}
    random.shuffle(preference_lists)
    ranks_order = [i.get_id() for i in preference_lists]
    for preferences_list in preference_lists:
        for preference in preferences_list:
            if not dorms.is_taken(preference):
                dorm_id_to_owner_id[dorms[preference]] = preferences_list.get_id()
                dorms.take(preference)
                break
    return dorm_id_to_owner_id, ranks_order
