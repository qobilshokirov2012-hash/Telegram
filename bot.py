import discord
from discord.ext import commands
import aiohttp
import random
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

JIKAN_BASE = "https://api.jikan.moe/v4"

async def jikan_get(session, endpoint):
    async with session.get(f"{JIKAN_BASE}{endpoint}") as resp:
        if resp.status == 200:
            return await resp.json()
        return None

@bot.event
async def on_ready():
    print(f"Bot tayyor: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} ta slash buyruq sinxronlandi")
    except Exception as e:
        print(f"Sinxronlash xatosi: {e}")

@bot.command(name="anime")
async def anime_search(ctx, *, qidiruv: str):
    """Anime qidirish: !anime <nomi>"""
    async with aiohttp.ClientSession() as session:
        data = await jikan_get(session, f"/anime?q={qidiruv}&limit=1")
        if not data or not data.get("data"):
            await ctx.send("❌ Hech narsa topilmadi.")
            return
        a = data["data"][0]
        embed = discord.Embed(
            title=a.get("title", "Noma'lum"),
            url=a.get("url", ""),
            description=a.get("synopsis", "Ma'lumot yo'q")[:300] + "...",
            color=0xFF6B9D
        )
        if a.get("images", {}).get("jpg", {}).get("image_url"):
            embed.set_thumbnail(url=a["images"]["jpg"]["image_url"])
        embed.add_field(name="⭐ Reyting", value=a.get("score", "N/A"), inline=True)
        embed.add_field(name="📺 Epizodlar", value=a.get("episodes", "N/A"), inline=True)
        embed.add_field(name="📊 Status", value=a.get("status", "N/A"), inline=True)
        embed.add_field(name="🎭 Janr", value=", ".join([g["name"] for g in a.get("genres", [])[:3]]) or "N/A", inline=False)
        embed.set_footer(text="Ma'lumot: MyAnimeList")
        await ctx.send(embed=embed)

@bot.command(name="manga")
async def manga_search(ctx, *, qidiruv: str):
    """Manga qidirish: !manga <nomi>"""
    async with aiohttp.ClientSession() as session:
        data = await jikan_get(session, f"/manga?q={qidiruv}&limit=1")
        if not data or not data.get("data"):
            await ctx.send("❌ Hech narsa topilmadi.")
            return
        m = data["data"][0]
        embed = discord.Embed(
            title=m.get("title", "Noma'lum"),
            url=m.get("url", ""),
            description=m.get("synopsis", "Ma'lumot yo'q")[:300] + "...",
            color=0x9B59B6
        )
        if m.get("images", {}).get("jpg", {}).get("image_url"):
            embed.set_thumbnail(url=m["images"]["jpg"]["image_url"])
        embed.add_field(name="⭐ Reyting", value=m.get("score", "N/A"), inline=True)
        embed.add_field(name="📖 Boblar", value=m.get("chapters", "N/A"), inline=True)
        embed.add_field(name="📊 Status", value=m.get("status", "N/A"), inline=True)
        embed.set_footer(text="Ma'lumot: MyAnimeList")
        await ctx.send(embed=embed)

@bot.command(name="karakter")
async def character_search(ctx, *, qidiruv: str):
    """Karakter qidirish: !karakter <ism>"""
    async with aiohttp.ClientSession() as session:
        data = await jikan_get(session, f"/characters?q={qidiruv}&limit=1")
        if not data or not data.get("data"):
            await ctx.send("❌ Karakter topilmadi.")
            return
        c = data["data"][0]
        embed = discord.Embed(
            title=c.get("name", "Noma'lum"),
            url=c.get("url", ""),
            description=c.get("about", "Ma'lumot yo'q")[:300] + "...",
            color=0x1ABC9C
        )
        if c.get("images", {}).get("jpg", {}).get("image_url"):
            embed.set_thumbnail(url=c["images"]["jpg"]["image_url"])
        embed.add_field(
            name="🎬 Animeda",
            value=", ".join([a["anime"]["title"] for a in c.get("anime", [])[:3]]) or "N/A",
            inline=False
        )
        embed.set_footer(text="Ma'lumot: MyAnimeList")
        await ctx.send(embed=embed)

@bot.command(name="topanime")
async def top_anime(ctx):
    """Eng yaxshi 10 ta anime ro'yxati: !topanime"""
    async with aiohttp.ClientSession() as session:
        data = await jikan_get(session, "/top/anime?limit=10")
        if not data or not data.get("data"):
            await ctx.send("❌ Ma'lumot olishda xato.")
            return
        embed = discord.Embed(title="🏆 Top 10 Anime", color=0xF39C12)
        for i, a in enumerate(data["data"][:10], 1):
            embed.add_field(
                name=f"{i}. {a.get('title', 'N/A')}",
                value=f"⭐ {a.get('score', 'N/A')} | 📺 {a.get('episodes', '?')} ep",
                inline=False
            )
        embed.set_footer(text="Ma'lumot: MyAnimeList")
        await ctx.send(embed=embed)

@bot.command(name="random")
async def random_anime(ctx):
    """Tasodifiy anime: !random"""
    async with aiohttp.ClientSession() as session:
        data = await jikan_get(session, "/random/anime")
        if not data or not data.get("data"):
            await ctx.send("❌ Xato yuz berdi.")
            return
        a = data["data"]
        embed = discord.Embed(
            title=f"🎲 Tasodifiy: {a.get('title', 'Noma'lum')}",
            url=a.get("url", ""),
            description=a.get("synopsis", "Ma'lumot yo'q")[:300] + "...",
            color=0xE74C3C
        )
        if a.get("images", {}).get("jpg", {}).get("image_url"):
            embed.set_thumbnail(url=a["images"]["jpg"]["image_url"])
        embed.add_field(name="⭐ Reyting", value=a.get("score", "N/A"), inline=True)
        embed.add_field(name="📺 Epizodlar", value=a.get("episodes", "N/A"), inline=True)
        embed.add_field(name="🎭 Janr", value=", ".join([g["name"] for g in a.get("genres", [])[:3]]) or "N/A", inline=False)
        embed.set_footer(text="Ma'lumot: MyAnimeList")
        await ctx.send(embed=embed)

@bot.command(name="sezon")
async def current_season(ctx):
    """Joriy mavsum animelari: !sezon"""
    async with aiohttp.ClientSession() as session:
        data = await jikan_get(session, "/seasons/now?limit=10")
        if not data or not data.get("data"):
            await ctx.send("❌ Ma'lumot olishda xato.")
            return
        embed = discord.Embed(title="🌸 Joriy Mavsum Animelari", color=0x3498DB)
        for a in data["data"][:10]:
            embed.add_field(
                name=a.get("title", "N/A"),
                value=f"⭐ {a.get('score', 'N/A')} | 📺 {a.get('episodes', '?')} ep",
                inline=True
            )
        embed.set_footer(text="Ma'lumot: MyAnimeList")
        await ctx.send(embed=embed)

@bot.command(name="janr")
async def anime_by_genre(ctx, *, janr: str):
    """Janr bo'yicha qidirish: !janr <janr nomi>"""
    janrlar = {
        "akshun": 1, "sarguzasht": 2, "avtomobillar": 3, "komediya": 4,
        "drama": 8, "fantastika": 24, "fanteziya": 10, "o'yin": 11,
        "qo'rqinchli": 14, "jodugar": 16, "musiqiy": 19, "sirli": 7,
        "romantika": 22, "maktab": 23, "sport": 30
    }
    janr_id = janrlar.get(janr.lower())
    if not janr_id:
        mavjud = ", ".join(janrlar.keys())
        await ctx.send(f"❌ Janr topilmadi.\n✅ Mavjud janrlar: {mavjud}")
        return
    async with aiohttp.ClientSession() as session:
        data = await jikan_get(session, f"/anime?genres={janr_id}&order_by=score&sort=desc&limit=5")
        if not data or not data.get("data"):
            await ctx.send("❌ Bu janrda anime topilmadi.")
            return
        embed = discord.Embed(title=f"🎭 {janr.capitalize()} janridagi top animeler", color=0x27AE60)
        for a in data["data"][:5]:
            embed.add_field(
                name=a.get("title", "N/A"),
                value=f"⭐ {a.get('score', 'N/A')} | 📺 {a.get('episodes', '?')} ep",
                inline=False
            )
        embed.set_footer(text="Ma'lumot: MyAnimeList")
        await ctx.send(embed=embed)

@bot.command(name="yordamanime")
async def help_anime(ctx):
    """Barcha buyruqlar ro'yxati: !yordamanime"""
    embed = discord.Embed(
        title="🤖 Anime Bot — Buyruqlar",
        description="Quyidagi buyruqlardan foydalaning:",
        color=0xFF6B9D
    )
    embed.add_field(name="!anime <nomi>", value="Anime qidirish", inline=False)
    embed.add_field(name="!manga <nomi>", value="Manga qidirish", inline=False)
    embed.add_field(name="!karakter <ism>", value="Karakter haqida ma'lumot", inline=False)
    embed.add_field(name="!topanime", value="Top 10 anime ro'yxati", inline=False)
    embed.add_field(name="!random", value="Tasodifiy anime tavsiya", inline=False)
    embed.add_field(name="!sezon", value="Joriy mavsum animelari", inline=False)
    embed.add_field(name="!janr <janr>", value="Janr bo'yicha anime", inline=False)
    embed.set_footer(text="Ma'lumot: MyAnimeList (Jikan API)")
    await ctx.send(embed=embed)

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN muhit o'zgaruvchisi topilmadi!")

bot.run(TOKEN)
      
