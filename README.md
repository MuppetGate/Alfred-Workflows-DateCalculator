## Date Calculator
Hello there!
I needed a bit of motivation to learn Python and Alfred workflows, so I thought I’d kill two horses with one bullet, so to speak.
Right, so this is a date calculator – kind of. It won’t tell you when you will the lottery, or how long you’ve got to hide your ‘arty videos’ before  your wife gets home, but it will answer one or two _very simple_ questions about dates.

![](http://www.packal.org/sites/default/files/public/workflow-files/muppetgatenetdatecalculator/screenshots/screenshot2014-06-21at084104.png)

For example, if you enter

**dcalc 25.12.14 - 18.01.14**

then it will tell you the number of days between those dates. Note that the workflow parses the command as you enter it, so you’ll see _invalid command_, _invalid expression_ and _invalid format_ errors as you type. Once you’ve completed the command then you’ll be given the result.

You could also try

**dcalc 25.12.14 - now**

for the number of days until Christmas. (Always seems so far away . . .)

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

**dcalc 18.12.12 + 5y 9d 3w - 2d + 1d 1w**

What does that mess do?
- Take the date 18.12.12 
- Add 5 years
- Add another 9 days
- Add another 3 weeks
- Then take off 2 days
- Add another 1 day
- And then add another 1 week

If you want to know what week number you’re in, then try this:

**dcalc ! today**

Or for a specific date:

**dcalc ! 25.12.14**

You can also use the _today_ thing in other places too:

**dcalc today + 4d**

And we have another thing called _time_ because the workflow can handle times too:

**dcalc time + 6h 8M**

will add 6 hours and 8 minutes to the current time. Note the capital ‘M’ to denote minutes. Odd, I know . . .  sorry, but the workflow has to distinguish between this and a small ‘m’ (for months). I figured make this one a capital because it would see much less use. (It has for me.)

If you just want the current time, then just enter

**dcalc time**

Here’s another time calculation
**dcalc 14:35 + 6h**

That’s the time 6 hours from now, and for real nerdiness:

**dcalc 21.06.14@14:20 - 23.01.12@09:21 long**

Probably not all that useful, but some of this other stuff might be. You know all about

**dcalc now**

For giving you the current time and date. Well you can use 

**dcalc tomorrow**

for tomorrow’s date, and as you would expect

**dcalc tomorrow + 1d**

will give you the day after tomorrow.

**dcalc next tue**

will give you the date next Tuesday. Or for for Thursday you could enter

**dcalc next tue + 2d**

if you’re still a little too inebriated to realise that

**dcalc thu**

will give you the same answer.

That about covers it, I think. I haven’t done anything clever with locales, but you can pick a different date format with

**dcalc settings**

If you’re ever puzzled by _invalid command_ or _invalid expression_ errors, then start with the settings; they might be set incorrectly.

Oh, almost forgot.

**dcalc easter**

Is the date for next Easter Sunday, for no other reason that I can never remember it, and now there’s an easy way to find out how many days until Christmas:

**dcalc today - christmas**

## Exclusions
Added at the request of a friend, though I'm not sure there's a lot of call for it. Okay, say you need to know how long you have to complete a project:

**dcalc today - christmas**

Not a problem, but hang on a mo – you don't like to work on weekends, so you'd better exclude them:

**dcalc today - christmas exclude weekends**

That'll exclude weekends from the calculations. Fantastic! But hang on, the wife's birthday! You won't be working on that day if you know what's good for you:

**dcalc today - christmas exclude weekends 26.09.2014**

Nicely saved, my friend; but there is still that small break you were planning in October:

**dcalc today - christmas exclude weekends 26.09.2014 05.10.2014 to 10.10.2014**

Crap! You're also having a wisdom tooth removed next wednesday

**dcalc today - christmas exclude weekends 26.09.2014 05.10.2014 to 10.10.2014 next wed**

Though I think you'll need more than a day to get over that.

### Credits
A list of things that made my first attempt at Python programming possible:
- Dean Jackson for his more-than-slightly awesome [Alfred Workflow framework](#), and for his ‘parse-as-you-type’ idea.
- The folk at [Jetbrains](#), for making programming, in any language, bearable.
- Peter Odding for writing [HumanFriendly](#).
- Gustavo Niemeyer for [Python-DateUtil](#).
- Volker Birk for [PyPEG](#).
- And finally, and by no means least – Mr Smirnoff for discovering how to bottle patience.

### Version History
Latest release (Version 1.6). Refactoring. Added exclusion functionality, and macros for **year\_start** and **year\_end**. Changed the calls for days of the week: You now need to enter **next mon** to get the date for next Monday, but you can also now type **prev mon** to get the date for last Monday. Huzzah!

Latest release (Version 1.5). Refactoring. Rewrote the code for date subtraction arithmetic. 
Now it’s a lot more accurate, even when working with uneven months and weeks. Minor bug fixes.

Last release (Version 1.4) Fixed bug that caused inaccuracies when calculating anniversaries. 
Refactored code to make it easier to add new date functions and date formatters. General tidy-up

Last release (Version 1.3) Adds extra formatting functions (day of week) and bug fixes.

Last release (Version 1.2) was an improvement to add user-defined macros.

Last release (Version 1.1) was on the 01.07.2014. This included a new anniversary list function, 
and the addition of the international date format (yyyy-mm-dd).

Last release (Version 1.0) was on the 27.06.2014. This included an improved date parser, 
added macros (days of week, christmas and easter) and a general tidy up. 
The symbol for getting the week number for a particular date has changed 
from ‘^’ to ‘!’ or ‘wn’. Why? Because I seemed to be struggling to find ‘^’ on the keyboard.

### License
Well, I guess the [MIT](#) one will do. :-)

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
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


