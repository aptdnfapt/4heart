# Active Context: AI Persona Discord Bot Collection

## 1. Current Work Focus
- Continuing with **Phase 1: Basic Bot Setup & Single Persona Interaction**.
- Implemented Gemini API client initialization and basic AI response generation in `bot.py`.
- Next: Refine to implement a single, distinct AI persona and basic NLU for greetings.

## 2. Recent Changes
- `bot.py` updated:
    - Gemini API client (`genai.GenerativeModel`) is now initialized.
    - `get_gemini_response` async function added to call the Gemini API.
    - `on_message` event now processes user messages, sends them to Gemini with a generic prompt, and relays the AI's response back to Discord.
    - Basic error handling for API calls and response length included.
- Foundational project files (`requirements.txt`, `.env.example`, initial `bot.py`) were previously created.

## 3. Next Steps (Immediate)
- Guide user on testing the current `bot.py` functionality.
- Begin implementing a more defined single AI persona:
    - Create a basic persona prompt (e.g., "You are Luna, a cheerful and helpful AI friend...").
    - Modify `on_message` in `bot.py` to use this persona prompt when interacting with Gemini.
- Start work on "Simple NLU for greetings and basic questions" as per Phase 1.

## 4. Active Decisions & Considerations
- **Project Scope:** The project aims for a highly natural, NLU-driven interaction model for multiple AI personas, including activities like Truth or Dare. This is a complex undertaking.
- **Technology Stack (Initial):** Python with `discord.py`, Gemini API for AI.
- **Memory Bank Adherence:** Strictly following the `.clinerules` for documentation and workflow.

## 5. Important Patterns & Preferences (Emerging)
- Emphasis on natural, human-like interaction over command-based systems.
- Desire for immersive role-playing experience.
- User-defined personalities for AI personas.
- The Memory Bank system itself is a core pattern for this project's development.

## 6. Learnings & Project Insights
- The shift from a simple bot to a complex NLU-driven multi-persona system significantly increases development complexity, particularly around state management and reliable intent recognition.
- Clear documentation via the Memory Bank is critical, especially given the potential for interruptions or context shifts.
