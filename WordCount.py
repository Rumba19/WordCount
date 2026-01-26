import sys

def count_words(text):
    """Count words in a piece of text"""
    words = text.split()
    word_count = {}
    
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    
    return word_count

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
    print()
    
    # Split text into 2 parts
    middle = len(text) // 2  # // means divide and round down
    
    part1 = text[:middle]   # From start to middle
    part2 = text[middle:]   # From middle to end
    
    print("=== PART 1 ===")
    print(part1)
    count1 = count_words(part1)
    print("Word count:", count1)
    
    print("\n=== PART 2 ===")
    print(part2)
    count2 = count_words(part2)
    print("Word count:", count2)
    # words = text.split()
    # count = 0
    # for word in words:
    #     if word == "hello":
    #         count += 1
  

    # print(f"\nThe word 'hello' appears {count} times")
 # Split into words
    # words = text.split()
    
    # # Use a dictionary to count each word
    # word_count = {}
    
    # for word in words:
    #     if word in word_count:
    #         word_count[word] += 1  # Word exists, add 1
    #     else:
    #         word_count[word] = 1   # First time seeing this word
    
    # Show results
    # print(f"\nWord frequencies:")
    # for word, count in word_count.items():
    #     print(f"  {word}: {count}")

if __name__ == "__main__":
    main()