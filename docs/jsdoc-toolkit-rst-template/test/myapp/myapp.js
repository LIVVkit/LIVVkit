// Global variables
// @public
gVar = "value";

/**
 * Accelerator value: 9.80665
 * @constant
 */
const ACCEL = 9.80665;

// Local variables

// Methods

/**
 * Set ups the hangar
 * @param {Hangar} hangar
 */
function setup(hangar) {

}

/**
 * @class
 * Simple class for modelling a direction
 * @param {int} x X coordinate
 * @param {int} y Y coordinate
 *
 * @property {number} x X value
 * @property {number} y Y value
 * @deprecated Since version 0.5. You should now plain Object instead: ``{x:234, y:123}``
 */
var Direction = function(x, y) {
  this.x = x;
  this.y = y;
};

/**
 * @class
 * @author Juha Mustonen
 *
 * @description
 * This is a class with no other purpose
 * but being an example and for testing.
 *
 * Second paragraph just to show off:
 *
 * <ul>
 * <li>One</li>
 *   <li>Two</li>
 * </ul>
 *
 * As for the HTML elements, template has a limited support
 * for transforming them into <b>bold</b> and <i>italic</i>
 * elements.
 *
 * @example
 * var android = new Bot("Android");
 * android.speak();
 *
 * @example
 * // Extend bot
 * subapp = new Bot;
 * subapp.prototype.walk = function(direction) {
 *   // ...
 * };
 *
 * @param {string} name Unique name for the bot
 * @version 1.0
 *
 */
var Bot = function (name) {
  // @default "Anonymous"
  this.name = name || 'Anonymous';
};

/**
 * Constructs the Bot
 *
 * @param {string} name Unique name for the bot
 * @constructs App

 */
Bot.prototype.constructor = function (name) {

};

/**
 * This function really does the thing.
 *
 * @example
 * var bot = new Bot('bot');
 * bot.talk({x:123, y:2});
 */
Bot.prototype.talk = function () {
  return this.name;
};

/**
 * This function really does the thing.
 *
 * @param {Direction} direction X and Y coordiates
 * @example
 * var bot = new Bot('bot');
 * bot.walk({x:123, y:2});
 */
Bot.prototype.walk = function (direction) {
  this.move(direction.x, direction.y);
};

/**
 * Change given string into uppercase.
 *
 * @param {string} str String to convert into uppercase
 * @returns {string} app name
 * @private
 */
Bot.prototype._toUpper = function(str) {
  return str.toUpper();
};

/**
 * @class
 * @extends Bot
 * @description
 *
 * Android is a subclass of Bot
 *
 * @constructor
 * Constructs the Android class
 */
Android = function() {};
/**
 * @class
 * Android class
 */
Android.prototype = new Bot();



/**
 * Constructs the Android
 *
 * @param {String} name Unique name for the bot
 * @constructs Android
 */
Android.prototype.constructor = function (name) {

};

/**
 * Makes the Android talk
 * @returns {String} what Android said,
 * in format: "Android said: <message>"
 *
 * @see Bot#talk
 * @see #talk
 */
Android.prototype.talk = function() {
  return "Android said: " + Bot.talk();
};

/**
 * Hangar is a singleton object that is responsible
 * for fixing the bots
 * @namespace Hangar
 *
 * @example
 * var mybot = Bot("test");
 * mybot = Hangar.repair(mybot);
 *
 * @see {@link Bot} Bot
 */
var Hangar = {};

/**
 * @static
 * @param {Bot} bot Bot to repair
 * @returns {Bot} Fixed bot back
 */
Hangar.repair = function(bot) {
  return bot;
};