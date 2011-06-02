Hello.  My name is David Colgan and I like programming languages.

The reason I like programming languages is because after 5 years at Taylor I have observed an unfortunate fact about computer science:

Programming is HARD.

Like really hard.

Might I suggest that software systems are some of the most complicated things humans have ever created.  

Like, really really hard.  Programmers create some of the most complicated structures humanity has ever attempted.  I had the privilege to work on WordSurv for the past three years, a program that ended up at around 8000 lines of code.  The program is more complicated than anything I have ever finished and yet it pales in comparison to enterprise code bases that have hundreds of thousands of lines or even millions.

That is a lot of complexity!  And it is all abstract, and the different parts have to interact with each other just right or else you get the dreaded software bug!

So what does this have to do with programming languages?  Well, there is this thing called the TIOBE index that keeps track of the most popular programming languages used in industry, and at the top of the list are all the languages everyone knows about because everybody uses them.  And these languages are all mostly the same.  They are procedural or object oriented, and most of them have C-style syntax

Now, since I have become a part of the computer science world, I have heard rumors of languages that are more expressive and powerful than these standard ones that everybody uses.  Languages that promise fewer bugs and fewer lines of code to do the same thing.

So is it true?  This is the question my research sought to answer.  Do these other, lesser-known languages deliver on their claims?

In my time at Taylor I either learned to varying degrees of competence more than 20 different languages.  And I have always thought to myself, yes, some of these languages are better than others.  Why don't we use them more?  But I was never really able to quantify it.  That then is the point of this research project - to do a full-blown analysis of the differences in languages so that we can answer the question are there languages out there that give the programmer more power?

So first we should determine How are we going to compare language power?  Well, has this ever been done in the past?

Yes!

Literature searching revealed two major ways that people have done this sort of programming language survey before: feature comparisons and program comparisons.  Several people compare C and Paschal, Java and Ada, etc.

Feature by feature comparisons usually just say this language has feature X and this language has this instead/also.

Program comparisons I think are more interesting.  Lutz Prechelt did a study where he posted on an online newsgroup a request for people to write the same program in various languages.  He then took all of the programs and got some descriptive statistics, lines of code, execution speed, memory usage, and so on, and then compared the data.

I have taken an approach that combines these two methods.  I have taken five languages and have compared them based on features, and I have also written the same small program in all five.

The program I wrote was a program to play the dice game Farkle.

We want faster development time with fewer lines of code and fewer bugs.

Show stats, this is what I found

Here is why these results are the way that they are




I DEFINE POWER IN A LANGUAGE AS EASE OF PROGRAMMING, TENDENCY TO HAVE BUGS, PROGRAMMER ANGST, 


"Python is a programming language that lets you work more quickly and integrate your systems more effectively. You can learn to use Python and see almost immediate gains in productivity and lower maintenance costs." -python.org

I love languages, sometimes I feel like I am like Tim the Toolman Taylor.  I need POWER in my tools.

Meet the languages, as illustrated in some code to find the average of the elements of a list.

C - the venerable classic - every programmer knows C at least sortof whether they know it or not.  If they know it it because they actually use C, but all kinds modern languages have been influenced by C.

Return type, typed parameters, variable declarations, curly braces to delimit blocks, looping with an interator variable, returning a value with the return statement, and doing a calculation by repeated modification of a variable.

    int find_average(int* arr, int len){
        int i;
        int sum = 0;
        for(i=0; i < len; i++){
            sum += dice[i];
        }
        return sum / count;
    }

Arrays do not know their own size, so you have to keep track of it yourself.  This lead me to that one bug.

C IS LIKE
And as I hope you will come to see, C has the power of an electric drill with a butterknife pinwheel on the end.  



Python - Ah Python, a breath of fresh air in the procedural/object oriented world.  Python is a very readable language, it has concise ways of expressing things, there is less noise in the syntax

No declared types, whitespace is significant, reducing lines with just a }, no iteration variable, eliminates off-by-one errors, arrays manage their own lengths, so you can call len on them to get the size.  You  the programmer could keep track of these things, but programming is hard enough.  I like letting the computer take care of as much as possible for me.  This is programming at a higher level of abstraction.  

    def find_average(lst):
        sum = 0
        for elem in lst:
            sum += elem
        return sum / len(lst)

In some ways I feel like this is the most readable, at least in terms of code describing exactly what it is doing.  You can easily see that we are setting sum to 0, looping over the elements in the list, adding each to sum, and then returning the sum divided by the number of elements.  Not that this is intuitively obvious to everyone, but all programmers will be able to understand it with minimal explanation.  The for/in loop eliminates all off by one errors and eliminates the need for a loop variable.

For these reasons, I feel that Python is a sharp saw.  Coming from the butter knife pinwheel, the difference is obvious.

But wait, I want POWER tools.  I don't want to do the manual labor of setting up loops and managing arrays.  And for that we introduce some new languages that you may never have heard of.


Clojure
    (defn find-average [dice]
      (/ (reduce + 0 dice)
         (count dice)))

Clojure goes one step further and takes out the loop altogether.  Here we call reduce, which is a higher-order function - it takes another function as a parameter!

It has been noticed that there are a couple of loop patterns that are used all over the place, and in languages without higher-order functions this duplication is not able to be factored out.


Type declarations - these are optional, the type system can figure them out for you.

This is really pretty similar to the Clojure code, though Haskell has MANY differences that I will get to in a minute.  Haskell has a lot of safety features that this simple code example can't express, but it really is as different from C and Python as Clojure is.

Haskell
    findAverage :: [Int] -> Int
    findAverage lst = (foldl (+) 0 lst) / (length lst)

Haskell is like a mobile wood chipper mulcher.  It has a lot of safety features so that you can't smack your face with the blade, and you sort of have to prepare the wood before you use the power.


And finally, for something totally backwards, we come to Factor.  Unlike most languages that are read left to right, Factor is written in what you might call reverse polish notation, so things sort of go right to left sortof.

No explicit variables, function have no named parameters, called words because they are just words, code blocks can be passed around, things go on the stack, bi combinator takes two blocks and a single value off the stack and applies the block to both.

Factor
    find-average ( seq -- x )
        [ 0 [ + ] reduce ] [ length / ] bi ;

Factor claims to be able to reduce ALL redundancy.  That is hott, but does it make readability suffer?  This code right here is fairly straightforward, but anything larger than this gets hairy, and not all code is this easy to write.


Now it is cute and all to write a single little function/word thing like this and say LOOKIT one is better than the other.  Is this even a good way of comparing languages?  Well, in order to find a good way to compare languages, I went and read the literature, and turns out this sort of language comparison has been done before.

two kinds - feature comparisons and program comparisons.
get a qualitative view of the language with feature comparisons
get a quantitative view with program comparisons

I took a hybrid approach - feature comparison to get a general idea, and program comparison by writing the same program in each language.

Now, what program to do? One night during a family game night, we busted out farkle, and suddenly the idea came to write a farkle simulator in the five languages.  And so I did.  

Farkle works like this

And so I have a farkle simulator in C, Python, Clojure, Haskell, and Factor.

I would now like to go through and describe some of the OMG moments that I had when using these languages.




Factor is hard to read, maybe lisp is too, but that is because you have not programmed in it before/very much.  I feel like this is sort of the same idea that we have in User interface design.  Just because the interface is not immediately intuitive, if it lets you do work quickly, does it matter if you have to consult a manual first?  The command line is not a pretty or "easy to use" interface per se, but now that I have been using for a lot, it is very powerful.

And this brings up a very important point.  Most of my time this semester was spent learning the languages.  And these functional languages are difficult to learn.  It takes time for the ideas to sink in.  I had tried to learn Haskell about two years prior, and I ultimately gave up for a while because I was overwhelmed by it.  And it was much easier learning it this second time, and I got further in my understanding, but there are still concepts I do not fully understand.  I think I explained monads correctly, but a more important result of the research than what a monad is is that monads are hard to learn.

So I would very much like to continue learning these three new languages.  I am confident that Clojure is a solid language, and I am still holding out that Haskell and Factor are as well, I am just not as good at them.


If I had to program a very large program, I think I might want to most powerful tool, and that might be Factor, unless the power is unweildable, and then maybe I'll do a bit less that is more managable.  Is Factor so powerful that it is harder to use?  I'm not sure, I need more experience.

If I had to program a very large program, I might want to safest tool, and in some ways that would be Haskell, unless of course the safety features get in the way, and I have not done enough Haskell to make that decision yet.

Clojure I feel has the best combination of power and safety without being too much of either of those.  It does not have all of the type system of Haskell, and it does not have the extreme terseness of Factor, but it still managed to have the fewest tokens overall!  And, the bugs I had did not cause too terribly much problems, because of the lack of mutable variables, that was enough.  

If someone came up to me and said "What language should I use for my new project, I would ask them if they are willing to learn a lot or a little.

If willing to learn a little, choose Python, the most powerful language I know that is also the closest to a C-like language.

If you are willing to learn a lot, choose Clojure.  It is the most expressive and simplest of the functional languages I have tried.


        




Here you have to manage the indices of your arrays manually, and that is something you can get used to doing, but it is just one more way that the software can fail.

So the question that I sought to answer was "Should these other languages be considered for new projects in industry?"

My area of interest, you might say, in computer science, is figuring out how we can deliver software in less time with fewer bugs.  

I am always finding new languages that promise less code for the same functionality, with fewer bugs.  I thought that this research project would be an excellent time to investigate these claims.

Paul Graham, one of those famous people in the field, has long thought that fewer lines of code is better because you can't have bugs in code that doesn't exist.  So the fewer lines, the fewer bugs.  So conciseness is power.  Does that hold true?

My findings are that it does to an extent.

Never got around to Java because I was putting it off due to bad experiences with it in the past.  That would be something else to do in the future.

One day we played a game of Farkle as a family game night.  Egads I thought, a perfect system to implement for each language!


# An Investigation of Lesser Known Programming Languages
## Senior Research of David Colgan
## Taylor University


# Background - I like programming languages


# Method - Sitting at the table one night and Farkle!
## Others in the past have done comparisons by writinng the same program in many different languages and comparing
## I wrote the same program of Farkle in 5 different languages


# Meet the languages
## C, Python, Clojure, Haskell, Factor
In order of how likely you are to have heard of them.

## A graph of programmer mood while programming in these.

C - meh
Python - hmm
Clojure - mmmm
Haskell - aaah
Factor - AAAh

Key takeaway: learning a new language is easy, learning a new paradigm is hard.
The functional paradigm is becoming more and more important, and perhaps at Taylor we should teach it earlier and more thoroughly.

Some of these advanced languages 

# Weird and cool things about certain ones:

## Clojure and Haskell are Lazy
* Explanation of laziness


# A comparison of one function in all 5 languages


# An explanation of the new paradigms 


We can trade computer performance for programmer performance


# C

Doesn't really have a logo per se other than the famous KNR book.
C is sort of the classic, default language that everyone sort of knows and influenced everything else.  The C curly bracket and block structure is evident in most mainstream languages.

# Python 
"Python is a programming language that lets you work more quickly and integrate your systems more effectively. You can learn to use Python and see almost immediate gains in productivity and lower maintenance costs."

# Haskell
From the website haskell.org:
"Haskell is an advanced purely-functional programming language. An open-source product of more than twenty years of cutting-edge research, it allows rapid development of robust, concise, correct software. With strong support for integration with other languages, built-in concurrency and parallelism, debuggers, profilers, rich libraries and an active community, Haskell makes it easier to produce flexible, maintainable, high-quality software."

Does Haskell live up to this tall order?



# Factor



Some 30 lines of the Haskell program were 
