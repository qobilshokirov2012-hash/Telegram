# 🤖 Anime Discord Bot

Discord uchun anime bot — MyAnimeList ma'lumotlari asosida ishlaydi.

## Buyruqlar

| Buyruq | Tavsif |
|--------|--------|
| `!anime <nomi>` | Anime qidirish |
| `!manga <nomi>` | Manga qidirish |
| `!karakter <ism>` | Karakter haqida ma'lumot |
| `!topanime` | Top 10 anime ro'yxati |
| `!random` | Tasodifiy anime tavsiya |
| `!sezon` | Joriy mavsum animelari |
| `!janr <janr>` | Janr bo'yicha anime |
| `!yordamanime` | Barcha buyruqlar |

## Railway + GitHub orqali Deploy qilish

### 1-qadam: Discord Bot yaratish
1. [Discord Developer Portal](https://discord.com/developers/applications) ga kiring
2. "New Application" tugmasini bosing, nom bering
3. "Bot" bo'limiga o'ting → "Add Bot"
4. "Reset Token" tugmasini bosib tokenni nusxalab oling
5. "Privileged Gateway Intents" bo'limida **Message Content Intent** ni yoqing
6. "OAuth2 → URL Generator" bo'limidan bot uchun URL yarating:
   - Scopes: `bot`
   - Bot Permissions: `Send Messages`, `Embed Links`, `Read Message History`
7. Linkni brauzerda ochib botni serveringizga qo'shing

### 2-qadam: GitHub ga yuklash
```bash
cd anime-bot
git init
git add .
git commit -m "Anime bot - birinchi versiya"
git branch -M main
git remote add origin https://github.com/SIZNING_USERNAME/anime-bot.git
git push -u origin main
```

### 3-qadam: Railway da deploy
1. [Railway.app](https://railway.app) ga kiring
2. "New Project" → "Deploy from GitHub repo"
3. Repozitoriyangizni tanlang
4. **Variables** bo'limiga o'ting va qo'shing:
   ```
   DISCORD_TOKEN = your_token_here
   ```
5. Deploy avtomatik boshlanadi!

## Mahalliy ishga tushirish

```bash
pip install -r requirements.txt
cp .env.example .env
# .env faylini tahrirlang va tokenni qo'ying
python bot.py
```
