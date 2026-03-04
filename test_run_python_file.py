from functions.run_python_file import run_python_file


def main():
    test_cases = [
        ("usage instructions", lambda: run_python_file("calculator", "main.py")),
        ("calculator run: 3 + 5", lambda: run_python_file("calculator", "main.py", ["3 + 5"])),
        ("run calculator tests", lambda: run_python_file("calculator", "tests.py")),
        ("outside working dir error", lambda: run_python_file("calculator", "../main.py")),
        ("nonexistent file error", lambda: run_python_file("calculator", "nonexistent.py")),
        ("not a python file error", lambda: run_python_file("calculator", "lorem.txt")),
    ]

    for i, (label, fn) in enumerate(test_cases, start=1):
        print(f"\n=== Test {i}: {label} ===")
        result = fn()
        print(result)


if __name__ == "__main__":
    main()