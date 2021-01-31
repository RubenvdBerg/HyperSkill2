def what_to_do(command):
    s = "Simon says"
    if command.startswith(s) or command.endswith(s):
        answer = command.replace(s, "").strip()
        return f"I {answer}"
    else:
        return "I won't do it!"

