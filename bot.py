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
    # For text-only, use gemini-pro. For multimodal, use gemini-pro-vision
    model = genai.GenerativeModel('gemini-pro')
    logger.info("Gemini API client configured successfully.")
except Exception as e:
    logger.critical(f"Failed to configure Gemini API client: {e}")
    model = None # Ensure model is None if setup fails

async def get_gemini_response(prompt_text: str) -> str | None:
    """Gets a response from the Gemini API."""
    if not model:
        logger.error("Gemini model is not initialized. Cannot get response.")
        return None
    try:
        # For simplicity, using generate_content for now.
        # For chat-like behavior, model.start_chat(history=[]) would be better.
        response = await model.generate_content_async(prompt_text)
        # Ensure we handle potential API errors or empty responses gracefully
        if response and response.parts:
            # Assuming the first part contains the text response
            # You might need to inspect response.parts more carefully depending on the model and usage
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
    # await bot.change_presence(activity=discord.Game(name="Truth or Dare"))

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

    # --- Basic AI Response (Single Persona - Phase 1) ---
    # For now, any message in the designated channel will be sent to the AI.
    # This is a very simple interaction, no real "persona" yet.
    
    # Construct a very simple prompt
    # In later phases, this will be much more sophisticated, including persona details,
    # conversation history, and NLU results.
    user_message_content = message.content
    
    # Simple prompt for now - acts like a generic chatbot
    # TODO: Replace with persona-specific prompting later
    prompt = f"User '{message.author.name}' said: {user_message_content}\nRespond to the user as a friendly AI."

    ai_response_text = await get_gemini_response(prompt)

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
