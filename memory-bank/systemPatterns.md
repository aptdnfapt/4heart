# System Patterns: AI Persona Discord Bot Collection

## 1. System Architecture Overview
The system will be a single Python application using the `discord.py` library to connect to Discord as a bot. This application will manage multiple AI "personas."

```mermaid
graph TD
    DiscordAPI[Discord API] -- Events (Messages, Joins) --> BotApp[Python Bot Application (discord.py)]
    BotApp -- User Input / Context --> NLUModule[NLU Module]
    NLUModule -- Intent/Entities --> BotApp
    BotApp -- Prompts / Persona Context --> AI_API[AI API (e.g., Gemini)]
    AI_API -- Persona Responses --> BotApp
    BotApp -- Formatted Messages --> DiscordAPI

    BotApp --> StateManager[State Manager]
    StateManager -- Stores/Retrieves --> DB[Database (e.g., SQLite)]

    subgraph BotApplication
        direction LR
        NLUModule
        StateManager
        PersonaManager[Persona Manager]
        ActivityManager[Activity Manager (T&D, etc.)]
    end

    PersonaManager --> AI_API
    ActivityManager --> PersonaManager
    BotApp --> PersonaManager
    BotApp --> ActivityManager
```

## 2. Key Technical Decisions & Patterns
- **Single Bot, Multiple Personas:** The system will operate as one Discord bot instance that internally manages and voices multiple distinct AI personas. This simplifies deployment and inter-persona communication.
- **Natural Language Understanding (NLU) Core:** User input will be processed by an NLU component to determine intent (e.g., "wants to play Truth or Dare," "is greeting," "is asking a question to PersonaX") and extract key entities. This moves away from rigid command parsing.
- **Event-Driven Architecture:** The bot will react to events from Discord (new messages, users joining) and internal events (e.g., AI persona deciding to speak).
- **State Management:** A dedicated state manager will track:
    - Active users in the channel.
    - Current conversation context (recent messages, topics).
    - Active game states (e.g., current Truth or Dare game, whose turn).
    - Persona-specific states (e.g., their mood, recent interactions).
    This state will likely be persisted in a simple database (e.g., SQLite) to handle bot restarts.
- **Persona Prompting:** Each AI persona will have a carefully crafted base prompt defining its personality, backstory, speaking style, and relationship to other personas. These prompts will be combined with current conversational context when querying the AI API.
- **Asynchronous Operations:** `discord.py` is asynchronous. All I/O operations (Discord API calls, AI API calls, database interactions) must be handled asynchronously to prevent blocking.
- **Modular Design:** Components like NLU, Persona Management, Activity Management, and State Management will be developed as semi-independent modules to improve organization and testability.

## 3. Component Relationships
- **Main Bot (`moe_bot.py` or similar):** Initializes `discord.py`, loads configurations, and wires together the other components. Handles Discord events at a high level.
- **NLU Module:** Receives raw text from users. Outputs structured data (intent, entities, target persona if any).
- **Persona Manager:**
    - Stores persona profiles (prompts, avatars).
    - Decides which persona(s) should respond to a given input/event.
    - Formats prompts for the AI API based on persona and context.
    - Processes AI API responses into chat messages.
- **Activity Manager:**
    - Manages specific activities like Truth or Dare.
    - Tracks game rules, turns, and player participation.
    - Interacts with Persona Manager to get AI participation in activities.
- **State Manager:** Provides an interface for other components to read and write persistent and transient state.

## 4. Critical Implementation Paths
- **Reliable NLU for Intent Recognition:** This is the most critical and potentially challenging part. Accurately understanding user intent without commands is key to the "natural interaction" goal.
- **Contextual AI Prompting:** Generating coherent, in-character responses requires effective management of conversational history and persona-specific instructions in AI prompts.
- **Multi-Persona Interaction Logic:** Defining how personas decide to speak, how they interact with each other, and how they collectively respond to users without creating chaos.
- **Real-time Clock Integration:** Ensuring personas can use time-based greetings and references.
