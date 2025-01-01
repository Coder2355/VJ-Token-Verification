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





@app.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if len(message.command) !=2:
        return await message.reply("hi welcome to token verify bot")
    data = message.command[1]
    try:
        pre, file_id = data.split('_', 1)
    except:
        file_id = data
        pre = ""
    if data.split("-", 1)[0] == "verify":
        userid = data.split("-", 2)[1]
        token = data.split("-", 3)[2]
        if str(message.from_user.id) != str(userid):
            return await message.reply_text(
                text="<b>Invalid link or Expired link !</b>",
                protect_content=True
            )
        is_valid = await check_token(client, userid, token)
        if is_valid == True:
            await message.reply_text(
                text=f"<b>Hey {message.from_user.mention}, You are successfully verified !\nNow you have unlimited access for all files till today midnight.</b>",
                protect_content=True
            )
            await verify_user(client, userid, token)
        else:
            return await message.reply_text(
                text="<b>Invalid link or Expired link !</b>",
                protect_content=True
            )
    elif data.split("-", 1)[0] == "BATCH":
        try:
            if not await check_verification(client, message.from_user.id) and VERIFY_MODE == True:
                btn = [[
                    InlineKeyboardButton("Verify", url=await get_token(client, message.from_user.id, f"https://telegram.me/{username}?start="))
                ],[
                    InlineKeyboardButton("How To Open Link & Verify", url=VERIFY_TUTORIAL)
                ]]
                await message.reply_text(
                    text="<b>You are not verified !\nKindly verify to continue !</b>",
                    protect_content=True,
                    reply_markup=InlineKeyboardMarkup(btn)
                )
                return
        except Exception as e:
            return await message.reply_text(f"**Error - {e}**")


if __name__ == "__main__":
    print("Bot is running...")
    app.run()
