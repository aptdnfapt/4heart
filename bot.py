import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging
import google.generativeai as genai
import datetime
import asyncio
from collections import deque

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

# --- Message Cache Setup ---
# Use a deque to store recent message IDs to prevent processing duplicates.
# The maximum length determines how many recent messages are kept in memory.
# Adjust the maxlen based on expected message volume and memory constraints.
PROCESSED_MESSAGES_CACHE = deque(maxlen=1000) # Store up to 1000 recent message IDs

async def get_gemini_response(prompt_text: str) -> str | None:
    """Gets a response from the Gemini API using the single persona prompt."""
    if not model:
        logger.error("Gemini model is not initialized. Cannot get response.")
        return None
    try:
        # For simplicity, using generate_content for now.
        # For chat-like behavior, model.start_chat(history=[]) would be better in later phases.
        response = await model.generate_content_async(prompt_text)

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

    # --- Duplicate Message Check ---
    if message.id in PROCESSED_MESSAGES_CACHE:
        logger.debug(f"Ignoring duplicate message with ID: {message.id}")
        return # Ignore if message ID is already in cache

    # Add the message ID to the cache
    PROCESSED_MESSAGES_CACHE.append(message.id)

    # Basic check for designated channel if set
    if DESIGNATED_CHANNEL_ID and message.channel.id != DESIGNATED_CHANNEL_ID:
        # Silently ignore messages not in the designated channel, or provide a gentle reminder
        # logger.debug(f"Message received in non-designated channel {message.channel.id}, ignoring.")
        return

    logger.info(f"Processing message from {message.author.name} in #{message.channel.name}: {message.content}")

    user_message_content = message.content.lower() # Convert to lowercase for simpler matching

    # --- Determine Intent (Simple NLU - Phase 1) ---
    # This is a basic intent detection. More sophisticated NLU will be added later.
    intent = 'general_chat' # Default intent

    greeting_keywords = ["hi", "hello", "hey", "greetings", "o/", "👋"]
    if any(keyword in user_message_content for keyword in greeting_keywords):
        intent = 'greeting'

    simple_question_keywords = ["how are you", "how r u", "whats up", "what's up", "what are you doing", "what u doing"]
    if intent == 'general_chat' and any(keyword in user_message_content for keyword in simple_question_keywords):
        intent = 'simple_question'

    logger.debug(f"Detected intent: {intent}")

    # --- Generate AI Response Based on Intent ---
    ai_response_text = None
    prompt_for_ai = None
    context_for_ai = ""

    if intent == 'greeting':
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        context_for_ai = f"The current time is {current_time}. A user named {message.author.name} just sent a greeting."
        # Craft a specific prompt for the AI to generate a greeting
        prompt_for_ai = f"{SINGLE_PERSONA_PROMPT}\n{context_for_ai}\nUser's greeting: {message.content}\nGenerate a friendly, in-character greeting response:"
        ai_response_text = await get_gemini_response(prompt_for_ai)
        if ai_response_text:
            logger.info(f"Generated AI greeting response for {message.author.name}.")
        else:
            logger.warning(f"AI failed to generate greeting for {message.author.name}. Using fallback.")
            # Fallback to a simple hardcoded greeting if AI fails for greeting
            ai_response_text = f"Hi there, {message.author.name}! 👋"


    elif intent == 'simple_question':
        context_for_ai = f"A user named {message.author.name} just asked a simple question."
        # Craft a specific prompt for the AI to answer the question
        prompt_for_ai = f"{SINGLE_PERSONA_PROMPT}\n{context_for_ai}\nUser's question: {message.content}\nAnswer the question in character:"
        ai_response_text = await get_gemini_response(prompt_for_ai)
        if ai_response_text:
            logger.info(f"Generated AI response for simple question from {message.author.name}.")
        else:
            logger.warning(f"AI failed to generate response for simple question from {message.author.name}. Falling through to general chat fallback.")
            # If AI failed for simple question, let it fall through to general chat fallback below
            intent = 'general_chat' # Change intent to trigger general chat fallback


    if intent == 'general_chat':
        # This block handles messages that were not greetings or simple questions,
        # or were simple questions where the AI failed to respond.
        prompt_for_ai = f"{SINGLE_PERSONA_PROMPT}\nUser said: {message.content}\nYour response:"
        ai_response_text = await get_gemini_response(prompt_for_ai)
        if ai_response_text:
            logger.info(f"Generated AI general chat response for {message.author.name}.")
        else:
            logger.warning(f"AI failed to generate general chat response for {message.author.name}.")
            # Send a generic error message if AI fails for general chat
            ai_response_text = "I'm sorry, I couldn't process that right now. Please try again later."


    # --- Send the Final AI Response ---
    if ai_response_text:
        # Discord has a 2000 character limit per message.
        # For longer responses, we'll need to implement message splitting later.
        if len(ai_response_text) > 2000:
            logger.warning("AI response exceeds 2000 characters. Truncating.")
            await message.channel.send(ai_response_text[:2000])
        else:
            await message.channel.send(ai_response_text)
    else:
        # This case should ideally not be reached if fallbacks are in place,
        # but as a final safety net:
        logger.error("No AI response text generated and no fallback available.")
        await message.channel.send("An unexpected error occurred while generating a response.")


    # We are not using command_prefix for NLU based interaction,
    # but calling process_commands can help discord.py manage message events.
    await bot.process_commands(message)


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
