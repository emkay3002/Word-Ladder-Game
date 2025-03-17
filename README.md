# Word Ladder Adventure

## Overview
Word Ladder Adventure is a Python-based word transformation game where players navigate from a starting word to a target word by changing one letter at a time, with each step forming a valid word. The game offers multiple difficulty levels, search algorithms, and an AI-assisted hint system.

## Features
- **Manual Gameplay Mode**: Players guess each word in the transformation path.
- **AI-Assisted Mode**: AI provides hints with word definitions.
- **Multiple Search Algorithms**: BFS, UCS, and A* for optimal pathfinding.
- **Graph Visualization**: Displays word connections and transformation paths.
- **Challenge Mode**: Timed gameplay with additional obstacles.
- **Score Tracking**: Earn points for correct guesses and time efficiency.

## Requirements
Ensure you have the following installed:
- Python 3.x
- Required libraries:
  ```bash
  pip install requests networkx matplotlib
  ```

## Setup and Running the Game
1. Clone or download the repository.
2. Ensure a valid `dictionary.txt` file is present in the same directory.
3. Run the game in Visual Studio Code (or any terminal) using:
   ```bash
   python word_ladder.py
   ```

## Gameplay Instructions
1. **Select a Game Mode:**
   - Beginner (Simple word ladders)
   - Advanced (Longer word ladders)
   - Challenge Mode (Timed with constraints)
2. **Select a Play Mode:**
   - Manual Mode (Player guesses the words)
   - AI-Assisted Mode (AI provides hints)
3. **Manual Mode:**
   - Choose a search algorithm (BFS, UCS, or A*)
   - Transform the start word to the end word by guessing intermediate words.
4. **AI-Assisted Mode:**
   - AI provides hints (word definitions) for the next step.
5. **Challenge Mode:**
   - Complete within a random time limit (30-60 seconds)!
   - Time bonuses apply to scores.

## Example
**Beginner Mode (Manual Gameplay, BFS Algorithm):**
```
Select Game Mode: 1
Select Play Mode: 1
Choose Search Algorithm: 1

🔹 You must transform 'cat' → 'dog'. Guess each word in the path!
What is the next word after 'cat'? cut
✅ Correct! Moving to the next word...
```

## Scoring System
- **+10 points** for each correct guess.
- **-5 points** for each incorrect attempt.
- **Time Bonus** in Challenge Mode.
- **Final Score displayed at the end.**

## Graph Visualization
The word transformation graph is generated using NetworkX and Matplotlib, highlighting the shortest path in red.

## Notes
- Ensure `dictionary.txt` exists with valid words.
- The Free Dictionary API is used for definitions.

## License
This project is open-source and free to use for educational purposes.

## Contributors
- **Eman Khalid**
- **Moimma Ali Khan**

Enjoy solving word puzzles with **Word Ladder Adventure**! 🚀

