def get_int(prompt, min_val=None, max_val=None):
    while True:
        user_input = input(prompt)

        if not user_input.isdigit():
            print("Invalid input. Please enter a number.")
            continue

        value = int(user_input)

        if (min_val is not None and value < min_val) or \
           (max_val is not None and value > max_val):
            print("Invalid option. Please choose a valid number.")
            continue

        return value