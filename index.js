require('dotenv').config();
const { Telegraf, Markup } = require('telegraf');

const bot = new Telegraf(process.env.BOT_TOKEN);

const ADMIN_ID = process.env.ADMIN_ID;

let userData = {};

/* ================= START ================= */
bot.start((ctx) => {
  const username = ctx.from.username ? `@${ctx.from.username}` : 'username yo‘q';
  const id = ctx.from.id;
  const date = new Date().toLocaleString();

  ctx.reply(
`👋 Assalomu alaykum, hurmatli foydalanuvchi!

🎬 Anime & Bot’ga xush kelibsiz!

━━━━━━━━━━━━━━━━━━━

👤 Siz:
• ID: ${id}
• Username: ${username}
• Start: ${date}

━━━━━━━━━━━━━━━━━━━

💡 Anime kod yuboring yoki tugmalardan foydalaning`,
    Markup.inlineKeyboard([
      [
        Markup.button.callback('💎 Premium', 'premium'),
        Markup.button.url('🎬 Kanal', 'https://t.me/ANICENUZ')
      ]
    ])
  );
});

/* ================= PREMIUM ================= */
bot.action('premium', (ctx) => {
  ctx.answerCbQuery();

  ctx.reply(
`💎 VIP OBUNA

Film va seriallarni reklamasiz tomosha qiling!

🔆 Obuna tanlang:`,
    Markup.inlineKeyboard([
      [
        Markup.button.callback('15 kun - 5000', 'vip_15'),
        Markup.button.callback('1 oy - 8000', 'vip_1')
      ],
      [
        Markup.button.callback('2 oy - 15000', 'vip_2')
      ]
    ])
  );
});

/* ================= TARIFF ================= */
bot.action(['vip_15', 'vip_1', 'vip_2'], (ctx) => {
  let muddat, narx;

  if (ctx.callbackQuery.data === 'vip_15') {
    muddat = '15 kun';
    narx = '5000';
  } else if (ctx.callbackQuery.data === 'vip_1') {
    muddat = '1 oy';
    narx = '8000';
  } else {
    muddat = '2 oy';
    narx = '15000';
  }

  userData[ctx.from.id] = { muddat, narx };

  ctx.answerCbQuery();

  ctx.reply(
`📦 Tanlandi: ${muddat}

💰 To‘lov usuli:`,
    Markup.inlineKeyboard([
      [Markup.button.callback('Karta orqali', 'card')]
    ])
  );
});

/* ================= CARD ================= */
bot.action('card', (ctx) => {
  const data = userData[ctx.from.id];

  ctx.reply(
`💳 TO‘LOV MA’LUMOTI

👤 Egasi: Munira Qobilova
💳 Karta: 6262 5708 0467 1057

📦 Muddat: ${data.muddat}
💰 Narx: ${data.narx}

⚠️ To‘lovdan keyin "To‘lov qildim" ni bosing`,
    Markup.inlineKeyboard([
      [Markup.button.callback('✅ To‘lov qildim', 'paid')]
    ])
  );
});

/* ================= PAID ================= */
bot.action('paid', (ctx) => {
  ctx.reply('📎 Chekni rasm qilib yuboring');
});

/* ================= PHOTO TO ADMIN ================= */
bot.on('photo', async (ctx) => {
  const user = ctx.from;
  const data = userData[user.id];

  await ctx.telegram.sendPhoto(
    ADMIN_ID,
    ctx.message.photo[ctx.message.photo.length - 1].file_id,
    {
      caption:
`💰 Yangi to‘lov

👤 ID: ${user.id}
📦 Muddat: ${data?.muddat}
💰 Narx: ${data?.narx}`,
      reply_markup: {
        inline_keyboard: [
          [
            { text: '✔ Tasdiqlash', callback_data: `ok_${user.id}` },
            { text: '❌ Bekor qilish', callback_data: `no_${user.id}` }
          ]
        ]
      }
    }
  );

  ctx.reply('📤 Admin ko‘rib chiqadi');
});

/* ================= ADMIN ACTION ================= */
bot.action(/ok_(.+)/, async (ctx) => {
  const id = ctx.match[1];
  await ctx.telegram.sendMessage(id, '✅ To‘lov tasdiqlandi!');
  ctx.editMessageText('✔ Tasdiqlandi');
});

bot.action(/no_(.+)/, async (ctx) => {
  const id = ctx.match[1];
  await ctx.telegram.sendMessage(id, '❌ To‘lov bekor qilindi');
  ctx.editMessageText('❌ Bekor qilindi');
});

/* ================= BOT START ================= */
bot.launch();
console.log('Bot ishga tushdi 🚀');

process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
require('dotenv').config();
const { Telegraf } = require('telegraf');

const bot = new Telegraf(process.env.BOT_TOKEN);

const ADMIN_ID = Number(process.env.ADMIN_ID);

let userData = {};
let activeVip = {};

/* ================= VIP SELECT ================= */
bot.action(['vip_15', 'vip_1', 'vip_2'], (ctx) => {
  const userId = ctx.from.id;

  // ❌ VIP bor bo‘lsa
  if (activeVip[userId]) {
    return ctx.reply('⚠️ Sizda allaqachon aktiv VIP bor!');
  }

  let muddat = '';
  let narx = '';

  if (ctx.callbackQuery.data === 'vip_15') {
    muddat = '15 kun';
    narx = '5000';
  } else if (ctx.callbackQuery.data === 'vip_1') {
    muddat = '1 oy';
    narx = '8000';
  } else {
    muddat = '2 oy';
    narx = '15000';
  }

  userData[userId] = { muddat, narx };

  ctx.answerCbQuery();

  ctx.reply(
`📦 Tanlandi: ${muddat}
💰 Narx: ${narx}

💳 To‘lovni davom ettiring`,
  );
});

/* ================= CARD ================= */
bot.action('card', (ctx) => {
  const userId = ctx.from.id;
  const data = userData[userId];

  if (!data) {
    return ctx.reply('❌ Siz hali VIP tanlamagansiz!');
  }

  ctx.reply(
`💳 TO‘LOV MA’LUMOTI

👤 Egasi: Munira Qobilova
💳 Karta: 6262 5708 0467 1057

📦 Muddat: ${data.muddat}
💰 Narx: ${data.narx}

⚠️ To‘lovdan keyin chek yuboring`
  );
});

/* ================= PHOTO (ADMIN CHECK) ================= */
bot.on('photo', async (ctx) => {
  const userId = ctx.from.id;
  const data = userData[userId];

  if (!data) {
    return ctx.reply('❌ Siz VIP tanlamagansiz!');
  }

  const fileId = ctx.message.photo.at(-1).file_id;

  await ctx.telegram.sendPhoto(
    ADMIN_ID,
    fileId,
    {
      caption:
`💰 Yangi to‘lov

👤 ID: ${userId}
📦 Muddat: ${data?.muddat || 'BELGILANMAGAN'}
💰 Narx: ${data?.narx || 'BELGILANMAGAN'}`,
      reply_markup: {
        inline_keyboard: [
          [
            { text: '✔ Tasdiqlash', callback_data: `ok_${userId}` },
            { text: '❌ Bekor qilish', callback_data: `no_${userId}` }
          ]
        ]
      }
    }
  );

  ctx.reply('📤 Chek yuborildi');
});

/* ================= APPROVE ================= */
bot.action(/ok_(.+)/, async (ctx) => {
  const userId = ctx.match[1];

  activeVip[userId] = true;

  await ctx.telegram.sendMessage(
    userId,
    '✅ To‘lov tasdiqlandi!\n💎 VIP aktivlashtirildi'
  );

  ctx.editMessageText('✔ Tasdiqlandi');
});

/* ================= REJECT ================= */
bot.action(/no_(.+)/, async (ctx) => {
  const userId = ctx.match[1];

  await ctx.telegram.sendMessage(
    userId,
    '❌ To‘lov bekor qilindi'
  );

  ctx.editMessageText('❌ Bekor qilindi');
});

/* ================= SAFETY COMMAND ================= */
bot.command('id', (ctx) => {
  ctx.reply(ctx.from.id.toString());
});

bot.launch();
console.log('Bot ishga tushdi 🚀');

process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
