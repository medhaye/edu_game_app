# Educational Environmental Game

This educational game aims to raise awareness about environmental issues in Tunisia through an immersive adventure. Players control a character accompanied by a parrot guide, navigating through multiple worlds while collecting trash and solving challenges related to environmental conservation.

## Project Structure

The project is organized as follows:

```
edu_game_3/
├── assets/           # Image assets for the game (sprites, backgrounds, etc.)
├── docs/             # Documentation and PDF files about environmental issues
├── src/              # Source code for the game
│   ├── main_menu.py  # Main menu interface
│   ├── menu.py       # Level selection menu
│   ├── sea_level.py  # Sea level gameplay
│   ├── recycle_game.py # Recycling game level
│   ├── chat.py       # AI chat interface
│   ├── popup.py      # Educational popup system
│   └── risk_env_project_llm_rag.py # RAG system for environmental Q&A
├── faiss_index.pkl   # Pretrained FAISS index for the RAG system
├── game_venv/        # Python virtual environment
├── requirements.txt  # Python dependencies
└── run_game.py       # Main launcher script
```

## Game Features

- **Multiple Game Levels**:
  - Sea Level: Clean up a polluted beach by collecting trash
  - Recycle Level: Sort waste into appropriate recycling bins

- **Educational Content**:
  - Learn about environmental issues in Tunisia
  - Understand the impact of pollution on marine ecosystems
  - Discover sustainable practices for waste management

- **AI Assistant**:
  - Integrated Q&A system using Retrieval-Augmented Generation (RAG)
  - Ask questions about environmental issues in Tunisia
  - Built with Cohere LLM and sentence-transformers

## How to Run the Game

1. Make sure you have a Python virtual environment set up:
   ```
   python -m venv game_venv
   ```

2. Activate the virtual environment:
   ```
   # On Windows
   .\game_venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the game:
   ```
   python run_game.py
   ```

## Game Controls

- **Arrow keys**: Move the character
- **Space**: Jump
- **Click parrot icon**: Access the AI assistant for environmental questions

## Technologies Used

- **Game Engine**: Pygame
- **AI Components**:
  - Retrieval-Augmented Generation (RAG)
  - Cohere LLM
  - FAISS for semantic search
  - Sentence Transformers (all-MiniLM-L6-v2)

## Documentation

The `docs` directory contains PDF files about environmental issues in Tunisia that form the knowledge base for the AI assistant:
- 15727-WB_Tunisia Country Profile-WEB.pdf
- Environment and sustainable Tunisia.pdf
- Maghreb-Technical-Note-11.pdf
