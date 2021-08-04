from Draw_Algorithm.Draw import Dorms, Dorm_preference_list, draw

if __name__ == '__main__':
    n = 3
    dorms = Dorms()
    for i in range(n):
        dorms.add_dorm(i)
    print("Dorms: ")
    print(dorms)
    preference_lists = [Dorm_preference_list.get_random_preference_list(dorms) for _ in range(n)]
    print("preferences: ")
    for p in preference_lists:
        print(p)
    assigns, rank_order = draw(dorms, preference_lists)
    print("rank order:")
    print(rank_order)
    print("assignment: ")
    print("dorm : student")
    for i in assigns:
        print(i, " : ", assigns[i])
