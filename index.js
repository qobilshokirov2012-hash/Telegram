const { Telegraf, Markup } = require('telegraf');
const fs = require('fs');

const bot = new Telegraf(process.env.BOT_TOKEN);

const ADMIN_ID = Number(process.env.ADMIN_ID);

let db = JSON.parse(fs.readFileSync('./db.json', 'utf8'));

function saveDB() {
  fs.writeFileSync('./db.json', JSON.stringify(db, null, 2));
}

/* ================= START ================= */
bot.start((ctx) => {
  const user = ctx.from;

  if (!db.users[user.id]) {
    db.users[user.id] = {
      id: user.id,
      username: user.username || "yo'q",
      join: new Date()
    };
    saveDB();
  }

  const name = user.first_name || "Foydalanuvchi";
  const username = user.username ? `@${user.username}` : "yo'q";

  ctx.reply(
`👋 Assalomu alaykum👋🏻 hurmatli ${name}!

🎬 AnICen Bot ga xush kelibsiz!

━━━━━━━━━━━━━━

👤 Siz haqingizda:
🆔 ID: ${user.id}
👤 User: ${username}
🎫 Kanken ID: AnICen•${Math.floor(Math.random() * 999999)}

🕒 Start: ${new Date().toLocaleString()}

━━━━━━━━━━━━━━

📺 Anime kodlar
💎 Premium VIP
⚙ Admin panel`,
    Markup.inlineKeyboard([
      [
        Markup.button.callback('📺 Animelar', 'anime'),
        Markup.button.callback('💎 Premium', 'vip')
      ],
      [
        Markup.button.callback('⚙ Admin Panel', 'admin')
      ]
    ])
  );
});

/* ================= ANIME LIST ================= */
bot.action('anime', (ctx) => {
  let text = "📺 ANIMELAR:\n\n";

  Object.keys(db.anime).forEach((k) => {
    text += `🎬 ${k}\n`;
  });

  ctx.reply(text || "Anime yo‘q");
});

/* ================= VIP ================= */
bot.action('vip', (ctx) => {
  ctx.reply(
`💎 Premium bo‘lim

⚠️ Muddat: 5 kun - 5 oy`,
    Markup.inlineKeyboard([
      [Markup.button.callback('15 kun - 5000', 'vip_15')],
      [Markup.button.callback('1 oy - 8000', 'vip_1')],
      [Markup.button.callback('2 oy - 15000', 'vip_2')]
    ])
  );
});

let vipTemp = {};

/* ================= VIP SELECT ================= */
bot.action(/vip_(.+)/, (ctx) => {
  const type = ctx.match[1];

  let muddat = "";
  let narx = "";

  if (type === "15") {
    muddat = "15 kun";
    narx = "5000";
  }
  if (type === "1") {
    muddat = "1 oy";
    narx = "8000";
  }
  if (type === "2") {
    muddat = "2 oy";
    narx = "15000";
  }

  vipTemp[ctx.from.id] = { muddat, narx };

  ctx.reply(
`📦 Muddat: ${muddat}
💰 Narx: ${narx}

💳 To‘lov qiling`,
    Markup.inlineKeyboard([
      [Markup.button.callback('Karta orqali', 'pay')]
    ])
  );
});

/* ================= PAYMENT ================= */
bot.action('pay', (ctx) => {
  const data = vipTemp[ctx.from.id];

  ctx.reply(
`💳 To‘lov:
👤 Egasi: Munira Qobilova
💳 Karta: 6262 5708 0467 1057

📦 ${data.muddat}
💰 ${data.narx}

✔ To‘lov qilgandan keyin chek yuboring`,
    Markup.inlineKeyboard([
      [Markup.button.callback('✅ To‘lov qildim', 'paid')]
    ])
  );
});

/* ================= PAID ================= */
bot.action('paid', (ctx) => {
  ctx.reply("📎 Chek yuboring (rasm)");
});

/* ================= ADMIN PANEL ================= */
bot.action('admin', (ctx) => {
  if (ctx.from.id !== ADMIN_ID) {
    return ctx.reply("❌ Ruxsat yo‘q");
  }

  ctx.reply(
`⚙ ADMIN PANEL`,
    Markup.inlineKeyboard([
      [Markup.button.callback('➕ Anime qo‘shish', 'add')]
    ])
  );
});

/* ================= ADD ANIME ================= */
let step = {};

bot.action('add', (ctx) => {
  if (ctx.from.id !== ADMIN_ID) return;

  step[ctx.from.id] = { stage: "name" };

  ctx.reply("🎬 Anime nomini yozing:");
});

bot.on('text', (ctx) => {
  const id = ctx.from.id;

  if (!step[id]) return;

  if (step[id].stage === "name") {
    step[id].name = ctx.message.text;
    step[id].stage = "desc";

    return ctx.reply("📩 Anime description yozing:");
  }

  if (step[id].stage === "desc") {
    db.anime[step[id].name] = {
      desc: ctx.message.text
    };

    saveDB();
    step[id] = null;

    return ctx.reply("✅ Anime qo‘shildi");
  }
});

/* ================= BOT START ================= */
bot.launch();
console.log("BOT RUNNING 🚀");
