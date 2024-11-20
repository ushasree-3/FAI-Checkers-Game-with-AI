# **Checkers Game**

### **Course Project**  
**Course**: Foundations of AI  
**Instructors**:  
- Prof. Neeldhara Mishra  
- Prof. Manisha Padala  

### **Team Members**  
- **Deepanjali Kumari** - 22110069  
- **Anura Mantri** - 22110144  
- **Bhanu Repalle** - 22110221  
- **Saloni Shinde** - 22110242  
- **Thumma Ushashree** - 22110272  

---

## **Project Overview**

This project is a Python implementation of the classic board game **Checkers** using the `pygame` module. It features:  

- **Two-Player Mode**: Players can play against each other locally.  
- **Human vs AI Mode**: A single player can play against an AI opponent.  

The AI uses the **Minimax Algorithm** with **Alpha-Beta Pruning** to optimize decision-making and includes an **Epsilon-Greedy Strategy** for introducing variability in its moves.

---

## **How to Play**

### **Launching the Game**
After running the script, you'll be presented with a menu to choose the game mode:  
1. **Two-Player Mode**  
2. **Human vs AI Mode**  

### **Controls**
- Use the **mouse** to select and move pieces.  
- Valid moves will be **highlighted on the board**.  
- Pieces can capture opponent pieces by **jumping over them diagonally** to an empty square.  
- **Regular pieces** move diagonally forward, while **Kings** can move diagonally forward and backward.  
- **Kings** are created when a piece reaches the opponent’s back row.  
- Multiple captures in one turn are allowed if conditions permit.

---

## **Objective**

The objective of the game is to:  
- **Capture all of your opponent's pieces**, or  
- **Block all possible moves** of your opponent.  

---

## **Customization**

- **AI Depth**: Modify the depth of the Minimax tree in `game.py` to control the difficulty level of the AI.  
- **Epsilon Value**: Adjust the `epsilon` parameter in `game.py` to control the randomness of the AI’s moves.  

---

### **Enjoy playing Checkers!** 🎮

---

This updated version should render with proper bold text, headings, and spacing when displayed on platforms like GitHub or any Markdown viewer.
