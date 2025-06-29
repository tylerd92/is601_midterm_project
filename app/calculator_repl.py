from decimal import Decimal
import logging
from colorama import Style, Fore, init

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.logger import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory

init()

def calculator_repl():
    try:
        calc = Calculator()
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))
        print("Calculator started. Type 'help' for commands.")

        while True:
            try:
                command = input("\nEnter command: ").lower().strip()

                if command == 'help':
                    print(Fore.YELLOW)
                    print("Available commands:")
                    print("  add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff - Perform calculations")
                    print("  history - Show calculation history")
                    print("  clear - Clear calculation history")
                    print("  undo - Undo the last calculation")
                    print("  redo - Redo the last undone calculation")
                    print("  save - Save calculation history to file")
                    print("  load - Load calculation history from file")
                    print("  exit - Exit the calculator" + Style.RESET_ALL)
                    continue
                
                if command == 'exit':
                    try:
                        calc.save_history()
                        print(Fore.GREEN)
                        print("History saved successfully.")
                    except Exception as e: # pragma no cover
                        print(f"Warning: Could not save history: {e}")
                    print(Fore.GREEN)
                    print("Goodbye!")
                    break

                if command == 'history':
                    history = calc.show_history()
                    if not history:
                        print("No calculations in history")
                    else:
                        print(Fore.MAGENTA +"\nCalculation History:")
                        for i, entry in enumerate(history, 1):
                            print(Fore.CYAN + f"{i}. {entry}")
                        print(Style.RESET_ALL)
                    continue

                if command == 'clear':
                    calc.clear_history()
                    print(Fore.RED + "History cleared" + Style.RESET_ALL)
                    continue

                if command == 'undo':
                    if calc.undo():
                        print(Fore.RED + "Operation undone" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + "Nothing to undo" + Style.RESET_ALL)
                    continue

                if command == 'redo':
                    if calc.redo():
                        print(Fore.RED + "Operation redone" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + "Nothing to redo" + Style.RESET_ALL)
                    continue
            
                if command == 'save':
                    try:
                        calc.save_history()
                        print("History saved successfully")
                    except Exception as e: # pragma: no cover
                        print(f"Error saving history: {e}")
                    continue

                if command == 'load': 
                    try:
                        calc.load_history()
                        print("History loaded successfully")
                    except Exception as e: # pragma: no cover
                        print(f"Error loading history: {e}")
                    continue

                if command in OperationFactory.get_operations():
                    try:
                        print("Enter numbers (or 'cancel' to abort):")
                        a = input("First number: ")
                        if a.lower() == 'cancel':
                            print(Fore.RED + "Operation cancelled" + Style.RESET_ALL)
                            continue
                        b = input("Second number: ")
                        if b.lower() == 'cancel':
                            print(Fore.RED + "Operation cancelled" + Style.RESET_ALL)
                            continue
                        
                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)
                        result = calc.perform_operation(a, b)

                        if isinstance(result, Decimal):
                            result = result.normalize()

                        print(f"\nResult: {result}" + Style.RESET_ALL)
                    except (ValidationError, OperationError) as e:
                        print(f"Error: {e}")
                    except Exception as e:
                         print(f"Unexpected error: {e}")
                    continue

                print(Style.BRIGHT + Fore.RED + f"Unknown command: '{command}'. Type 'help' for available commands.")
                print(Style.RESET_ALL)

            except KeyboardInterrupt:
                print("\nOperation cancelled")
                continue
            except EOFError:
                print("\nInput terminated. Exiting...")
                break   
            except Exception as e:
                print(f"Error: {e}")
                continue
    except Exception as e: # pragma: no cover
        print(f"Fatal error: {e}")
        logging.error(f"Fatal error in calculator REPL: {e}")
        raise