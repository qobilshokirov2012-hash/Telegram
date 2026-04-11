const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  userId: Number,
  username: String,
  vip: {
    active: { type: Boolean, default: false },
    expireAt: Date
  }
});

module.exports = mongoose.model('User', userSchema);
