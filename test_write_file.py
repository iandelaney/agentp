from functions.write_file import write_file
def main():
    # Test case 1: Write to a file in the current directory
    print("Test case 1: Write to 'test1.txt' in the current directory")
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(f"  {result}")

    # Test case 2: Write to a file in a subdirectory
    print("\nTest case 2: Write to 'subdir/test2.txt' in a subdirectory")
    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(f"  {result}")

    # Test case 3: Attempt to write outside the working directory
    print("\nTest case 3: Attempt to write to '/tmp/temp.txt' outside the working directory")
    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(f"  {result}")

if __name__ == "__main__":
    main()