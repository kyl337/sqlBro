def get_input(prompt, required=True):
    while True:
        user_input = input(prompt)
        if not required and user_input == "":
            return None
        elif user_input:
            return user_input
        else:
            print("This field cannot be left blank.")

def generate_select_query():
    task_number = get_input("Enter ticketID: ")
    table_name = get_input("Enter table name: ")
    fields = get_input("Enter fields (separated by commas): ")
    condition = get_input("Enter condition (leave blank if none): ", required=False)
    query = f"SELECT {fields} FROM {table_name}"
    if condition:
        query += f" WHERE {condition}"
    return task_number, query

def main():
    while True:
        print("\nSQL Query Generator")
        print("1. Generate SELECT query")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            task_number, query = generate_select_query()
            print("\nTask Number:", task_number)
            print("\nGenerated SQL Query:", query)
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
