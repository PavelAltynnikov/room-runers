from model import Level, Character

required_answers = "wasdq"

size = 10
character = Character()
level = Level(size, character)
level.print()

while True:
    answer = input(
        "Куда передвинуть персонажа?\n"
        "w. Вверх\n"
        "d. Вправо\n"
        "s. Вниз\n"
        "a. Влево\n"
        "q. Закрыть игру\n"
        "Ответ буквой: "
    )

    if answer not in required_answers:
        print(f"Ваш ответ не понятен, введите один из символов {required_answers}")
        continue
    if answer == "q":
        break

    if answer == "w":
        character.try_to_go_up()
    elif answer == "d":
        character.try_to_go_right()
    elif answer == "s":
        character.try_to_go_down()
    else:
        character.try_to_go_left()

    level.print()
