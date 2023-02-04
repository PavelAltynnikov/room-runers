from model import Level, Character

required_answers = "12345"

size = 10
character = Character()
level = Level(size, character)
level.print()

while True:
    answer = input(
        "Куда передвинуть персонажа?\n"
        "1. Вверх\n"
        "2. Вправо\n"
        "3. Вниз\n"
        "4. Влево\n"
        "5. Закрыть игру\n"
        "Ответ цифрой: "
    )

    if answer not in required_answers:
        print(f"Ваш ответ не понятен, введите одну из цифр {required_answers}")
        continue
    if answer == "5":
        break

    if answer == "1":
        character.try_to_go_up()
    elif answer == "2":
        character.try_to_go_right()
    elif answer == "3":
        character.try_to_go_down()
    else:
        character.try_to_go_left()

    level.print()
