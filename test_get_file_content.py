from functions.get_file_content import get_file_content
from config import MAX_CHARS

def main():
    content = get_file_content("calculator", "lorem.txt")

    suffix = f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'
    assert content.endswith(suffix), "Expected lorem.txt to be truncated with the suffix message"
    assert content[MAX_CHARS:].startswith('[...File "lorem.txt" truncated at')
    
    print("lorem.txt truncation test passed")

    #text1 = get_file_content("calculator", "main.py")
    res = get_file_content("calculator", "main.py")
    print(f"  {res.replace('\n', '\n  ')}")

    res = get_file_content("calculator", "pkg/calculator.py")
    print(f"  {res.replace('\n', '\n  ')}")

    res = get_file_content("calculator", "/bin/cat") 
    print(f"  {res.replace('\n', '\n  ')}")

    res = get_file_content("calculator", "pkg/does_not_exist.py")
    print(f"  {res.replace('\n', '\n  ')}")

if __name__ == "__main__":
    main()