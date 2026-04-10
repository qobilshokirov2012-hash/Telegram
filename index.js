const { Telegraf, Markup } = require('telegraf');
const fs = require('fs');

const bot = new Telegraf(process.env.BOT_TOKEN);
const ADMIN_ID = Number(process.env.ADMIN_ID);

/* ================= DB ================= */
function loadDB() {
  return JSON.parse(fs.readFileSync('./db.json', 'utf8'));
}

function saveDB(data) {
  fs.writeFileSync('./db.json', JSON.stringify(data, null, 2));
}

/* ================= START ================= */
bot.start((ctx) => {
  ctx.reply(
`👋 Anime Botga xush kelibsiz!

📌 Anime kod yuboring yoki pastdagi tugmalardan foydalaning`,
    Markup.inlineKeyboard([
      [Markup.button.callback('📺 Animelar', 'list')],
      [Markup.button.callback('💎 Premium', 'premium')],
      [Markup.button.callback('⚙ Admin Panel', 'admin')]
    ])
  );
});

/* ================= ANIME LIST ================= */
bot.action('list', (ctx) => {
  const db = loadDB();
  const keys = Object.keys(db.anime);

  if (keys.length === 0) {
    return ctx.reply('❌ Hozircha anime yo‘q');
  }

  let text = '📺 ANIMELAR:\n\n';

  keys.forEach((k) => {
    const a = db.anime[k];
    text += `🎬 ${k} (${a.type})\n`;
  });

  ctx.reply(text);
});

/* ================= PREMIUM ================= */
bot.action('premium', (ctx) => {
  ctx.reply('💎 Premium bo‘lim (keyin kengaytiramiz)');
});

/* ================= ADMIN PANEL ================= */
bot.action('admin', (ctx) => {
  if (ctx.from.id !== ADMIN_ID) {
    return ctx.reply('❌ Siz admin emassiz');
  }

  ctx.reply(
`⚙ ADMIN PANEL`,
    Markup.inlineKeyboard([
      [Markup.button.callback('➕ Anime qo‘shish', 'add')],
      [Markup.button.callback('✏ Anime tahrirlash', 'edit')],
      [Markup.button.callback('🗑 Anime o‘chirish', 'del')]
    ])
  );
});

/* ================= ADD ANIME ================= */
let step = {};

bot.action('add', (ctx) => {
  if (ctx.from.id !== ADMIN_ID) return;

  step[ctx.from.id] = { type: 'add' };

  ctx.reply('🎬 Anime nomini yozing:');
});

bot.on('text', (ctx) => {
  const id = ctx.from.id;

  if (id !== ADMIN_ID) return;

  if (!step[id]) return;

  const db = loadDB();

  if (step[id].type === 'add_name') {
    step[id].name = ctx.message.text;
    step[id].type = 'add_desc';

    return ctx.reply('📄 Anime maʼlumotini yozing:');
  }

  if (step[id].type === 'add_desc') {
    db.anime[step[id].name] = {
      desc: ctx.message.text,
      type: 'free'
    };

    saveDB(db);
    step[id] = null;

    return ctx.reply('✅ Anime qo‘shildi');
  }

  if (step[id].type === 'add') {
    step[id].name = ctx.message.text;
    step[id].type = 'add_desc';

    return ctx.reply('📄 Anime maʼlumotini yozing:');
  }
});

/* ================= EDIT ================= */
bot.action('edit', (ctx) => {
  if (ctx.from.id !== ADMIN_ID) return;

  step[ctx.from.id] = { type: 'edit' };

  ctx.reply('✏ Qaysi anime tahrirlanadi? nomini yozing:');
});

bot.on('text', (ctx) => {
  const id = ctx.from.id;
  const db = loadDB();

  if (id !== ADMIN_ID) return;
  if (!step[id]) return;

  if (step[id].type === 'edit') {
    const name = ctx.message.text;

    if (!db.anime[name]) {
      return ctx.reply('❌ Anime topilmadi');
    }

    step[id] = { type: 'edit_desc', name };

    return ctx.reply('📄 Yangi maʼlumot yozing:');
  }

  if (step[id].type === 'edit_desc') {
    db.anime[step[id].name].desc = ctx.message.text;

    saveDB(db);
    step[id] = null;

    return ctx.reply('✅ Yangilandi');
  }
});

/* ================= DELETE ================= */
bot.action('del', (ctx) => {
  if (ctx.from.id !== ADMIN_ID) return;

  step[ctx.from.id] = { type: 'del' };

  ctx.reply('🗑 Qaysi anime o‘chiriladi? nomini yozing:');
});

bot.on('text', (ctx) => {
  const id = ctx.from.id;
  const db = loadDB();

  if (id !== ADMIN_ID) return;
  if (!step[id]) return;

  if (step[id].type === 'del') {
    delete db.anime[ctx.message.text];

    saveDB(db);
    step[id] = null;

    return ctx.reply('🗑 O‘chirildi');
  }
});

/* ================= BOT ================= */
bot.launch();
console.log('BOT STARTED 🚀');
