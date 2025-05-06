# Active Context: AI Persona Discord Bot Collection

## 1. Current Work Focus
- Continuing with **Phase 1: Basic Bot Setup & Single Persona Interaction**.
- Implemented dynamic AI-generated greetings and basic single persona response in `bot.py`.
- Next: Further refine single persona implementation and begin setting up the basic database.

## 2. Recent Changes
- `bot.py` updated:
    - `on_message` now sends greeting intents to the AI with time and user context to generate dynamic, in-character greetings.
    - Includes a fallback to a hardcoded greeting if the AI fails.
    - `get_gemini_response` function updated to accept an optional `context` parameter.
- Basic single AI persona response using a placeholder prompt and simple NLU for greetings were previously implemented.

## 3. Next Steps (Immediate)
- Guide user on testing the updated `bot.py` functionality, specifically the dynamic greetings.
- Refine the `SINGLE_PERSONA_PROMPT` to better capture the desired "Luna" character.
- Add more basic NLU for simple questions (e.g., "How are you?").
- Begin setting up the initial SQLite database for minimal state storage.

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
