# ⚠️⚠️⚠️ TEMPORARY FILE — सिर्फ़ एक बार Migration/Copy के लिए ⚠️⚠️⚠️
# इस्तेमाल:
#   1. इसे /plugins/ फोल्डर में डालें, बॉट restart करें
#   2. बॉट को PM में भेजें:
#        /check_db MONGO_URL [DB_NAME]
#      उदाहरण:
#        /check_db mongodb+srv://user:pass@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
#      (URL ना दें तो अपने आप DATABASE_URL/DATABASE_NAME (info.py) वाला इस्तेमाल होगा)
#   3. बॉट उसी DB का connection status, collections, documents,
#      storage, index size, database size दिखाएगा
#   4. फिर 3 बटन देगा:
#        📋 Copy Database   → पूरा DB नए URI में कॉपी होगा
#        📂 Copy Collection → सिर्फ़ चुनी हुई collection कॉपी होगी
#        🔄 Migrate         → पूरा DB कॉपी होगा + migrate वाला final message
#   5. बटन दबाने के बाद (Copy Collection में पहले collection चुनें) नया
#      MongoDB URI रिप्लाई करें — चाहें तो साथ में DB_NAME भी दे सकते हैं
#      (स्पेस से अलग करके)
#   6. Progress bar के साथ कॉपी होगी
#   7. काम पूरा होने पर पासवर्ड वाला मैसेज Delete करें
#   8. इस्तेमाल के बाद यह फाइल /plugins/ से हटा दें और बॉट restart करें

import time
import motor.motor_asyncio
from hydrogram import Client, filters
from hydrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import ADMINS, DATABASE_URL, DATABASE_NAME

BATCH_SIZE = 500

# user_id -> {"action": "copy_db"/"copy_collection"/"migrate", "collection": str|None}
PENDING = {}
# user_id -> True  (जब collection चुनने का स्टेप चल रहा हो)
CHOOSING_COLLECTION = {}
# user_id -> {"url": str, "db_name": str}  — जो DB /check_db में चेक किया गया था
SOURCE = {}


def _size_fmt(num_bytes):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.2f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.2f} PB"


def _progress_bar(done, total, width=12):
    if total <= 0:
        pct = 0
    else:
        pct = min(100, int(done * 100 / total))
    filled = int(width * pct / 100)
    bar = "▓" * filled + "░" * (width - filled)
    return f"{bar} {pct}%"


@Client.on_message(filters.private & filters.user(ADMINS) & filters.command("check_db"))
async def check_db_cmd(bot, message):
    # /check_db [MONGO_URL] [DB_NAME] — URL ना दें तो info.py वाला default इस्तेमाल होगा
    if len(message.command) > 1:
        check_url = message.command[1]
        check_db_name = message.command[2] if len(message.command) > 2 else DATABASE_NAME
    else:
        check_url = DATABASE_URL
        check_db_name = DATABASE_NAME

    SOURCE[message.from_user.id] = {"url": check_url, "db_name": check_db_name}

    status = await message.reply("🔎 <b>DB की जानकारी निकाली जा रही है...</b>")

    try:
        old_client = motor.motor_asyncio.AsyncIOMotorClient(check_url)
        old_db = old_client[check_db_name]
        await old_client.admin.command("ping")
    except Exception as e:
        return await status.edit(f"❌ <b>DB से कनेक्ट नहीं हो पाया (Auth/Network Error):</b>\n<code>{e}</code>")

    try:
        collections = await old_db.list_collection_names()
        db_stats = await old_db.command("dbStats")
        storage_used = _size_fmt(db_stats.get("storageSize", 0))

        col_lines = []
        total_docs = 0
        for col_name in collections:
            count = await old_db[col_name].count_documents({})
            total_docs += count
            col_lines.append(f"📁 {col_name}\n    Docs : {count:,}")

        text = (
            f"✅ MongoDB Connected\n\n"
            f"Database : {check_db_name}\n"
            f"Collections : {len(collections)}\n\n"
            + "\n\n".join(col_lines) +
            f"\n\nStorage : {storage_used}"
        )

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("📦 Copy Database", callback_data="dbop:copy_db")],
            [InlineKeyboardButton("📁 Select Collections", callback_data="dbop:copy_collection")],
            [InlineKeyboardButton("🔁 Migrate", callback_data="dbop:migrate")],
            [InlineKeyboardButton("❌ Cancel", callback_data="dbop:cancel")],
        ])
        await status.edit(text, reply_markup=buttons)
    except Exception as e:
        await status.edit(f"❌ DB जानकारी निकालने में गलती:\n{e}")


@Client.on_callback_query(filters.user(ADMINS) & filters.regex(r"^dbop:"))
async def dbop_callback(bot, cq):
    action = cq.data.split(":", 1)[1]

    if action == "cancel":
        PENDING.pop(cq.from_user.id, None)
        CHOOSING_COLLECTION.pop(cq.from_user.id, None)
        return await cq.message.edit("❌ Cancel कर दिया गया।")

    if action == "copy_collection":
        src = SOURCE.get(cq.from_user.id, {"url": DATABASE_URL, "db_name": DATABASE_NAME})
        try:
            old_client = motor.motor_asyncio.AsyncIOMotorClient(src["url"])
            old_db = old_client[src["db_name"]]
            collections = await old_db.list_collection_names()
            old_client.close()
        except Exception as e:
            return await cq.message.edit(f"❌ <b>Collections लोड नहीं हो पाईं:</b>\n<code>{e}</code>")

        if not collections:
            return await cq.message.edit("❌ कोई collection नहीं मिली।")

        rows = [[InlineKeyboardButton(c, callback_data=f"colsel:{c}")] for c in collections]
        rows.append([InlineKeyboardButton("❌ Cancel", callback_data="dbop:cancel")])
        CHOOSING_COLLECTION[cq.from_user.id] = True
        await cq.message.edit("📂 <b>किस collection की copy बनानी है?</b>", reply_markup=InlineKeyboardMarkup(rows))
        return await cq.answer()

    # copy_db या migrate
    PENDING[cq.from_user.id] = {"action": action, "collection": None}
    label = "पूरे DB की Copy" if action == "copy_db" else "Migrate"
    await cq.message.edit(
        f"✏️ <b>{label} के लिए नया MongoDB URI भेजें</b> (इसी चैट में रिप्लाई करें):\n\n"
        f"<code>mongodb+srv://user:pass@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority</code>\n\n"
        f"चाहें तो साथ में DB_NAME भी दे सकते हैं, स्पेस से अलग करके:\n"
        f"<code>mongodb+srv://... mydbname</code>\n\n"
        f"रद्द करने के लिए <code>/cancel</code> भेजें।"
    )
    await cq.answer()


@Client.on_callback_query(filters.user(ADMINS) & filters.regex(r"^colsel:"))
async def collection_selected(bot, cq):
    col_name = cq.data.split(":", 1)[1]
    CHOOSING_COLLECTION.pop(cq.from_user.id, None)
    PENDING[cq.from_user.id] = {"action": "copy_collection", "collection": col_name}

    await cq.message.edit(
        f"✏️ <b>collection <code>{col_name}</code> की Copy के लिए नया MongoDB URI भेजें</b>:\n\n"
        f"<code>mongodb+srv://user:pass@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority</code>\n\n"
        f"चाहें तो साथ में DB_NAME भी दे सकते हैं, स्पेस से अलग करके:\n"
        f"<code>mongodb+srv://... mydbname</code>\n\n"
        f"रद्द करने के लिए <code>/cancel</code> भेजें।"
    )
    await cq.answer()


@Client.on_message(filters.private & filters.user(ADMINS) & filters.command("cancel"))
async def cancel_pending(bot, message):
    had = PENDING.pop(message.from_user.id, None) or CHOOSING_COLLECTION.pop(message.from_user.id, None)
    if had:
        await message.reply("❌ Cancel कर दिया गया।")


@Client.on_message(
    filters.private & filters.user(ADMINS) & filters.text & ~filters.command(["check_db", "cancel"])
)
async def receive_new_url(bot, message):
    pending = PENDING.get(message.from_user.id)
    if not pending:
        return  # इस यूज़र का कोई pending action नहीं — दूसरे handlers के लिए छोड़ दें

    parts = message.text.strip().split()
    if not parts or not parts[0].startswith("mongodb"):
        return await message.reply("⚠️ यह सही MongoDB URI नहीं लग रहा। दोबारा भेजें, या <code>/cancel</code> करें।")

    new_url = parts[0]
    db_name = parts[1] if len(parts) > 1 else DATABASE_NAME
    action = pending["action"]
    target_collection = pending.get("collection")
    PENDING.pop(message.from_user.id, None)

    label = {"copy_db": "Copy Database", "copy_collection": f"Copy Collection ({target_collection})",
              "migrate": "Migration"}[action]
    status = await message.reply(f"🚚 <b>{label} शुरू हो रहा है...</b>\n\nनए DB से कनेक्ट किया जा रहा है...")

    src = SOURCE.get(message.from_user.id, {"url": DATABASE_URL, "db_name": DATABASE_NAME})
    try:
        old_client = motor.motor_asyncio.AsyncIOMotorClient(src["url"])
        new_client = motor.motor_asyncio.AsyncIOMotorClient(new_url)
        old_db = old_client[src["db_name"]]
        new_db = new_client[db_name]
        await new_client.admin.command("ping")
    except Exception as e:
        return await status.edit(f"❌ <b>नए DB से कनेक्ट नहीं हो पाया (Auth/Network Error):</b>\n<code>{e}</code>\n\n"
                                  f"👉 Atlas में Network Access में <code>0.0.0.0/0</code> जुड़ा है ना, चेक कर लें।")

    all_collections = await old_db.list_collection_names()
    if not all_collections:
        return await status.edit("❌ पुराने DB में कोई collection नहीं मिली।")

    if action == "copy_collection":
        if target_collection not in all_collections:
            return await status.edit(f"❌ Collection <code>{target_collection}</code> अब मौजूद नहीं है।")
        collections_to_copy = [target_collection]
    else:
        collections_to_copy = all_collections

    grand_total = 0
    last_edit = time.time()

    for col_name in collections_to_copy:
        old_col = old_db[col_name]
        new_col = new_db[col_name]
        total = await old_col.count_documents({})
        copied, batch = 0, []

        async for doc in old_col.find({}):
            batch.append(doc)
            if len(batch) >= BATCH_SIZE:
                copied += await _insert_batch(new_col, batch)
                batch = []
                if time.time() - last_edit > 4:
                    last_edit = time.time()
                    try:
                        await status.edit(
                            f"🚚 <b>{label} जारी है...</b>\n\n"
                            f"📂 <code>{col_name}</code>: {copied}/{total}\n"
                            f"{_progress_bar(copied, total)}"
                        )
                    except Exception:
                        pass

        if batch:
            copied += await _insert_batch(new_col, batch)

        grand_total += copied
        try:
            await status.edit(
                f"✅ <code>{col_name}</code> पूरा: {copied}/{total}\n{_progress_bar(copied, total)}\n\n"
                f"⏳ अगली collection की तरफ़..."
            )
        except Exception:
            pass

    old_client.close()
    new_client.close()

    if action == "migrate":
        final_text = (
            f"🎉 <b>Migration पूरा हुआ!</b>\n\n"
            f"📦 कुल collections: <code>{len(collections_to_copy)}</code>\n"
            f"📄 कुल documents कॉपी हुए: <code>{grand_total}</code>\n\n"
            f"👉 अब Koyeb में <b>DATABASE_URL</b> env var को नए वाले से बदलें और बॉट restart करें।\n"
            f"⚠️ फिर यह मैसेज Delete करें और यह फाइल plugins से हटाकर restart करें।"
        )
    elif action == "copy_collection":
        final_text = (
            f"🎉 <b>Collection Copy बन गई!</b>\n\n"
            f"📂 Collection: <code>{target_collection}</code>\n"
            f"📄 Documents कॉपी हुए: <code>{grand_total}</code>\n\n"
            f"ℹ️ पुराना DB जैसा का वैसा चालू है, कुछ बदलने की ज़रूरत नहीं।\n"
            f"⚠️ यह मैसेज Delete करें (इसमें नया password था)।"
        )
    else:
        final_text = (
            f"🎉 <b>Database Copy बन गई!</b>\n\n"
            f"📦 कुल collections: <code>{len(collections_to_copy)}</code>\n"
            f"📄 कुल documents कॉपी हुए: <code>{grand_total}</code>\n\n"
            f"ℹ️ पुराना DB जैसा का वैसा चालू है, कुछ बदलने की ज़रूरत नहीं।\n"
            f"नया DB सिर्फ़ बैकअप/कॉपी के तौर पर तैयार है।\n"
            f"⚠️ यह मैसेज Delete करें (इसमें नया password था)।"
        )

    await status.edit(final_text)


async def _insert_batch(new_col, batch):
    """duplicate _id (re-run की स्थिति में) पर पूरा batch fail न हो"""
    try:
        res = await new_col.insert_many(batch, ordered=False)
        return len(res.inserted_ids)
    except Exception:
        return len(batch)
