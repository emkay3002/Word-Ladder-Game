import heapq
import random
from collections import deque, defaultdict
import requests


# Function to fetch the definition of a word from Free Dictionary API
def get_word_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and "meanings" in data[0]:
                meanings = data[0]["meanings"]
                if meanings:
                    return meanings[0]["definitions"][0]["definition"]
        return "No definition found."
    except Exception as e:
        return f"Error fetching definition: {e}"

# Check if two words differ by exactly one letter
def is_adjacent(word1, word2):
    return sum(1 for a, b in zip(word1, word2) if a != b) == 1

def build_graph(word_list):
    """Build a word transformation graph efficiently using adjacency buckets."""
    graph = defaultdict(list)
    adjacency_map = defaultdict(list)

    # Create pattern-based adjacency (e.g., "c_t" -> ["cat", "cut"])
    for word in word_list:
        for i in range(len(word)):
            pattern = word[:i] + "_" + word[i+1:]
            adjacency_map[pattern].append(word)

    # Populate the graph
    for words in adjacency_map.values():
        for word in words:
            graph[word].extend(w for w in words if w != word)

    return graph

# Breadth-First Search (BFS)
def bfs(start, end, graph):
    if start not in graph or end not in graph:
        print(f"Error: '{start}' or '{end}' not in graph.")
        return None

    queue = deque([(start, [start])])
    visited = set()
    while queue:
        word, path = queue.popleft()
        if word == end:
            return path
        visited.add(word)
        for neighbor in graph.get(word, []):  # Use .get() to prevent KeyError
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    return None

# Uniform Cost Search (UCS)
def ucs(start, end, graph):
    if start not in graph or end not in graph:
        print(f"Error: '{start}' or '{end}' not in graph.")
        return None

    pq = [(0, start, [start])]
    visited = set()
    while pq:
        cost, word, path = heapq.heappop(pq)
        if word == end:
            return path
        if word not in visited:
            visited.add(word)
            for neighbor in graph.get(word, []):
                heapq.heappush(pq, (cost + 1, neighbor, path + [neighbor]))
    return None


# A* Search
def heuristic(word, end):
    return sum(1 for a, b in zip(word, end) if a != b)

def a_star(start, end, graph):
    if start not in graph or end not in graph:
        print(f"Error: '{start}' or '{end}' not in graph.")
        return None

    pq = [(heuristic(start, end), 0, start, [start])]
    visited = set()
    while pq:
        _, cost, word, path = heapq.heappop(pq)
        if word == end:
            return path
        if word not in visited:
            visited.add(word)
            for neighbor in graph.get(word, []):
                heapq.heappush(pq, (cost + heuristic(neighbor, end), cost + 1, neighbor, path + [neighbor]))
    return None


#load words frm dictonay
def load_words(filename="dictionary.txt"):
    """Load words from a predefined dictionary file."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            words = {line.strip().lower() for line in file if line.strip()}
            #print(f"Loaded words: {words}")  # Debug print
            print(f"Loaded {len(words)} words from {filename}.")  # More concise

            return words
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return set()




def manual_gameplay(start, end, graph, search_algo):

    path = search_algo(start, end, graph)  # Compute the best path


    print(f"\n🔹 You must transform '{start}' → '{end}'. Guess each word in the path!")
    print("You have 3 incorrect attempts for the entire game.")

    attempts = 3
    current_word = start
    user_path = [current_word]

    for next_word in path[1:]:  # Start from the second word in the path
        while True:
            user_guess = input(f"🔹 What is the next word after '{current_word}'? ({attempts} attempts left): ").strip().lower()

            if user_guess == next_word:
                print("✅ Correct! Moving to the next word...")
                user_path.append(user_guess)
                current_word = user_guess
                break  # Move to the next word in the path
            else:
                attempts -= 1
                print(f"❌ Incorrect! ({attempts} attempts left)")

                if attempts == 0:
                    print(f"❌ Out of attempts! The correct path was: {' -> '.join(path)}")
                    return  # Ends the game immediately

    print("\n🎉 Congratulations! You reached the final word successfully!")
    print(f"🔗 Path followed: {' -> '.join(user_path)}")

# AI-Assisted Hint System
def ai_assisted_play(start, end, dictionary):
    word_list = {word for word in dictionary if len(word) == len(start)}
    if start not in word_list or end not in word_list:
        print("Error: One or both words are not in the dictionary.")
        return

    graph = build_graph(word_list)
    path = a_star(start, end, graph)  # Using A* for optimal hints

    if path:
        print(f"\n🔹 AI Hint System Active! Transform '{start}' → '{end}'. You have 3 total incorrect attempts.")

        attempts = 3  # Only 3 incorrect attempts for the whole game
        user_path = [start]  # Track the path the user follows


        for i in range(1, len(path)):  # Loop through intermediate words
            next_word = path[i]
            definition = get_word_definition(next_word)
            #debug statement
            print(f"Debug: AI-generated path -> {path}")

            print(f"\nHint {i}: The next word has this meaning → {definition}")

            while True:  # Ensure user stays on the same word until they get it right or fail
                user_input = input(f"🔹 Guess the word (Incorrect attempts left: {attempts}): ").strip().lower()

                if user_input == next_word:
                    print("✅ Correct! Moving to the next word...")
                    user_path.append(user_input)  # Store correct guesses
                    break  # Move to the next hint
                else:
                    attempts -= 1
                    print(f"❌ Incorrect! ({attempts} attempts left)")

                    if attempts == 0:
                        print(f"❌ Out of attempts! The correct word was '{next_word}'. Game over.")
                        return  # Ends the game immediately

        print("\n🎉 Congratulations! You reached the final word successfully!")
        print(f"🔗 Path followed: {' → '.join(user_path)}")
    else:
        print("⚠️ No valid path found between the words.")

def select_game_mode():
    print("Select Game Mode:")
    print("1. Beginner (Simple word ladders)")
    print("2. Advanced (Longer, complex word ladders)")
    print("3. Challenge Mode (Obstacles and constraints)")
    while True:
        try:
            choice = int(input("Enter mode (1/2/3): "))
            if choice in [1, 2, 3]:
                return choice
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def select_play_mode():
    print("\nSelect Play Mode:")
    print("1. Manual Gameplay")
    print("2. AI-Assisted Gameplay")
    while True:
        try:
            choice = int(input("Enter mode (1/2): "))
            if choice in [1, 2]:
                return choice
            print("Invalid choice. Enter 1 or 2.")
        except ValueError:
            print("Invalid input. Enter a number.")

def play_game(dictionary):
    # Step 1: Select Game Mode
    mode = select_game_mode()

    # Step 2: Select Play Mode
    play_mode = select_play_mode()

    # Step 3: Choose words based on game mode
    if mode == 1:
        start, end = "cat", "dog"
    elif mode == 2:
        start, end = "stone", "money"
    else:
        start = input("Enter the start word: ").strip().lower()
        end = input("Enter the end word: ").strip().lower()

    word_list = {word for word in dictionary if len(word) == len(start)}

    if start not in word_list or end not in word_list:
        print("Error: One or both words are not in the dictionary.")
        return

    graph = build_graph(word_list)

    # Step 4: Choose Algorithm for Manual Mode
    if play_mode == 1:  # Manual Mode
        print("\nChoose Search Algorithm:")
        print("1. BFS")
        print("2. UCS")
        print("3. A* Search")

        while True:
            try:
                algo_choice = int(input("Enter choice (1/2/3): "))
                if algo_choice in [1, 2, 3]:
                    search_algo = bfs if algo_choice == 1 else ucs if algo_choice == 2 else a_star
                    manual_gameplay(start, end, graph, search_algo)
                    return
                print("Invalid choice. Enter 1, 2, or 3.")
            except ValueError:
                print("Invalid input. Enter a number.")

    # Step 5: AI-Assisted Mode
    else:
        ai_assisted_play(start, end, dictionary)

# Run the game
if __name__ == "__main__":
    dictionary = load_words()
    if dictionary:  # Only play if words were successfully loaded
        play_game(dictionary)
