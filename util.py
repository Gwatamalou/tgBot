def load_prompt(name):
    with open("resources/prompts/" + name + ".txt", "r",
              encoding="utf8") as file:
        return file.read()


def load_message(name):
    with open("resources/messages/" + name + ".txt", "r",
              encoding="utf8") as file:
        return file.read()

