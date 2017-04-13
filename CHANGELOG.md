## April 12th, 2017: Joshua
**FINISHED ITEMS**

- Python 3 Support
- Major refactor to make style more pythonic
- Organizing objects into modules


## April 11th, 2014: Joshua
**FINISHED ITEMS**

- Added support for loading plain resource files.
- Working on OSX support.


## January, 27th 2007: Joshua
**FINISHED ITEMS**

- Lots of changes!
- Last Boss Art.
- Polish, polish, polish...


## January, 10th 2007:  Jony
**FINISHED ITEMS**

- Consolidated gem code into a single file.

- New gem types - Duel Shot, Fast Shot.

- Balanced game play.

- When the player has both reflect and damage the images switch.

- Unique songs in each world as well as a unique song for the menu.

- Yurei now spawn when Baake Boss is injured, they are now not killable

- Cleaned up Batto spawning code.

- created new Class to make just a surface with text on it.

- Created enemy class


## January 2nd, 2007: Joshua
**FINISHED ITEMS**

- Created an Animation class to simplify Actor animations.

- Created a particleEmitter class to simplify particle effects.

- Added self = None to Actor's die()

- Various new image files.


## December ??, 2006 Jony
**FINISHED ITEMS**

- Placed player firing sound in its own channel.

- While shooting a song plays loudly, when the player stops shooting the song fades to quiet.

- Limited the number of Rokubi on the screen to 10.

- Made use of bullet timers to cut player shooting in half.

- Added a 'dong' effect when the Baake are hit by a bullet.

- Baake now leave the screen as the boss fight begins instead of just disappearing.  Small bug, Baake make one more turn after the start of the boss fight.

- Balenced sounds to make them work better together.

- Picking up gems now has a sound effect.

- Added new enemy Haoya, which moves towards the player then charges within so close.

- Forced nova drops every 10 spawns during boss fights

- Added a short delay between the end of the stages and a boss fight.

- Changed Nova bound style to BOUND_STYLE_NONE

- Fixed a bug with Yurei spawning that would cause them to kill themselves as they were spawned.

- The boss will now leave the screen before next level/world starts.  Enemies also stop spawning once the boss has been killed.  This is a bit boring to sit through when the boss has a long ways to go.

- Cleaned up player hurt code.

- Added another world and the ability to dynamically create and exit worlds.

- Created and added music to the game.

- Added function setTimer to text.py.  Allows for adding a life timer after the creation of the text object.

- Player gains their lives times 5000 points when they kill a boss.  This is displayed on the screen as a counter.

- Made use of options menu.  Reworked the menus so that there is only one option menu, has particles, music, and sound effects.  Fully functional and saves the settings when the program is closed.

- Reduced the number of stars in a nova.

- Nova stars now spin as they move.

- The boss now 'charges' at the player every ten seconds once the boss' life is equal to the level plus 1.  The boss now 'summons' Yurei to help him once the boss' life is equal to the level.

- Added a screen at the end of each world that tells the player that they beat the world and what score they got.  Reset player.lives back to 3, also reset player.score.

- Misc. other changes.


## December ??, 2006 Joshua
**FINISHED ITEMS**

- Player now has hurt method that handles damaging the player.

- Player now has an incrementScore method that handles player scoring.

- Fixed bug in Player's fire method.

- The player now has lives. Every 50,000 points earns an additional life.

- The play is now invincible for a short duration after losing a life.

- Renamed font.py to text.py.

- Rewrote how scoring works. Game now runs faster. :)

- Created Icon class. Good for creating static images that don't need to be created over and over.

- Added place holder sounds.


## December ??, 2006 Jony
**FINISHED ITEMS**

- Battos now follow a leader as they move.

- Debug damage bonus code.


## November 13th, 2006: Joshua
**FINISHED ITEMS**

- Added animation for stars and particles.

- Tweaked how Reflect Gems work. The bullets no longer last forver (3 seconds) and the bonus time is a little bit longer (1.5 seconds).

- Fixed spawn_off_screen.

- Added new boss image and animation. Fixed boss accordingly.

#
## November 7th, 2006: Jony
**FINISHED ITEMS**

- Implimented boss fights at the end of each level. All creatures that are to spawn during a boss fight must be listed as the last stage of the level.  The boss itself must, upon its death, change the level and call load_level().

- Made a simple boss based off the Baake.  Who is 'stunned' when he is hit by a nova.  Bosses health based off of what level in the world the player is on.

- Fixed a crash bug associated with gem_damagex2 and gem_reflect.  Their duration is now handled within the player.

- Reflect and damage bonuses reset when a player goes to a new level.

- Added timer to the start of levels that delays the spawning of enemies for 2 seconds.

- Changed actor types to be more simple.  Improves readability of collision code.  Enemies that use a standard reaction to collision now are ACTOR_ENEMY.  Baakes and bosses have their own actor types, ACTOR_BAAKE and ACTOR_BOSS.  Each boss will handle its own collision.

- Fixed bug with get_closest that would cause objects being checked to be added into additional groups. This could lead to an object being in thousands of groups.


## November 7th, 2006: Joshua
**FINISHED ITEMS**

- BUGFIX Error when Enemy dies and last_collided = Non-Player

- BUGFIX Actors can now die() only once.

- Removed scale and rotation for a speed improvement.

- Added and implemented a particle system.


## October 26th, 2006: Jony
**FINISHED ITEMS**

- Created new AI, in aitools, arc_to_target Slowly changes an actors direction towards a given point.

- Creatd new actor, batto.  Uses arc_to_target.

- Added 3 additional levels to world.  For a total of 4 fully functional worlds.

- Points needed to beat a stage is now a function of the level that the player is	on in a world.

- Set Moono and Baake to use aitools for spawning and AI behavior.

- Created new actor, Yurei.  Goes to and destorys the nearest powerup.  If no powerups on the screen uses arc_to_target.

- Changed gem_damagex2 so that they add one to the players damage instead of setting it to two then back to one.  This fixed a bug that would cause the gem_damagex2 to end prematurely if you picked up a second gem_damagex2 before the first ran out.

- Individual actor types no longer increase their spawn rate as a factor of time. This method was ineffective at slowly increasing difficulty with the new world class because it was impossible to slowly increase difficulty with spawn rates higher then one second.

- Show session high score at the end of each game.

- Changed the likelyhood of drops based upon actor type.  Moono less likely to drop anything. Robuki now drop items.  reflect gems are now less likely to drop.

- Lengthened the duration of the damage powerup to two seconds.  Shortened the reflect powerup to half a second.

**ITEMS THAT STILL NEED WORK**

- The gem_reflect will still end prematurely if you pick up a second gem before the first one ends.  Not sure on best method to use to fix the problem.

- Rewrite the high score so it isn't a menu item.

- Is the player group needed for anything?


## October 26th, 2006: Joshua
**FINISHED ITEMS**

- Reworked the image loading code. It seems to have sped up the game.

- Improved upon the scene class.

- Bug squashing dealing with vector class.


## October 26th, 2006: Jony
**FINISHED ITEMS**

- Created a world class to handle spawning the actors on the screen.  Includes stages and levels. This allows for smooth increaing of difficulty. World can be created and destoryed dynamically.


## October 22nd, 2006: Joshua
**FINISHED ITEMS**

- Wrote a vector class.

- Implemented vector class in exisiting code.

- Created another dimming function. This one returns an image.

- Wrote the scene class which is used as the background image for the menus.


## October 19th, 2006: Jony
**FINISHED ITEMS**

- Created aitools.py to store all AI functions.

- Created get_nearest function that returns the nearest object of a given group with a given actor_type.

- Created hide function that tells an actor to hide from a given target behind a given object.

- Added spawning and existing AI methods to aitools.py

- Created spawn_off_screen which moves an actor to a random location a given distance from the screen

- Created new enemy type, Rukobi, which hides behind the Baake until the player gets too close at which point they chase after the player.

- Created DEBUG constant that can be set to true to display which functions are being entered in the console.  A call to this function should be made within each function.  (Thanks J-ra!)


## October 19th, 2006: Joshua
**FINISHED ITEMS**

- Rewrote get_nova to use less resources.

- Added a surface/screen dimmer.


## October 2006: Jony
**FINISHED ITEMS**

- Implimented gem_reflect correctly, bullets shot by player have a bound_style reflect and a collide_style reflect.

- Implimented gem_nova.  Creates a ring of stars that are not killed when they strike an enemy, pass through Baake, kill Moono.

- Implimented gem_damagex2.  Doubles the damage the bullets that the player shoot does for one second.

- Streamlined gem dropping code so its easy to tell the percentage chance of something dropping.

- Created an end game 'menu' activated when the player dies.

- Noticed bug in using random.random in if statements. Didn't result in a one in five chance as it should have.  Fixed.


## October 16th, 2006: Joshua
**FINISHED ITEMS**

- Improved upon the Menu class. I kinda went crazy.

- For the most part, all the appropriate menus are in place.

- Moono's now display their value when killed.


## October 14th, 2006: Jony
**FINISHED ITEMS**

- Created font class which allows for easy implimentaion of text on the screen.  Has problem which is noted in font.

- Created gem_500 class to handle gems that give score bonus. Retained gem_reflect for future use with a timer.

- Text appears when gems are picked up

- Spawn rate of Moonos increase as a function of time.

- Set max spawn rate of Moonos.  Once hit sets game to difficulty level 1 where on Baakes also start spawning. Baake spawn rate does not increase with time.

- Made a menu class


## October 13th, 2006: Joshua
**FINISHED ITEMS**

- Scoring implemented.

- Moono's will only appear a certain distance away from the player. This is determined by the spawn() method.

- Overall code cleanup. Also overall code organization/uniformity.

- Implemented hitrects for more accurate collision detection.

- Gems now will flicker and go away after a while.


## October 12th, 2006 Update: Jony
**FINISHED ITEMS**

- Changed gem to gem_reflect so as to allow for other kinds of gems

- Added collision between the bullets and the enemy actors. Each enemy is effected in different ways.

- Added collision between the player and enemy actors.  Each enemy effects the player in different ways.

- Streamlined collision effect code to limit variable passing.

- Added health to the character and enemies

- Added code for a gem_reflect to drop when an enemy character is killed.

**ITEMS THAT STILL NEED WORK**

- Moono's always spawn on the lower half of the screen so as to assure that the player isn't instantly killed by them.  Should be reworked so they can't spawn within x distance of the player.



## October 12th, 2006: Joshua
**FINISHED ITEMS**

- Created enemy classes baake.py and moono.py with simple AI.

- New images for each bad guy type.

- Player's fire function is now time related.

- Locking in framerate works correctly.


## October 12th, 2006: Jony
**FINISHED ITEMS**

- Added collision detection, uses surfaces rect, may want add our own collision function if the inaccuracies are too large.

- When the gem is collided with the gem disappears and all stars on the screens are set to BOUND_STYLE_REFLECT.  Also sets all new stars to be BOUND_STYLE_WRAP.

- Added a new argument when creating a bullet.Bullet, init_bound_style.  This is used to accomplish setting all new stars to a certain BOUND_STYLE.

- Renamed effect_group to bullet_group so as to be more descriptive.  With the changes made to affect the BOUND_STYLE of every element in this group other affects should not be added into this group unless you want these other affects to be modified iin the same way that the bullets are.

- Cleaned up the code:

- Removed the extra call to retrieve the mouses position that was thrown out.  Placed a call to get the mouses position in the game.Game.__init__ function instead.

- removed one temp variable that wasn't needed.

- Made use of actor.Actor.__init__ in the __init__ of its inheritors to set variables that are the same for all/most actors.

- Shortened actor.Actor.__init__ to only include variables that are the same for all/most actors.

**ITEMS STARTED THAT NEED WORK**

- The timer should be used to reset the bullet_group to BOUND_STYLE_KILL after a set duration.


## October 5th, 2006 Update: Joshua
**FINISHED ITEMS**

- Created Actor class that most sprites should inherit from. The player, bullet and gem class in this case.

- Added a player image!  Kuun.png

- Added mouse control.

- Hopefully locked in a frame rate. Thirty fps.

- Created a snippets.py to put code I am not using but don't want to lose.

- Improved upon Jonathan's boundary code. It now has six ways to handle an actor that is "Out Of Bounds."

- Also changed how the player's bounding box is created, which results in more flexiblity.

- Sprites will only rotate and or scale if they have to, unlike the first implementation. Much faster!

- Added the ability to press 'Esc' to exit the program.

- Added the ability to run game in fullscreen mode. Just change the FULLSCREEN value in settings.py to 'True'

**ITEMS STARTED THAT NEED WORK**

- Started working on a Gem class. The player needs something to pickup.

- Collision. I wrote some psudeo-code in the snippets.py file. I think it should be mostly correct, but probably needs fixing before being implemented.

- You cannot set a sprite's scale and rotate it. It will revert back to the original size. I know why this is happening but I am not quite sure of a good solution.


## October 2nd, 2006:  Jony
**FINISHED ITEMS**

- Added a function utility.past_boundry that can check to see if an object is off any side of the screen. Returns a list of all four sides of the screen [right, left, top, bottom] of boolean values.

- Placed object Translation into its own function.

- Added the ability for the player to 'shoot.'  Creates a new star at the players position that then travels at a given velocity until it leaves the screen.  Whereon the Translation function removes it from all lists. The player continues to shoot every so often as long as they continue to press the space bar.  Shooting handled in main game loop, should be moved.  I would think that all of the stars 'shot' by the player should be placed within the Character class.

- Added a new class Character that inherits from the Star class.  Overrided the Translation function so as to allow seperate control of the player star from the stars that are shot.  The player can no longer move off of the screen.

- Added a function utility.scale to allow for the scaling of sprites.  Should be rewritten, removed, or combined with the rotate function.  Causes serious lag issues. Up and Down arrows control scaling.
