import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DESIGNATED_CHANNEL_ID_STR = os.getenv("DESIGNATED_CHANNEL_ID")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-pro") # Default to gemini-pro if not set

# --- Logging Setup ---
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# --- Validate Configuration ---
if not DISCORD_BOT_TOKEN:
    logger.critical("DISCORD_BOT_TOKEN not found in environment variables. Exiting.")
    exit()
if not GEMINI_API_KEY:
    logger.critical("GEMINI_API_KEY not found in environment variables. Exiting.")
    exit()
if not DESIGNATED_CHANNEL_ID_STR:
    logger.warning("DESIGNATED_CHANNEL_ID not found in environment variables. Bot may not function as expected in a specific channel.")
    DESIGNATED_CHANNEL_ID = None
else:
    try:
        DESIGNATED_CHANNEL_ID = int(DESIGNATED_CHANNEL_ID_STR)
    except ValueError:
        logger.error(f"Invalid DESIGNATED_CHANNEL_ID: {DESIGNATED_CHANNEL_ID_STR}. Must be an integer. Bot may not function as expected.")
        DESIGNATED_CHANNEL_ID = None


# --- Discord Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content
intents.members = True          # Optional: if you need member join/leave events or member details

bot = commands.Bot(command_prefix="!", intents=intents) # Using a dummy prefix for now, NLU will override

# --- Gemini API Setup ---
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Use the model name from environment variables
    model = genai.GenerativeModel(GEMINI_MODEL_NAME)
    logger.info(f"Gemini API client configured successfully with model: {GEMINI_MODEL_NAME}")
except Exception as e:
    logger.critical(f"Failed to configure Gemini API client with model {GEMINI_MODEL_NAME}: {e}")
    model = None # Ensure model is None if setup fails

# --- Placeholder for Single Persona Prompt (Phase 1) ---
# In later phases, this will be managed by the PersonaManager and will be more complex,
# including conversation history and dynamic elements.
SINGLE_PERSONA_PROMPT = """
You are Luna, a cheerful and friendly AI persona designed to chat with users in a Discord channel.
You are one of several AI sisters/friends in this channel.
Respond to the user's message in a friendly and engaging manner.
Keep your responses relatively concise.
"""

async def get_gemini_response(user_message_content: str) -> str | None:
    """Gets a response from the Gemini API using the single persona prompt."""
    if not model:
        logger.error("Gemini model is not initialized. Cannot get response.")
        return None
    try:
        # Combine the persona prompt with the user's message
        full_prompt = f"{SINGLE_PERSONA_PROMPT}\nUser said: {user_message_content}\nYour response:"

        # For simplicity, using generate_content for now.
        # For chat-like behavior, model.start_chat(history=[]) would be better in later phases.
        response = await model.generate_content_async(full_prompt)

        # Ensure we handle potential API errors or empty responses gracefully
        if response and response.parts:
            # Assuming the first part contains the text response
            candidate = response.candidates[0]
            if candidate.content and candidate.content.parts:
                 return "".join(part.text for part in candidate.content.parts if hasattr(part, 'text'))
            logger.warning(f"Gemini response did not contain expected text parts. Response: {response.text[:100] if hasattr(response, 'text') else 'No text attribute'}")
            return None # Or some default error message
        else:
            logger.warning(f"Gemini response was empty or malformed. Response: {response}")
            return None # Or some default error message
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")
        return None

@bot.event
async def on_ready():
    """Called when the bot is successfully connected to Discord."""
    logger.info(f"Bot logged in as {bot.user.name} (ID: {bot.user.id})")
    logger.info(f"Operating in channel ID: {DESIGNATED_CHANNEL_ID}" if DESIGNATED_CHANNEL_ID else "No specific DESIGNATED_CHANNEL_ID set.")
    logger.info("Bot is ready and listening for messages.")
    # You can set the bot's presence here if desired
    # await bot.change_presence(activity=discord.Game(name="Chatting with friends!")) # Example presence

# --- Main Bot Logic (to be expanded) ---
@bot.event
async def on_message(message: discord.Message):
    """Called when a message is sent in a channel the bot can see."""
    if message.author == bot.user:
        return  # Ignore messages from the bot itself

    # Basic check for designated channel if set
    if DESIGNATED_CHANNEL_ID and message.channel.id != DESIGNATED_CHANNEL_ID:
        # Silently ignore messages not in the designated channel, or provide a gentle reminder
        # logger.debug(f"Message received in non-designated channel {message.channel.id}, ignoring.")
        return

    logger.info(f"Message from {message.author.name} in #{message.channel.name}: {message.content}")

    user_message_content = message.content.lower() # Convert to lowercase for simpler matching

    # --- Simple NLU for Greetings (Phase 1) ---
    # This is a very basic check. More sophisticated NLU will be added later.
    greeting_keywords = ["hi", "hello", "hey", "greetings", "o/", "👋"]

    is_greeting = any(keyword in user_message_content for keyword in greeting_keywords)

import datetime # Import datetime module

# ... (rest of imports and configuration) ...

# --- Placeholder for Single Persona Prompt (Phase 1) ---
# In later phases, this will be managed by the PersonaManager and will be more complex,
# including conversation history and dynamic elements.
SINGLE_PERSONA_PROMPT = """
You are Luna, a cheerful and friendly AI persona designed to chat with users in a Discord channel.
You are one of several AI sisters/friends in this channel.
Respond to the user's message in a friendly and engaging manner.
Keep your responses relatively concise.
"""

async def get_gemini_response(user_message_content: str, context: str = "") -> str | None:
    """Gets a response from the Gemini API using the single persona prompt and additional context."""
    if not model:
        logger.error("Gemini model is not initialized. Cannot get response.")
        return None
    try:
        # Combine the persona prompt, context, and user's message
        full_prompt = f"{SINGLE_PERSONA_PROMPT}\n{context}\nUser said: {user_message_content}\nYour response:"

        # For simplicity, using generate_content for now.
        # For chat-like behavior, model.start_chat(history=[]) would be better in later phases.
        response = await model.generate_content_async(full_prompt)

        # Ensure we handle potential API errors or empty responses gracefully
        if response and response.parts:
            # Assuming the first part contains the text response
            candidate = response.candidates[0]
            if candidate.content and candidate.content.parts:
                 return "".join(part.text for part in candidate.content.parts if hasattr(part, 'text'))
            logger.warning(f"Gemini response did not contain expected text parts. Response: {response.text[:100] if hasattr(response, 'text') else 'No text attribute'}")
            return None # Or some default error message
        else:
            logger.warning(f"Gemini response was empty or malformed. Response: {response}")
            return None # Or some default error message
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")
        return None

# ... (on_ready event) ...

# --- Main Bot Logic (to be expanded) ---
@bot.event
async def on_message(message: discord.Message):
    """Called when a message is sent in a channel the bot can see."""
    if message.author == bot.user:
        return  # Ignore messages from the bot itself

    # Basic check for designated channel if set
    if DESIGNATED_CHANNEL_ID and message.channel.id != DESIGNATED_CHANNEL_ID:
        # Silently ignore messages not in the designated channel, or provide a gentle reminder
        # logger.debug(f"Message received in non-designated channel {message.channel.id}, ignoring.")
        return

    logger.info(f"Message from {message.author.name} in #{message.channel.name}: {message.content}")

    user_message_content = message.content.lower() # Convert to lowercase for simpler matching

    # --- Simple NLU for Greetings (Phase 1) ---
    # This is a very basic check. More sophisticated NLU will be added later.
    greeting_keywords = ["hi", "hello", "hey", "greetings", "o/", "👋"]

    is_greeting = any(keyword in user_message_content for keyword in greeting_keywords)

    if is_greeting:
        # --- Dynamic Persona Greeting Response (Phase 1) ---
        # Send the greeting intent to the AI with persona and time context.
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        greeting_context = f"The current time is {current_time}. A user named {message.author.name} just sent a greeting."
        ai_greeting_response = await get_gemini_response(message.content, context=greeting_context) # Use original case for AI

        if ai_greeting_response:
            await message.channel.send(ai_greeting_response)
            logger.info(f"Responded to greeting from {message.author.name} with AI-generated response.")
        else:
            # Fallback to a simple hardcoded greeting if AI fails
            fallback_greeting = f"Hi there, {message.author.name}! 👋"
            await message.channel.send(fallback_greeting)
            logger.warning(f"AI failed to generate greeting for {message.author.name}. Used fallback.")

        return # Stop processing after responding to a greeting

    # --- Basic AI Response with Persona Prompt (Single Persona - Phase 1) ---
    # If it's not a recognized greeting, send the message to the AI with the persona prompt.

    ai_response_text = await get_gemini_response(message.content) # Use original case for AI

    if ai_response_text:
        # Send the AI's response back to the channel
        # Discord has a 2000 character limit per message.
        # For longer responses, we'll need to implement message splitting later.
        if len(ai_response_text) > 2000:
            logger.warning("AI response exceeds 2000 characters. Truncating.")
            await message.channel.send(ai_response_text[:2000])
        else:
            await message.channel.send(ai_response_text)
    else:
        # Send a generic error message if AI fails to respond
        await message.channel.send("I'm sorry, I couldn't process that right now. Please try again later.")

    # We are not using command_prefix for NLU based interaction,
    # but if you add traditional commands later, uncomment the line below.
    # await bot.process_commands(message)


# --- Run the Bot ---
if __name__ == "__main__":
    if DISCORD_BOT_TOKEN:
        try:
            bot.run(DISCORD_BOT_TOKEN)
        except discord.LoginFailure:
            logger.critical("Failed to log in. Please check your DISCORD_BOT_TOKEN.")
        except Exception as e:
            logger.critical(f"An unexpected error occurred while running the bot: {e}")
    else:
        logger.critical("DISCORD_BOT_TOKEN is not set. Cannot run bot.")
