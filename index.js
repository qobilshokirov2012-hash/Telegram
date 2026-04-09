require('dotenv').config();
const { Telegraf } = require('telegraf');

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.start((ctx) => {
  ctx.reply('Assalomu alaykum! Bot ishga tushdi ✅');
});

bot.launch().then(() => {
  console.log('Bot ishga tushdi 🚀');
});

process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
