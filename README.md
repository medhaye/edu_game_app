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

4. Set up environment variables:
   - Create a `.env` file in the root directory with the following API keys:
   ```
   HUGGINGFACE_API_TOKEN=your_huggingface_token
   COHERE_API_KEY=your_cohere_api_key
   ```
   - These API keys are required for the RAG system to work properly
   - You can obtain API keys from [Hugging Face](https://huggingface.co/settings/tokens) and [Cohere](https://dashboard.cohere.ai/api-keys)

5. Run the game:
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

## FAISS Index Management

The game uses a FAISS index file (`faiss_index.pkl`) for the RAG system to efficiently retrieve information from the PDF documents. This file is pre-built and included in the repository.

If you need to regenerate the FAISS index (e.g., if you add new documents):

1. Delete the existing `faiss_index.pkl` file
2. Run the game - it will automatically rebuild the index from the documents in the `docs` directory (this may take a few minutes)
3. The new index will be saved to `faiss_index.pkl` for future use

## Development

### Environment Setup

For development, ensure you have:

1. A virtual environment activated (`game_venv`)
2. All dependencies installed (`requirements.txt`)
3. API keys set up in a `.env` file (not tracked by git)
4. Proper access to the FAISS index
