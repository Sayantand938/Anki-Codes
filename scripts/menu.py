# # # menu.py

# # import os
# # import platform

# # def clear_screen():
# #     # Clear screen based on the OS
# #     if platform.system() == "Windows":
# #         os.system('cls')
# #     else:
# #         os.system('clear')

# # def show_menu():    
# #     print("1. Add Notes")
# #     print("2. Add Tags")
# #     print("3. Add Extra")
# #     print("4. Fetch note id")
# #     print("5. Prelims Notes Organizer")
# #     print("6. Prelims Tag Counter")
# #     print("7. Prelims Tag Remover")
# #     print("8. Exam")
# #     print("10. Exit")

# # def add_notes():
# #     clear_screen()
# #     print("Running add_note.py...")
# #     os.system('python add_note.py')  # Relative path from scripts/
# #     wait_for_enter()

# # def add_tags():
# #     clear_screen()
# #     print("1. Add Tags from txt")
# #     print("2. Add Tags from Anki")
# #     tag_choice = input("Enter your choice: ")
# #     if tag_choice == '1':
# #         print("Running add_tags_from_txt.py...")
# #         os.system('python add_tags_from_txt.py')  # Run the script for option 1
# #     elif tag_choice == '2':
# #         print("Add Tags from Anki is not implemented yet.")  # Do nothing for option 2
# #     else:
# #         print("Invalid choice, please try again.")
    
# #     wait_for_enter()

# # def add_extra():
# #     clear_screen()
# #     print("Running add_extra.py...")
# #     os.system('python add_extra_from_txt.py')
# #     wait_for_enter()

# # def fetch_note_ids():
# #     clear_screen()
# #     print("Running fetch_note_ids.py...")
# #     os.system('python fetch_note_ids.py')  # Relative path from scripts/
# #     wait_for_enter()

# # def prelims_notes_organizer():
# #     clear_screen()
# #     print("Running prelims_notes_organizer.py...")
# #     os.system('python prelims_notes_organizer.py')  # Relative path from scripts/
# #     wait_for_enter()

# # def prelims_tag_counter():
# #     clear_screen()
# #     print("Running prelims_tag_counter.py...")
# #     os.system('python prelims_tag_counter.py')  # Relative path from scripts/
# #     wait_for_enter()

# # def prelims_tag_remover():
# #     clear_screen()
# #     print("Running prelims_tag_remover.py...")
# #     os.system('python prelims_tag_remover.py')  # Relative path from scripts/
# #     wait_for_enter()

# # def wait_for_enter():
# #     input("Press Enter to continue...")
# #     clear_screen()

# # def main():
# #     while True:
# #         show_menu()
# #         choice = input("Enter your choice: ")
# #         if choice == '1':
# #             add_notes()
# #         elif choice == '2':
# #             add_tags()
# #         elif choice == '3':
# #             add_extra()
# #         elif choice == '4':
# #             fetch_note_ids()
# #         elif choice == '5':
# #             prelims_notes_organizer()
# #         elif choice == '6':
# #             prelims_tag_counter()
# #         elif choice == '7':
# #             prelims_tag_remover()
# #         elif choice == '10':
# #             print("Exiting...")
# #             break
# #         else:
# #             print("Invalid choice, please try again.")
# #             wait_for_enter()

# # if __name__ == "__main__":
# #     main()


# import os
# import platform

# def clear_screen():
#     # Clear screen based on the OS
#     if platform.system() == "Windows":
#         os.system('cls')
#     else:
#         os.system('clear')

# def show_menu():
#     print("1. Add Notes")
#     print("2. Add Tags")
#     print("3. Add Extra")
#     print("4. Fetch note id")
#     print("5. Prelims Notes Organizer")
#     print("6. Prelims Tag Counter")
#     print("7. Prelims Tag Remover")
#     print("8. Exam")
#     print("10. Exit")

# def add_notes():
#     clear_screen()
#     print("Running add_note.py...")
#     os.system('python add_note.py')  # Relative path from scripts/
#     wait_for_enter()

# def add_tags():
#     clear_screen()
#     print("1. Add Tags from txt")
#     print("2. Add Tags from Anki")
#     tag_choice = input("Enter your choice: ")
#     if tag_choice == '1':
#         print("Running add_tags_from_txt.py...")
#         os.system('python add_tags_from_txt.py')  # Run the script for option 1
#     elif tag_choice == '2':
#         print("Add Tags from Anki is not implemented yet.")  # Do nothing for option 2
#     else:
#         print("Invalid choice, please try again.")

#     wait_for_enter()

# def add_extra():
#     clear_screen()
#     print("Running add_extra.py...")
#     os.system('python add_extra_from_txt.py')
#     wait_for_enter()

# def fetch_note_ids():
#     clear_screen()
#     print("Running fetch_note_ids.py...")
#     os.system('python fetch_note_ids.py')  # Relative path from scripts/
#     wait_for_enter()

# def prelims_notes_organizer():
#     clear_screen()
#     print("Running prelims_notes_organizer.py...")
#     os.system('python prelims_notes_organizer.py')  # Relative path from scripts/
#     wait_for_enter()

# def prelims_tag_counter():
#     clear_screen()
#     print("Running prelims_tag_counter.py...")
#     os.system('python prelims_tag_counter.py')  # Relative path from scripts/
#     wait_for_enter()

# def prelims_tag_remover():
#     clear_screen()
#     print("Running prelims_tag_remover.py...")
#     os.system('python prelims_tag_remover.py')  # Relative path from scripts/
#     wait_for_enter()

# def run_exam():
#     clear_screen()
#     print("Running exam.bat in Exam folder...")
#     os.chdir('Exam')  # Change to the Exam folder
#     os.system('exam.bat')  # Run the batch file
#     os.chdir('..')  # Change back to the original directory
#     wait_for_enter()

# def wait_for_enter():
#     input("Press Enter to continue...")
#     clear_screen()

# def main():
#     while True:
#         show_menu()
#         choice = input("Enter your choice: ")
#         if choice == '1':
#             add_notes()
#         elif choice == '2':
#             add_tags()
#         elif choice == '3':
#             add_extra()
#         elif choice == '4':
#             fetch_note_ids()
#         elif choice == '5':
#             prelims_notes_organizer()
#         elif choice == '6':
#             prelims_tag_counter()
#         elif choice == '7':
#             prelims_tag_remover()
#         elif choice == '8':
#             run_exam()
#         elif choice == '10':
#             print("Exiting...")
#             break
#         else:
#             print("Invalid choice, please try again.")
#             wait_for_enter()

# if __name__ == "__main__":
#     main()


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
    print("4. Fetch note id")
    print("5. Prelims Notes Organizer")
    print("6. Prelims Tag Counter")
    print("7. Prelims Tag Remover")
    print("10. Exam")

def add_notes():
    clear_screen()
    print("Running add_note.py...")
    os.system('python add_note.py')  # Relative path from scripts/
    wait_for_enter()

def add_tags():
    clear_screen()
    print("1. Add Tags from txt")
    print("2. Add Tags from Anki")
    tag_choice = input("Enter your choice: ")
    if tag_choice == '1':
        print("Running add_tags_from_txt.py...")
        os.system('python add_tags_from_txt.py')  # Run the script for option 1
    elif tag_choice == '2':
        print("Add Tags from Anki is not implemented yet.")  # Do nothing for option 2
    else:
        print("Invalid choice, please try again.")

    wait_for_enter()

def add_extra():
    clear_screen()
    print("Running add_extra.py...")
    os.system('python add_extra_from_txt.py')
    wait_for_enter()

def fetch_note_ids():
    clear_screen()
    print("Running fetch_note_ids.py...")
    os.system('python fetch_note_ids.py')  # Relative path from scripts/
    wait_for_enter()

def prelims_notes_organizer():
    clear_screen()
    print("Running prelims_notes_organizer.py...")
    os.system('python prelims_notes_organizer.py')  # Relative path from scripts/
    wait_for_enter()

def prelims_tag_counter():
    clear_screen()
    print("Running prelims_tag_counter.py...")
    os.system('python prelims_tag_counter.py')  # Relative path from scripts/
    wait_for_enter()

def prelims_tag_remover():
    clear_screen()
    print("Running prelims_tag_remover.py...")
    os.system('python prelims_tag_remover.py')  # Relative path from scripts/
    wait_for_enter()

def run_exam():
    clear_screen()
    print("Running exam.bat in Exam folder...")
    os.chdir('Exam')  # Change to the Exam folder
    os.system('exam.bat')  # Run the batch file
    os.chdir('..')  # Change back to the original directory
    wait_for_enter()

def wait_for_enter():
    input("Press Enter to continue...")
    clear_screen()

def main():
    while True:
        show_menu()
        choice = input("Enter your choice (or 'q' to quit): ")
        if choice == '1':
            add_notes()
        elif choice == '2':
            add_tags()
        elif choice == '3':
            add_extra()
        elif choice == '4':
            fetch_note_ids()
        elif choice == '5':
            prelims_notes_organizer()
        elif choice == '6':
            prelims_tag_counter()
        elif choice == '7':
            prelims_tag_remover()
        elif choice == '10':
            run_exam()
        elif choice.lower() == 'q':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")
            wait_for_enter()

if __name__ == "__main__":
    main()
