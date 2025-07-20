# Cursor Bouncy Ball Example

This is the first result I generated with Cursor. I started by asking
it to generate a simple bouncing vector dot ball, like one would see in
a 1990's Amiga demo. I then asked prompts to get it to turn it into
a simple and boring pinball game. I didn't do any code on this, other
thank look through what it generated.

Below are the prompts I used:

- Create a simple python application that opens a window and then has
  a ball boucing around in it. The ball should be a vector dot ball,
  similar to those seen in 1990's Amiga demos, where the ball is a
  series of points. As the ball bounces, the points should spin and
  rotate.
  
- Update the code so that instead of a 2D ball, it looks like a 3D
  ball
  
- Please remove the lines in the ball. It should just be points.

- Now add two more balls to the example. When a ball collides with
  another ball, have the two balls bounce of each other.
  
- Now make each ball a different color. Also, make the size of the
  vector dots slightly smaller.

- Add two pinball like bumpers to the bottom of the screen. They
  should be solid yellow, with one on the left and one on the
  right. When the user presses the space bar, the bumpers will rotate
  for a moment. Whenever a ball collides with a moving bumper, it
  should bounce upwards from it the way it would happen in a pinball
  game.
  
- The bumpers should not change in size. They should just move
  up. Also, the balls should bounce off of them if there is a
  collision, even if the player is not hitting the space bar.
  
- Change the apsect ratio of the window so that it is 3:4 instead of
  4:3.
  
- Instead of two bumpers lets just make one. The bumper should start
  in the center of the screen. It should also be wider and shorted.
  
- Decrease the amount of time that the bumper stays up when the user
  presses space. It should just move up and then come back down
  without pausing at the top.
  
- Lets make it so that the bumper can also be controlled by the
  mouse. The bumper should move left or right when the mouse moves
  left or right. When the user clicks the left mouse button, the
  bumper should activate just like the space bar.
  
- Can you hide the mouse when the window is active?

- The balls are srill passing through the bumper sometimes. Can you
  make it so they always bounce away from the bumper whenever they hit
  it?
  
- Can you make the bumper a rounded rectangle instead of a rectangle?

- Can you allow the left and right arrow keyboard keys to also control
  the bumper?
  
- Update the keyboard controls so that when the user holds down the
  left and right arrow keys, the bumper continues to move left and
  right
  
- Lets make this more of a game. Draw a solid line with a hole in it
  at the bottom of the screen. If the ball goes through the hole, the
  ball should disappear off the screen. The bumper should be abovoe
  this line. The player should try to stop the ball from going in the
  hole.
  
- Error: inserted stack trace - found there was an init before it was
  defined
  
- Make the balls smaller. Also add more balls. When all the balls have
  disappeared through the hole, add a flashing "GAME OVER" message for
  5 seconds'
  
- Also make the balls bounce off the bottom line as well

- After flashing the game over message, ask "Shall we play again?"  If
  the user types y, then start a new game. Otherwise exit.
  
- Move the bottom line up a little. The balls should be visible as
  they pass through the hole.
  
- Can you change the bottom line so it has two holes instead of one

- Can you add a score for every time you  block a ball from going into
  the hole and display it in the corner
