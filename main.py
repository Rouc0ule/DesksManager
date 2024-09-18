import random

student_list = [
    "Alice", "Benoît", "Chloé", "David", "Émilie",
    "François", "Gabrielle", "Hugo", "Inès", "Jules",
    "Katherine", "Léa", "Mathis", "Nina", "Olivier",
    "Pauline", "Quentin", "Roxane", "Sébastien", "Théo",
    "Ursule", "Victor", "Wendy", "Xavier", "Yasmine",
    "Zacharie", "Anaïs", "Clément", "Juliette", "Lucas"
]

random.shuffle(student_list)

groupes = []
for i in range(0, len(student_list), 2):
    if i + 1 < len(student_list):
        groupes.append((student_list[i], student_list[i+1]))
    else:
        groupes.append((student_list[i],))

print("Plan de classe :")
print("---------------")
for i, groupe in enumerate(groupes, 1):
    if len(groupe) == 2:
        print(f"Bureau {i}: {groupe[0]} et {groupe[1]}")
    else:
        print(f"Bureau {i}: {groupe[0]} (seul)")

alone_student = [groupe[0] for groupe in groupes if len(groupe) == 1]
if alone_student:
    print("\nÉlève(s) sans partenaire :")
    for eleve in alone_student:
        print(eleve)
