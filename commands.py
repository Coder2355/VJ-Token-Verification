from utils import verify_user, check_token
from utils import check_verification, get_token
from info import VERIFY, VERIFY_TUTORIAL, BOT_USERNAME
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions

API_ID = "28015531"
API_HASH = "2ab4ba37fd5d9ebf1353328fc915ad28"
BOT_TOKEN = "7800807621:AAHctirzl9smHyCPXZbtSBkTlyT6vVgKbVE"
BOT_USERNAME = "Hshdgdvdv23bot"
GROUP_ID = -1002176916778

app = Client("group_verification_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)



@app.on_message(filters.command("start"))
async def start(client, message):
    # Check if the command has parameters
    if len(message.command) < 2:
        return await message.reply_text(
            text="<b>Welcome to the Verification Bot!</b>\n\n"
                 "It seems you started the bot without a valid link or command.\n"
                 "To use this bot, please follow the instructions or use a valid verification link.",
            protect_content=True
        )

    data = message.command[1]  # Extract the parameter from the command
    if data.split("-", 1)[0] == "verify":  # Check if it's a verification command
        try:
            userid = data.split("-", 2)[1]
            token = data.split("-", 3)[2]
        except IndexError:
            return await message.reply_text(
                text="<b>Invalid verification link! Please check and try again.</b>",
                protect_content=True
            )

        # Verify if the user ID matches
        if str(message.from_user.id) != str(userid):
            return await message.reply_text(
                text="<b>Invalid link or Expired link!</b>",
                protect_content=True
            )

        # Validate the token
        is_valid = await check_token(client, userid, token)
        if is_valid:
            await message.reply_text(
                text=f"<b>Hey {message.from_user.mention}, You are successfully verified!</b>\n\n"
                     "You now have unlimited access to all files until midnight.",
                protect_content=True
            )
            await verify_user(client, userid, token)
        else:
            return await message.reply_text(
                text="<b>Invalid or expired link! Please try again.</b>",
                protect_content=True
            )
    else:
        return await message.reply_text(
            text="<b>Unknown command! Please use a valid link or command.</b>",
            protect_content=True
        )

@app.on_message(filters.group & filters.chat(GROUP_ID) & (filters.video | filters.document | filters.text | filters.audio))
async def button_handler(client, message):

    if not await check_verification(client, message.from_user.id) and VERIFY == True:
        btn = [[
            InlineKeyboardButton("Verify", url=await get_token(client, message.from_user.id, f"https://telegram.me/{BOT_USERNAME}?start="))
        ],[
            InlineKeyboardButton("How To Open Link & Verify", url=VERIFY_TUTORIAL)
        ]]
        await message.reply_text(
            text="<b>You are not verified !\nKindly verify to continue !</b>",
            protect_content=True,
            reply_markup=InlineKeyboardMarkup(btn)
        )
        return


if __name__ == "__main__":
    print("Bot is running...")
    app.run()
