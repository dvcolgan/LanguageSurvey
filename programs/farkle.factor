USING: kernel random math sequences prettyprint io formatting
accessors fry locals math.order sorting splitting math.parser
combinators tools.continuations ;
IN: farkle

: rotate ( seq -- seq ) dup first suffix 0 swap remove-nth ;

: roll-dice ( x -- seq ) [ 6 random 1 + ] replicate ;

: count ( elt seq -- cnt ) swap '[ _ = ] filter length ;

:: sort-by-frequency ( arr -- seq )
    arr [ 2dup [ arr count ] bi@ >=<
            dup +eq+ = [ drop <=> ] [ 2nip ] if
        ] sort ;
    
: all-eq? ( seq -- ? ) dup first '[ _ = ] all? ;

: must-have ( seq score block count -- seq score )
    [ over ] 2dip rot length <= swap when ; inline
    

: (score-6) ( seq score -- seq score ) [ over all-eq?
    [ 3000 [ 6 tail ] 2dip ] [ 0 ] if + ] 6 must-have ;

: (score-42) ( seq score -- seq score ) [ over
    [ 4 head all-eq? ] [ 4 tail all-eq? ] bi and
    [ 1500 [ 6 tail ] 2dip ] [ 0 ] if + ] 6 must-have ;

: (score-33) ( seq score -- seq score ) [ over
    [ 3 head all-eq? ] [ 3 tail all-eq? ] bi and
    [ 2500 [ 6 tail ] 2dip ] [ 0 ] if + ] 6 must-have ;

: (score-222) ( seq score -- seq score ) [ over
    [ 2 head all-eq? ] [ 2 4 rot subseq all-eq? ]
    [ 4 tail all-eq? ] tri and and
    [ 1500 [ 6 tail ] 2dip ] [ 0 ] if + ] 6 must-have ;

: (score-straight) ( seq score -- seq score ) [ over
    { 1 2 3 4 5 6 } =
    [ 1500 [ 6 tail ] 2dip ] [ 0 ] if + ] 6 must-have ;

: (score-5) ( seq score -- seq score ) [ over 5 head all-eq?
    [ 2000 [ 5 tail ] 2dip ] [ 0 ] if + ] 5 must-have ;

: (score-4) ( seq score -- seq score ) [ over 4 head all-eq?
    [ 1000 [ 4 tail ] 2dip ] [ 0 ] if + ] 4 must-have ;


: (3s-score) ( seq -- score ) first dup 1 =
    [ drop 300 ] [ 100 * ] if ;

: (score-3) ( seq score -- seq score ) [ over 3 head all-eq?
    [ over (3s-score) [ 3 tail ] 2dip ] [ 0 ] if + ] 3 must-have ;


: (score-1s5s) ( seq score -- seq score ) swap
    [ [ [ 1 = not ] [ 5 = not ] bi and ] filter ]
    [ [ 1 = ] filter length 100 * ] 
    [ [ 5 = ] filter length 50 * ] tri + swap [ + ] dip swap ;


: score-dice ( seq -- leftovers score )
    sort-by-frequency 0 (score-6) (score-42)
    (score-33) (score-222) (score-straight)
    (score-5) (score-4) (score-3) (score-1s5s) ;

: farkle? ( seq -- ? )
    score-dice 0 = nip ;


: string>array ( str -- arr ) " " split [ string>number ] map ;

: array>string ( arr -- str ) [ number>string ] map " " join ;

: (contains-values?) ( container containee -- ? )
    {
        { [ dup length 0 = ] [ 2drop t ] }
        { [ over length 0 = ] [ 2drop f ] }
        { [ 2dup [ first ] bi@ = ] 
            [ [ rest ] bi@ (contains-values?) ] }
        [ [ rest ] dip (contains-values?) ] 
    } cond ;

: contains-values? ( container containee -- ? ) 
    [ [ <=> ] sort ] bi@ (contains-values?) ;


TUPLE: turn-state remaining set-aside turn-score ;
: <turn-state> ( -- turn-state ) 6 roll-dice { } 0 turn-state boa ;

TUPLE: human-player name score win-count ;

: <human-player> ( name -- human-player ) 0 0 human-player boa ;

TUPLE: greedy-ai-player threshold name score win-count ;

: <greedy-ai-player> ( threshold name -- greedy-ai-player )
    0 0 greedy-ai-player boa ;

GENERIC: query-set-aside ( state player -- set-aside )
M: human-player query-set-aside ( state player -- set-aside )
    swap dup remaining>> "You roll the dice:\n" write
    dup array>string write
    "\nIndicate the dice you want to set aside by entering
    their numbers separated by spaces.\n" write
    readln string>array dup score-dice
    0 > [ length 0 = ] dip [ 2dup contains-values? ] 2dip
    and and [ [ 3drop ] dip ] [ 2drop swap query-set-aside ] if ;


M:: greedy-ai-player query-set-aside ( state player -- set-aside )
    ! "AI player rolled " write
    ! state remaining>> array>string write "\n" write
    state remaining>> dup [ score-dice nip 1000 > ] [ length 6 = ] bi and
    [ ]
    [ [ [ 1 = ] [ 5 = ] [ state remaining>> count 3 >= ] tri or or ] filter ] if ;

GENERIC: query-stop ( state player -- ? )
M: human-player query-stop ( state player -- ? )
    swap "You have " write
    turn-score>> number>string write
    " points.  Hit enter to continue rolling, or type 'stop' to
    end your turn.\n" write
    readln "" = [ f ] [ t ] if nip ;

M: greedy-ai-player query-stop ( state player -- ? )
    2dup threshold>> [ turn-score>> ] dip >=
    [ 
    ! "AI player stopped with " write over turn-score>>
    ! number>string write " points.\n" write 
    2drop t ]
    [
    ! "AI player continues.\n" write
    2drop f ] if ;

GENERIC: warn-farkle ( state player -- state player )
M: human-player warn-farkle ( state player -- state player )
    "You got a farkle!\n" write
    "Dice: " write over remaining>> array>string write
    "\n" write ;

M: greedy-ai-player warn-farkle ( state player -- state player )
    ! "AI player got a farkle!\n" write
    ! "Dice: " write over remaining>> array>string write
    ! "\n" write
    ;

: set-aside-dice ( state set-aside -- state )
    [ score-dice nip '[ _ + ] change-turn-score ]
    [ '[ _ append ] change-set-aside ]
    [ '[ length _ length - roll-dice ] change-remaining ]
    2tri 2drop ;

: reset-dice-if-empty ( state -- state )
    dup remaining>> length 0 = [
        [ drop 6 roll-dice ] change-remaining
        [ drop { } ] change-set-aside
    ] when ;

: (take-turn) ( player state -- player state )
    dup remaining>> farkle? [ swap warn-farkle swap ] [
        2dup swap query-set-aside
        set-aside-dice reset-dice-if-empty
        2dup swap query-stop [ ] [ (take-turn) ] if
    ] if ;

: take-turn ( player -- player score ) 
    ! "\n\nYou have " write dup score>> number>string write
    ! " points.\n" write
    <turn-state> (take-turn) turn-score>> ;


: play-farkle ( players -- player ) 
    dup first take-turn '[ _ + ] change-score
    dup score>> 10000 >= [ nip [ 1 + ] change-win-count ]
    [ drop rotate play-farkle ] if ;

: main ( -- )
    "Concatenative Farkle in Factor!" print
    { }
    ! "David" <human-player> suffix ! Ahh duplication - how to remove?
    300 "Greedy Player 300" <greedy-ai-player> suffix
    500 "Greedy Player 500" <greedy-ai-player> suffix
    800 "Greedy Player 800" <greedy-ai-player> suffix
    1000 "Greedy Player 1000" <greedy-ai-player> suffix
    10000 [ dup play-farkle drop [ [ drop 0 ] change-score ] map ] times
    [ [ name>> write " had " write ]
      [ win-count>> number>string write " wins.\n" write ] bi ] each ;
    ! name>> "The winner is %s!\n" printf

MAIN: main
