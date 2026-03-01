from functions.get_files_info import get_files_info

def main():
    # Test case 1: Current directory of the calculator
    # For example, to handle the indentation for every line:
    print("Result for current directory:")
    res = get_files_info("calculator", ".")
    print(f"  {res.replace('\n', '\n  ')}")

    # Test case 2: The 'pkg' directory inside calculator
    print("\nResult for 'pkg' directory:")
    res = get_files_info("calculator", "pkg")
    print(f"  {res.replace('\n', '\n  ')}")

    # Test case 3
    print("Result for '/bin' directory:")
    res = get_files_info("calculator", "/bin")
    print(f"  {res.replace('\n', '\n  ')}")

    # Test case 4
    print("\nResult for '../' directory:")
    res = get_files_info("calculator", "../")
    print(f"  {res.replace('\n', '\n  ')}")


if __name__ == "__main__":
    main()