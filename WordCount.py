import sys



def main():
    # Check if user provided a filename
    if len(sys.argv) != 2:
        print("Usage: python WordCount.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    # Read the file
    with open(filename, 'r') as f:
        text = f.read()
    
    # Show what we got
    print("File content:")
    print(text)

    words = text.split()
    count = 0
    for word in words:
        if word == "hello":
            count += 1
  

    print(f"\nThe word 'hello' appears {count} times")


if __name__ == "__main__":
    main()