# Project Brief: AI-Powered Discord Roleplay Bots

## 1. Project Name
AI Persona Discord Bot Collection

## 2. Project Goal
To create a collection of 3-5 AI-powered Discord bot personas (envisioned as sisters or friends) that can engage in natural, continuous role-play conversations with users on a designated Discord channel. A key feature will be their ability to play "Truth or Dare" with users and each other in a fluid, non-command-based manner. The bots should feel like persistent, human-like entities within the channel.

## 3. Scope
- **Core Functionality:**
    - 4 AI personas with distinct, user-defined personalities.
    - Continuous, 24/7 conversational ability in a designated channel per server.
    - Natural Language Understanding (NLU) to interpret user messages and intent (e.g., initiating games, general chat).
    - Ability for personas to initiate and participate in Truth or Dare games.
    - Fluid game mechanics: any user or AI can ask/be asked, suggestions for truths/dares can come from multiple participants.
    - Roleplay actions (e.g., `**hugs UserX**`) supported for both users and AI.
    - AI personas should interact with each other as well as users.
    - Real-time awareness for greetings (e.g., "Good morning!").
    - Seamless joining/rejoining of users into conversations/games.
- **Technical Aspects:**
    - Initial AI backend: Gemini API.
    - Future consideration: Local LLMs.
    - Language/Framework: Python with `discord.py`.
    - State management for conversations and game status.
- **Out of Scope (Initial Version):**
    - Complex multi-server management beyond one designated channel per server.
    - Persistent memory of individual user preferences beyond the current session/recent context.
    - Voice chat capabilities.
    - Image generation/interaction beyond avatars.

## 4. Target Users
Discord users interested in interactive role-playing experiences with AI characters.

## 5. Success Criteria
- Users can engage in believable, extended conversations with the AI personas.
- Truth or Dare games can be initiated and played naturally without explicit commands.
- AI personas exhibit their defined personalities consistently.
- The system is stable and can maintain context within a reasonable conversational window.
