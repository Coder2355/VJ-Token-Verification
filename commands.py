from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import verify_user, check_token, check_verification, get_token
from info import VERIFY, VERIFY_TUTORIAL, BOT_USERNAME

API_ID = "28015531"
API_HASH = "2ab4ba37fd5d9ebf1353328fc915ad28"
BOT_TOKEN = "7800807621:AAHctirzl9smHyCPXZbtSBkTlyT6vVgKbVE"
BOT_USERNAME = "Hshdgdvdv23bot"
GROUP_ID = -1002176916778

app = Client("group_verification_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)





# Handler to process verification links
@app.on_message(filters.command("start"))
async def verify_start(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Invalid request.")
    
    data = message.command[1]
    if data.split("-", 1)[0] == "verify":
        userid = data.split("-", 2)[1]
        token = data.split("-", 3)[2]
        if str(message.from_user.id) != str(userid):
            return await message.reply_text(
                text="<b>Invalid link or Expired link!</b>",
                protect_content=True
            )
        
        is_valid = await check_token(client, userid, token)
        if is_valid:
            await message.reply_text(
                text=f"<b>Hey {message.from_user.mention}, You are successfully verified!\nNow you have unlimited access for all files till today midnight.</b>",
                protect_content=True
            )
            await verify_user(client, userid, token)
        else:
            return await message.reply_text(
                text="<b>Invalid link or Expired link!</b>",
                protect_content=True
            )


# Handler to check verification before allowing actions
@app.on_message(filters.group)
async def enforce_verification(client, message):
    if VERIFY and not await check_verification(client, message.from_user.id):
        btn = [[
            InlineKeyboardButton(
                "Verify",
                url=await get_token(client, message.from_user.id, f"https://telegram.me/{BOT_USERNAME}?start=verify-{message.from_user.id}-token")
            )
        ], [
            InlineKeyboardButton("How To Open Link & Verify", url=VERIFY_TUTORIAL)
        ]]
        
        await message.reply_text(
            text="<b>You are not verified!\nKindly verify to continue!</b>",
            protect_content=True,
            reply_markup=InlineKeyboardMarkup(btn)
        )
        return

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
