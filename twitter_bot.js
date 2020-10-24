const config = require('./config');
const twit = require('twit');
const T = new twit(config);

// Possible responses
const messages = ["Bold and brash", 
                  "More like, belongs in the trash!"];
// @ of the bot
const user = "@BoldAndBrashBot";

let stream = T.stream('statuses/filter', { track: [user] });
stream.on('tweet', tweetEvent);

function tweetEvent(tweet) {
    // Get ID of tweet to reply to
    let nameID  = tweet.id_str;

    // Formatting reply, need to include the @ first
    let mention = "@" + tweet.user.screen_name + " ";
    let reply = (Math.random() >= 0.5) ? messages[0] : messages[1];
    let params = {
        status: mention + reply,
        in_reply_to_status_id: nameID
    };

    T.post('statuses/update', params, function(err, data, response) {
      if (err) {
        console.log(err);
      } else {
        console.log('Tweeted: ' + params.status);
      }
    })
};