import sys
import threading
from collections import defaultdict

# ============================================================================
# MULTITHREADED WORD FREQUENCY COUNTER
# This program partitions a text file into N segments and processes each
# segment using a separate thread to count word frequencies.
# ============================================================================

class WordFrequencyCounter:
    """Manages multithreaded word frequency counting"""
    
    def __init__(self, filename, num_segments):
        self.filename = filename
        self.num_segments = num_segments
        self.segment_results = {}  # Stores results from each thread
        self.lock = threading.Lock()  # For thread-safe operations
    
    def read_file(self):
        """Read the entire text file"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    
    def partition_text(self, text):
        """Partition text into N segments"""
        if not text:
            return []
        
        total_length = len(text)
        segment_size = total_length // self.num_segments
        segments = []
        start = 0
        
        for i in range(self.num_segments):
            if i == self.num_segments - 1:
                # Last segment gets all remaining text
                segments.append(text[start:])
            else:
                # Find end position
                end = start + segment_size
                
                # Avoid splitting words - find next space
                while end < total_length and text[end] not in ' \n\t':
                    end += 1
                
                segments.append(text[start:end])
                start = end
        
        return segments
    
    def count_words(self, text):
        """Count word frequencies in a text segment"""
        word_freq = defaultdict(int)
        
        # Clean and split text
        words = text.lower().split()
        
        for word in words:
            # Remove punctuation
            cleaned = word.strip('.,;:!?"\'()[]{}—-')
            if cleaned:
                word_freq[cleaned] += 1
        
        return dict(word_freq)
    
    def process_segment(self, segment_id, text):
        """Process a single segment (runs in a thread)"""
        print(f"\n[Thread {segment_id}] Starting...")
        
        # Count words in this segment
        word_freq = self.count_words(text)
        
        # Store result in thread-safe manner
        with self.lock:
            self.segment_results[segment_id] = word_freq
        
        # Print intermediate results
        print(f"[Thread {segment_id}] Completed!")
        print(f"[Thread {segment_id}] Segment length: {len(text)} characters")
        print(f"[Thread {segment_id}] Total words: {sum(word_freq.values())}")
        print(f"[Thread {segment_id}] Unique words: {len(word_freq)}")
        
        # Show top 5 words from this segment
        top_5 = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        print(f"[Thread {segment_id}] Top 5 words: {top_5}")
    
    def consolidate_results(self):
        """Combine results from all threads"""
        final_freq = defaultdict(int)
        
        for segment_id, word_freq in self.segment_results.items():
            for word, count in word_freq.items():
                final_freq[word] += count
        
        return dict(final_freq)
    
    def run(self):
        """Main execution method"""
        print("=" * 60)
        print("MULTITHREADED WORD FREQUENCY COUNTER")
        print("=" * 60)
        print(f"File: {self.filename}")
        print(f"Number of segments: {self.num_segments}")
        
        # Step 1: Read file
        print("\n[1] Reading file...")
        text = self.read_file()
        print(f"    File size: {len(text)} characters")
        
        # Step 2: Partition text
        print(f"\n[2] Partitioning into {self.num_segments} segments...")
        segments = self.partition_text(text)
        print(f"    Created {len(segments)} segments")
        
        # Step 3: Create and start threads
        print(f"\n[3] Starting {self.num_segments} threads...")
        threads = []
        
        for i, segment in enumerate(segments):
            thread = threading.Thread(
                target=self.process_segment,
                args=(i, segment)
            )
            threads.append(thread)
            thread.start()
        
        # Step 4: Wait for all threads to complete
        print(f"\n[4] Waiting for all threads to complete...")
        for i, thread in enumerate(threads):
            thread.join()
            print(f"    Thread {i} has joined")
        
        # Step 5: Consolidate results
        print(f"\n[5] Consolidating results from all threads...")
        final_freq = self.consolidate_results()
        
        # Step 6: Display final results
        print("\n" + "=" * 60)
        print("FINAL CONSOLIDATED RESULTS")
        print("=" * 60)
        print(f"Total unique words: {len(final_freq)}")
        print(f"Total word count: {sum(final_freq.values())}")
        
        # Show top 20 words
        print(f"\nTop 20 Most Frequent Words:")
        print(f"{'Rank':<6} {'Word':<20} {'Frequency':<10}")
        print("-" * 40)
        
        top_20 = sorted(final_freq.items(), key=lambda x: x[1], reverse=True)[:20]
        for rank, (word, count) in enumerate(top_20, 1):
            print(f"{rank:<6} {word:<20} {count:<10}")
        
        print("\n" + "=" * 60)
        return final_freq


def main():
    """Main entry point"""
    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python WordCount.py <filename> <num_segments>")
        print("Example: python WordCount.py sample.txt 4")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        num_segments = int(sys.argv[2])
        if num_segments < 1:
            raise ValueError("Number of segments must be at least 1")
    except ValueError as e:
        print(f"Error: Invalid number of segments - {e}")
        sys.exit(1)
    
    # Create and run the counter
    counter = WordFrequencyCounter(filename, num_segments)
    counter.run()


if __name__ == "__main__":
    main()