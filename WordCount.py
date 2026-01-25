import sys



def main():
    # Check if user provided a filename
    if len(sys.argv) != 2:
        print("Usage: python step1.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    # Read the file
    with open(filename, 'r') as f:
        text = f.read()
    
    # Show what we got
    print("File content:")
    print(text)
    print(f"\nTotal characters: {len(text)}")


if __name__ == "__main__":
    main()