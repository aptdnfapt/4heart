# Tech Context: AI Persona Discord Bot Collection

## 1. Technologies Used
- **Programming Language:** Python (version 3.9+ recommended for `discord.py` features and modern syntax).
- **Discord Library:** `discord.py` (latest stable version). This library provides the interface to the Discord API.
- **AI API (Initial):** Google Gemini API. Access will be via Python client libraries.
- **Database (Initial):** SQLite for simplicity in storing state (conversation history, game states, user info, channel configs). `aiosqlite` will be used for asynchronous access.
- **NLU (Initial Approach):** Primarily prompt engineering with the Gemini API. For more complex scenarios, might explore smaller, specialized NLU libraries or fine-tuning if Gemini's direct NLU capabilities are insufficient for nuanced intent recognition.
- **Version Control:** Git (repository to be managed by the user).
- **Environment Management:** Python virtual environments (e.g., `venv` or `conda`).
- **Dependencies Management:** `requirements.txt` file for Python packages.

## 2. Development Setup
- A local Python development environment with `discord.py` and other necessary libraries installed.
- A Discord Bot application created through the Discord Developer Portal, providing a Bot Token.
- API key for the Gemini API.
- The bot will need to be invited to a test Discord server with appropriate permissions (read messages, send messages, manage channels if needed for configuration).

## 3. Technical Constraints & Considerations
- **API Rate Limits:** Both Discord API and Gemini API have rate limits. The application must handle these gracefully (e.g., with backoff strategies) to avoid being temporarily blocked. This is especially important with multiple personas potentially triggering AI API calls for a single user message.
- **Discord API Latency:** Network latency can affect responsiveness. Code should be optimized for asynchronous operations.
- **Gemini API Latency & Cost:** AI API calls can take time and incur costs. Efficient prompting and caching strategies (where appropriate) might be needed.
- **Context Window Limitations (AI):** LLMs have a finite context window. Managing conversational history to fit relevant information into prompts for the AI is crucial for coherence. Strategies like summarization or selective history might be needed for very long conversations.
- **NLU Accuracy:** The success of natural interaction heavily depends on the NLU's ability to correctly interpret user intent. This will require iterative refinement of prompts or NLU logic.
- **State Persistence & Scalability:** While SQLite is fine for initial development, if the bot becomes very popular or needs to manage state for many servers/users, a more robust database solution (e.g., PostgreSQL) might be considered in the future.
- **Security:** Bot token and API keys must be kept secure (e.g., using environment variables or a `.env` file, not hardcoded). User input should be handled carefully if it's used in database queries or system commands (though the latter is not planned).

## 4. Tool Usage Patterns
- **`discord.py` Client:** The primary interface for interacting with Discord. Events like `on_message`, `on_member_join` will be key.
- **Gemini API Client:** Used to send prompts (constructed with persona details and conversation context) and receive generated text responses.
- **`aiosqlite`:** For all database operations to ensure non-blocking behavior.
- **`datetime` module (Python):** For accessing the current time for time-aware greetings and logging.
- **Logging:** Python's `logging` module for debugging and tracking bot activity.

## 5. Future Technical Enhancements (Post-MVP)
- **Advanced NLU:** Integration with dedicated NLU libraries (e.g., Rasa, spaCy) or fine-tuning smaller LLMs for more robust intent recognition.
- **Dedicated Preprocessing AI for Ambiguity:** If the primary NLU (via Gemini prompt engineering) struggles with ambiguous user inputs, a future enhancement could involve a separate, "fresh" AI call with a specific system prompt to preprocess and clarify user messages before they are sent to the main NLU intent/entity extraction step. This could improve overall NLU accuracy but would add latency and potential API costs.
- **Local LLMs:** Exploring the use of self-hosted LLMs to reduce API dependency and cost, and potentially improve privacy/control. This would require significant hardware resources.
- **Vector Database:** For more sophisticated memory and context retrieval, especially for long-term memory or recalling specific past interactions.
- **Web Dashboard:** A simple web interface for configuring the bot or viewing stats (though this is a significant addition).
