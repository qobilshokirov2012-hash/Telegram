const { Telegraf, Markup } = require('telegraf');

const bot = new Telegraf(process.env.BOT_TOKEN);
const ADMIN_ID = Number(process.env.ADMIN_ID);

/* ================= MEMORY ================= */
let userData = {};
let activeVip = {};

/* ================= START ================= */
bot.start((ctx) => {
  const id = ctx.from.id;
  const username = ctx.from.username ? `@${ctx.from.username}` : 'yo‘q';
  const date = new Date().toLocaleString();

  ctx.reply(
`👋 Assalomu alaykum!

🎬 Anime Botga xush kelibsiz

━━━━━━━━━━━━━━

👤 ID: ${id}
👤 Username: ${username}
⏰ Start: ${date}

━━━━━━━━━━━━━━

💡 Quyidagilardan foydalaning`,
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

Reklamasiz kontent!

🔆 Tanlang:`,
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

/* ================= VIP SELECT ================= */
bot.action(['vip_15', 'vip_1', 'vip_2'], (ctx) => {
  const userId = ctx.from.id;

  if (activeVip[userId]) {
    return ctx.reply('⚠️ Sizda VIP allaqachon bor!');
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

  ctx.reply(
`📦 Tanlandi: ${muddat}
💰 Narx: ${narx}

💳 To‘lovni davom ettiring`,
    Markup.inlineKeyboard([
      [Markup.button.callback('💳 Karta', 'card')]
    ])
  );
});

/* ================= CARD ================= */
bot.action('card', (ctx) => {
  const userId = ctx.from.id;
  const data = userData[userId];

  if (!data) {
    return ctx.reply('❌ Avval VIP tanlang!');
  }

  ctx.reply(
`💳 TO‘LOV

👤 Egasi: Munira Qobilova
💳 Karta: 6262 5708 0467 1057

📦 Muddat: ${data.muddat}
💰 Narx: ${data.narx}

⚠️ To‘lovdan keyin chek yuboring`
  );
});

/* ================= PHOTO ================= */
bot.on('photo', async (ctx) => {
  const userId = ctx.from.id;
  const data = userData[userId];

  if (!data) {
    return ctx.reply('❌ VIP tanlanmagan!');
  }

  const fileId = ctx.message.photo.at(-1).file_id;

  await ctx.telegram.sendPhoto(
    ADMIN_ID,
    fileId,
    {
      caption:
`💰 Yangi to‘lov

👤 ID: ${userId}
📦 Muddat: ${data.muddat}
💰 Narx: ${data.narx}`,
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

  ctx.reply('📤 Chek admin ga yuborildi');
});

/* ================= ADMIN APPROVE ================= */
bot.action(/ok_(.+)/, async (ctx) => {
  const userId = ctx.match[1];

  activeVip[userId] = true;

  await ctx.telegram.sendMessage(
    userId,
    '✅ To‘lov tasdiqlandi!\n💎 VIP aktivlashtirildi'
  );

  await ctx.editMessageText('✔ Tasdiqlandi');
  await ctx.answerCbQuery('OK');
});

/* ================= ADMIN REJECT ================= */
bot.action(/no_(.+)/, async (ctx) => {
  const userId = ctx.match[1];

  await ctx.telegram.sendMessage(
    userId,
    '❌ To‘lov bekor qilindi'
  );

  await ctx.editMessageText('❌ Bekor qilindi');
  await ctx.answerCbQuery('OK');
});

/* ================= HELP ================= */
bot.command('help', (ctx) => {
  ctx.reply('📞 Support: @AnICenUzbekistan');
});

/* ================= START BOT ================= */
bot.launch();
console.log('BOT ISHGA TUSHDI 🚀');

process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
