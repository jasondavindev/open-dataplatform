const faker = require('faker');

const ONE_DAY_TIME = 1000 * 60 * 60 * 24;

class ContentGenerator {
  static _events = ['click', 'page_view', 'submit'];

  static factory() {
    const instance = new ContentGenerator();
    return instance;
  }

  generateRecord = ({ query: { date } }, res) => {
    const record = this._generateRecord(date);

    return res.status(200).json(record);
  };

  generateRecords = ({ query: { date, count = 30 } }, res) => {
    const countParam = parseInt(count);
    const records = Array(countParam)
      .fill(true)
      .map((_) => this._generateRecord(date));

    return res.status(200).json(records);
  };

  _generateRecord = (date) => {
    return {
      username: faker.name.findName(),
      page: faker.internet.url(),
      event_name: ContentGenerator._events[Math.floor(Math.random() * 3)],
      event_time: (new Date(date).getTime() + ONE_DAY_TIME) / 1000,
    };
  };
}

module.exports.ContentGenerator = ContentGenerator;
