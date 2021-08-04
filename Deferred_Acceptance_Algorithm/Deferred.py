import heapq
from random import shuffle, randint
from typing import List, Dict


class Student:
    def __init__(self, student_id: int, student_name: str = ""):
        self.student_name = student_name
        self.student_id = student_id
        self.fav_ind = -1
        self.preference_list = []

    def set_preference_list(self, preference_list: List[int]):
        """
        sets preference list of student.

        :param preference_list: List of hospital ids in order of most preferred to least preferred.
        :return: None
        """
        self.preference_list = preference_list
        self.fav_ind = 0

    def get_fav_hospital(self) -> int:
        """
        gets favorite hospital which has not rejected the student.

        :return: Hospital id
        """
        return self.preference_list[self.fav_ind]

    def reject(self):
        """
        Call this to reject student from its favorite hospital.

        :return: None
        """
        self.fav_ind += 1

    def __repr__(self):
        return "sid: " + str(self.student_id) + " sname: " + self.student_name + " preferences: " + str(
            self.preference_list)

    def set_random_preference_list(self, hospital_ids: List[int]):
        """
        sets a random preference list of student.

        :param hospital_ids: List of hospital ids.
        :return: None
        """
        self.preference_list = hospital_ids[:]
        shuffle(self.preference_list)
        self.fav_ind = 0

    _sid = 0

    @classmethod
    def create_random_student(cls):
        s = Student(cls._sid)
        cls._sid += 1
        return s


class Hospital:
    def __init__(self, hospital_id: int, capacity: int, hospital_name: str = ""):
        self.hospital_name = hospital_name
        self.hospital_id = hospital_id
        self.priority_dict = {}
        self.capacity = capacity
        self.tentative_students_heap = []

    def set_priority_dict(self, priority_dict: Dict[int, int]):
        """
        sets priorities of student ids of students available.

        :param priority_dict: priorities of student ids of students available.
        :return: None
        """
        self.priority_dict = priority_dict

    def process_student_application(self, student_id):
        """
        Processes student's application and rejects student or add to tentative list.

        :return: student_id of student who is rejected if No one rejected then None.
        """
        if len(self.tentative_students_heap) >= self.capacity:
            if -1 * self.tentative_students_heap[0][0] > self.priority_dict[student_id]:
                _, sid = heapq.heappushpop(self.tentative_students_heap,
                                           (-1 * self.priority_dict[student_id], student_id))
                return sid
            else:
                return student_id
        else:
            heapq.heappush(self.tentative_students_heap, (-1 * self.priority_dict[student_id], student_id))

    def __repr__(self):
        return "hid: " + str(self.hospital_id) + " hname: " + self.hospital_name + " preferences: " + str(
            self.priority_dict) + " capacity: " + str(self.capacity)

    def set_random_priority_dict(self, student_ids: List[int]):
        """
        sets priorities of student ids of students available.

        :param student_ids: list of student ids.
        :return: None
        """
        sids = student_ids[:]
        shuffle(sids)
        self.priority_dict = {i: sids[i] for i in range(len(sids))}

    _hid = 0
    _max_capacity = 3

    @classmethod
    def create_random_hospital(cls):
        h = Hospital(cls._hid, randint(1, cls._max_capacity))
        cls._hid += 1
        return h


def deferred_acceptance(student_dict: Dict[int, Student], hospital_dict: Dict[int, Hospital]):
    """
    apply deferred acceptance to student and hospital list.

    :param student_dict: map of student_id with student.
    :param hospital_dict: map of hospital_id with hospital.
    :return: map of student_id to hospital_id
    """
    unallocated_students = list(student_dict.keys())
    allocations = {}
    while unallocated_students:
        temp = []
        for s in unallocated_students:
            student = student_dict[s]
            if student.fav_ind < len(student.preference_list):
                sid = hospital_dict[student.get_fav_hospital()].process_student_application(student.student_id)
                allocations[student.student_id] = student.get_fav_hospital()
                if sid is not None:
                    student_dict[sid].reject()
                    del allocations[sid]
                    temp.append(sid)
        unallocated_students = temp
    return allocations
