const mongoose = require('mongoose');
const { MONGO_URL } = require('../config');

module.exports = async () => {
  await mongoose.connect(MONGO_URL);
  console.log('MongoDB ulandi 🚀');
};
