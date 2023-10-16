MAGiE: Your MAGnetic interactive Explorer
=================================================
Python Version
-------------------------------------------------

# Long story short
This is a binary-encoding puzzle game implemented as a Python console application.

I fully intend to release this as **free** software, but I haven't figured out the details, like settling on a license.
If all you want to do is play the game and tinker with the code, then please, be my guest.
But for now I, Nate Grigg, retain the copyright: all rights reserved.
Please contact me for any use cases which fall outside of "tinkering with" and "playing" the game.

# To Play
If you just run console_magie.py with a recent(ish) release of Python 3 it should work.
There's nothing very exotic going on.

The only way to quit right now is to CTRL-C out.
(I don't know how that works with Python on Windows, I've done practically zero Python in Windows.)

I have "add a back option to the menus" on my [TODO list](project.org)

## Narrow output
A lot of the lines of text are constrained to 13 characters.
This reflects the stylistic choices from the Mobile/Unity versions of the game.

It had a very retro asthetic, with an LCD-screen motif.
My designer buddy had created a nice-looking, chunky pixel font for us.
That, plus the retro-ness of it kept the text display narrow.

So if you feel cramped, it may help if you imagine yourself as
a 10 year old who's family apartment and school are both attached to a rad, retro-future, 80's shopping mall.

# Long story long(er)
I originally implemented this game in the Unity 3D game engine
and made it available in the Apple App Store and the Google Play Store.

I stopped paying my Apple Developer Dues, so they de-listed the game.
And I can't seem to find it in the Google Play Store, but I believe it's there.

Anyway - there is probably a large overlap between
(a) people who will enjoy this game and
(b) people who use Raspberry Pi and Linux. 
So I set out to create a version of the game that runs in Python.

The Unity/Mobile game was very interactive. And my initial goal was to duplicate the same experience here.
I thought Curses looked like a good way to provide that immediate interaction.
And as I started learning curses and implementing the game in it, I was proven right:
Curses did turn out to be a great way to get a very responsive game with a rich text user interface.

But it was very hard to debug as the implementation got more complex.

So, you will see references to Curses (and maybe even a bit of working code),
but the active development right now is in the plain "console" version of the game.

(Where you have to press [enter] every time you want to submit a guess 😩)

# Python compatibility
I've been developing against fairly recent releases of Python 3. (I believe I have used v3.9 and v3.10 quite a bit.)
I have also played it a bit in Pythonista on my iPhone, which I believe is Python 3.6.
If you find any compatibility issues or bugs, don't hesitate to let me know.
Perhaps we could even use this nifty "Issues" feature of GitHub.
