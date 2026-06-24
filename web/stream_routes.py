import os
import math
import mimetypes
import logging
from urllib.parse import quote
from aiohttp import web
from info import BIN_CHANNEL
from utils import temp
from core.tg_streamer import SmartStreamer

routes = web.RouteTableDef()
logger = logging.getLogger(__name__)
streamer = SmartStreamer()

# ─────────────────────────────────────────────
# 🏠 ROOT ROUTE
# ─────────────────────────────────────────────
@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.Response(text="<h1>✅ Fast Finder Stream Engine is Active!</h1>", content_type='text/html')

# ─────────────────────────────────────────────
# 📺 HTML PLAYER ROUTE (player.html को लोड करता है)
# ─────────────────────────────────────────────
@routes.get("/watch/{message_id}")
async def watch_handler(request):
    try:
        msg_id = int(request.match_info['message_id'])
        msg = await temp.BOT.get_messages(BIN_CHANNEL, msg_id)
        media = getattr(msg, msg.media.value, None) if msg and msg.media else None

        if not media:
            return web.Response(status=404, text="<h1>❌ File Not Found</h1>", content_type='text/html')

        file_name = getattr(media, "file_name", "Fast Finder Stream")
        mime = getattr(media, "mime_type", "video/mp4")
        
        src_url = f"/stream/{msg_id}"
        download_url = f"/download/{msg_id}"

        # player.html का पाथ ढूँढना (चाहे बॉट रूट में हो या सब-फ़ोल्डर में)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        player_path = os.path.join(base_dir, "web", "player.html")
        
        if not os.path.exists(player_path):
            player_path = os.path.join("web", "player.html")

        # HTML फ़ाइल को पढ़ना और प्लेसहोल्डर्स को असली डेटा से बदलना
        with open(player_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        html_content = html_content.replace("{{src}}", src_url)
        html_content = html_content.replace("{{download_src}}", download_url)
        html_content = html_content.replace("{{file_name}}", file_name)
        html_content = html_content.replace("{{mime_type}}", mime)

        return web.Response(text=html_content, content_type='text/html')
        
    except Exception as e:
        logger.error(f"Error in watch_handler: {e}")
        return web.Response(status=500, text=f"Internal Server Error: {e}")

# ─────────────────────────────────────────────
# ⚡ SMART STREAMING & DOWNLOAD ROUTE (0% RAM OVERHEAD)
# ─────────────────────────────────────────────
@routes.get("/stream/{message_id}")
@routes.get("/download/{message_id}")
async def stream_download_handler(request):
    try:
        msg_id = int(request.match_info['message_id'])
        is_download = "download" in request.path

        msg = await temp.BOT.get_messages(BIN_CHANNEL, msg_id)
        media = getattr(msg, msg.media.value, None) if msg and msg.media else None

        if not media:
            return web.Response(status=404, text="Media Not Found")

        file_size = media.file_size
        file_name = getattr(media, 'file_name', "video.mp4")
        mime_type = getattr(media, 'mime_type', None) or mimetypes.guess_type(file_name)[0] or "application/octet-stream"

        # ब्राउज़र के Range Header की गणना करना (ताकि वीडियो को आगे-पीछे सीक किया जा सके)
        range_header = request.headers.get("Range")
        fb, ub = 0, file_size - 1
        
        if range_header:
            parts = range_header.replace("bytes=", "").split("-")
            fb = int(parts[0]) if parts[0] else 0
            ub = int(parts[1]) if parts[1] else file_size - 1

        ub = min(ub, file_size - 1)
        req_len = ub - fb + 1

        if fb < 0 or ub < fb:
            return web.Response(status=416, text="416: Range Not Satisfiable", headers={"Content-Range": f"bytes */{file_size}"})

        # aiohttp का StreamResponse सेटअप — यह डेटा को बिना RAM में रोके सीधे ब्राउज़र में भेजता है
        response = web.StreamResponse(
            status=206 if range_header else 200,
            headers={
                "Content-Type": mime_type,
                "Content-Range": f"bytes {fb}-{ub}/{file_size}",
                "Accept-Ranges": "bytes",
                "Content-Length": str(req_len),
                "Content-Disposition": f'{"attachment" if is_download else "inline"}; filename="{quote(file_name)}"'
            }
        )
        await response.prepare(request)

        # core/tg_streamer.py के इंजन से डेटा के टुकड़े (Chunks) लेकर सीधे यूज़र तक पहुँचाना
        async for chunk in streamer.stream_file(msg, fb, ub):
            await response.write(chunk)

        return response
        
    except Exception as e:
        logger.warning(f"Client disconnected or streaming exception occurred: {e}")
        return web.Response(status=500, text="Stream Error")
