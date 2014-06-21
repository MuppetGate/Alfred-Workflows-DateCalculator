## Date Calculator
Hello there!
I needed a bit of motivation to learn Python and Alfred workflows, so I thought I’d kill two horses with one bullet, so to speak.
Right, so this is a date calculator – kind of. It won’t tell you when you will the lottery, or how long you’ve got to hide your ‘arty videos’ before  your wife gets home, but it will answer one or two _very simple_ questions about dates.

For example, if you enter

**dcalc 25.12.14 - 18.01.14**

then it will tell you the number of days between those dates:

You could also try

**dcalc 25.12.14 - now**

for the number of days until Chrismas. (Always seems so far away . . .)

Maybe you don’t want it in days, but would rather it in weeks:

**dcalc 25.12.14 - now w**

or days and weeks

**dcalc 25.12.14 - now wd**

or years, months, weeks and days

**dcalc 25.12.14 - now ymwd**

or

**dcalc 25.12.14 - now long**

will do the same thing. Personally, I always use the _long_ format because it’s more accurate.

For those who like to look ahead, you can add days to a date

**dcalc now + 6d**

or weeks

**dcalc 18.12.14 + 9w**

or combine ‘em

**dcalc 18.12.12 + 5y 9d 3w**

If you want to know what week number you’re in, then try this:

**dcalc ^today**

Or for a specific date:

**dcalc ^25.12.14**

You can also use the _today_ thing in other places too:

**dcalc today + 4d**

And we have another thing called _now_ because the workflow can handle times too:

**dcalc now + 6h 8M**

will add 6 hours and 8 minutes to the current time. Note the capital ‘M’ to denote minutes. Odd, I know . . .  sorry, but the workflow has to distinguish between this and a small ‘m’ (for months). I figured make this one a capital because it would see much less use. (It has for me.)

**dcalc 14:35 + 6h**

That’s the time 6 hours from now, and for real nerdiness:

**dcalc 21.06.14@14:20 - 23.01.12@09:21 long**

That about covers it, I think. I haven’t done anything clever with locales, but you can pick a different date format with

**dcalc settings**

If you’re ever puzzled by _invalid command_ or _invalid expression_ errors, then start with the settings; they might be set incorrectly.

### Credits
A list of things that made my first attempt at Python programming possible:
- Dean Jackson for his more-than-slightly awesome [Alfred Workflow framework](https://github.com/deanishe/alfred-workflow). 
- The folk at [Jetbrains](http://www.jetbrains.com), for making programming, in any language, bearable.
- Paul McGuire, for writing [PyParsing](http://pyparsing.wikispaces.com).
- Gustavo Niemeyer for [Python-DateUtil](https://labix.org/python-dateutil)
- And finally, and by no means least – Mr Smirnoff for discovering how to bottle patience.

### License
Well, I guess the [MIT](http://opensource.org/licenses/MIT) one will do. :-)

The MIT License (MIT)
Copyright (c) 2014 MuppetGate Media

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


