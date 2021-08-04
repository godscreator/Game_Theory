from Deferred_Acceptance_Algorithm.Deferred import Hospital, Student, deferred_acceptance

if __name__ == '__main__':
    H = 4
    S = 20
    Hospital._max_capacity = 2
    hospital_dict = {}
    hospital_ids = []
    for _ in range(H):
        h = Hospital.create_random_hospital()
        hospital_dict[h.hospital_id] = h
        hospital_ids.append(h.hospital_id)
    student_dict = {}
    student_ids = []
    for _ in range(S):
        s = Student.create_random_student()
        student_dict[s.student_id] = s
        student_ids.append(s.student_id)
    print("Hospitals: ")
    for hid in hospital_dict:
        hospital_dict[hid].set_random_priority_dict(student_ids)
        print(hospital_dict[hid])
    print("Students: ")
    for sid in student_dict:
        student_dict[sid].set_random_preference_list(hospital_ids)
        print(student_dict[sid])
    print()
    allocations = deferred_acceptance(student_dict, hospital_dict)
    print("Allocations: (sid,hid):")
    for i in allocations:
        print((i, allocations[i]))
