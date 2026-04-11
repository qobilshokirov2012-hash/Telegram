const mongoose = require('mongoose');

const animeSchema = new mongoose.Schema({
  code: Number,
  name: String,
  desc: String,
  videoId: String,
  type: String // free / premium
});

module.exports = mongoose.model('Anime', animeSchema);
