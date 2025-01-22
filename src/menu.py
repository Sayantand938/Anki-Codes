import os
import platform

def clear_screen():
    # Clear screen based on the OS
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def show_menu():    
    print("1. Add Notes")
    print("2. Add Tags")
    print("3. Add Extra")
    print("4. Exit")

def add_notes():
    clear_screen()
    print("Running add_note.py...")
    os.system('python add_note.py')
    wait_for_enter()

def add_tags():
    clear_screen()
    print("Running add_tags.py...")
    os.system('python add_tags.py')
    wait_for_enter()

def add_extra():
    clear_screen()
    print("Running add_extra.py...")
    os.system('python add_extra.py')
    wait_for_enter()

def wait_for_enter():
    input("Press Enter ...")
    clear_screen()

def main():
    while True:
        show_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            add_notes()
        elif choice == '2':
            add_tags()
        elif choice == '3':
            add_extra()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
