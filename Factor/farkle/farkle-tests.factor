! Copyright (C) 2011 Your name.
! See http://factorcode.org/license.txt for BSD license.
USING: tools.test farkle ;
IN: farkle.tests

[ { 1 1 1 2 3 4 } ] [ { 1 2 1 3 1 4 } sort-by-frequency ] unit-test
[ { 4 4 4 1 1 2 } ] [ { 1 2 1 4 4 4 } sort-by-frequency ] unit-test
[ { 4 4 4 4 4 2 } ] [ { 4 2 4 4 4 4 } sort-by-frequency ] unit-test

[ t ] [ { 1 1 1 1 } all-eq? ] unit-test
[ f ] [ { 1 2 2 1 } all-eq? ] unit-test

[ { } 3000 ] [ { 1 1 1 1 1 1 } 0 (score-6) ] unit-test
[ { 1 2 3 4 5 6 } 0 ]    [ { 1 2 3 4 5 6 } 0 (score-6) ] unit-test

[ { } 1500 ] [ { 4 4 4 4 2 2 } 0 (score-42) ] unit-test
[ { } 1500 ] [ { 3 3 3 3 5 5 } 0 (score-42) ] unit-test
[ { 3 3 3 2 2 5 } 0 ]    [ { 3 3 3 2 2 5 } 0 (score-42) ] unit-test

[ { } 2500 ] [ { 4 4 4 2 2 2 } 0 (score-33) ] unit-test
[ { } 2500 ] [ { 3 3 3 5 5 5 } 0 (score-33) ] unit-test
[ { 3 3 3 2 2 5 } 0 ]    [ { 3 3 3 2 2 5 } 0 (score-33) ] unit-test

[ { } 1500 ] [ { 4 4 2 2 3 3 } 0 (score-222) ] unit-test
[ { } 1500 ] [ { 3 3 5 5 1 1 } 0 (score-222) ] unit-test
[ { 3 3 3 2 2 5 } 0 ]    [ { 3 3 3 2 2 5 } 0 (score-222) ] unit-test

[ { } 1500 ] [ { 1 2 3 4 5 6 } 0 (score-straight) ] unit-test
[ { 1 1 2 2 3 3 } 0 ]    [ { 1 1 2 2 3 3 } 0 (score-straight) ] unit-test

[ { } 2000 ] [ { 1 1 1 1 1 } 0 (score-5) ] unit-test
[ { 1 2 4 5 6 } 0 ]    [ { 1 2 4 5 6 } 0 (score-5) ] unit-test

[ { } 1000 ] [ { 1 1 1 1 } 0 (score-4) ] unit-test
[ { 1 4 5 6 } 0 ]    [ { 1 4 5 6 } 0 (score-4) ] unit-test

[ { } 300 ] [ { 1 1 1 } 0 (score-3) ] unit-test
[ { } 200 ] [ { 2 2 2 } 0 (score-3) ] unit-test
[ { } 300 ] [ { 3 3 3 } 0 (score-3) ] unit-test
[ { } 400 ] [ { 4 4 4 } 0 (score-3) ] unit-test
[ { } 500 ] [ { 5 5 5 } 0 (score-3) ] unit-test
[ { } 600 ] [ { 6 6 6 } 0 (score-3) ] unit-test
[ { 1 4 5 } 0 ]   [ { 1 4 5 } 0 (score-3) ] unit-test

[ { 4 2 } 300 ] [ { 1 1 5 5 4 2 } 0 (score-1s5s) ] unit-test
[ { 3 4 2 } 100 ] [ { 3 5 5 4 2 } 0 (score-1s5s) ] unit-test
[ { 3 4 2 } 200 ] [ { 3 1 4 1 2 } 0 (score-1s5s) ] unit-test

[ { } 100 ] [ { 1 } score-dice ] unit-test
[ { } 50 ] [ { 5 } score-dice ] unit-test
[ { 2 } 0 ] [ { 2 } score-dice ] unit-test
[ { 3 } 0 ] [ { 3 } score-dice ] unit-test
[ { 4 } 0 ] [ { 4 } score-dice ] unit-test
[ { 6 } 0 ] [ { 6 } score-dice ] unit-test
[ { } 150 ] [ { 1 5 } score-dice ] unit-test
[ { } 200 ] [ { 1 1 } score-dice ] unit-test
[ { } 100 ] [ { 5 5 } score-dice ] unit-test
[ { 2 3 } 0 ] [ { 2 3 } score-dice ] unit-test
[ { 4 6 } 0 ] [ { 4 6 } score-dice ] unit-test
[ { } 300 ] [ { 1 1 1 } score-dice ] unit-test
[ { } 200 ] [ { 2 2 2 } score-dice ] unit-test
[ { } 300 ] [ { 3 3 3 } score-dice ] unit-test
[ { } 400 ] [ { 4 4 4 } score-dice ] unit-test
[ { } 500 ] [ { 5 5 5 } score-dice ] unit-test
[ { } 600 ] [ { 6 6 6 } score-dice ] unit-test
[ { 2 3 4 } 0 ] [ { 2 3 4 } score-dice ] unit-test
[ { 6 } 150 ] [ { 1 5 6 } score-dice ] unit-test
[ { 3 6 } 50 ] [ { 3 5 6 } score-dice ] unit-test
[ { } 1000 ] [ { 1 1 1 1 } score-dice ] unit-test
[ { } 1000 ] [ { 2 2 2 2 } score-dice ] unit-test
[ { } 1000 ] [ { 3 3 3 3 } score-dice ] unit-test
[ { } 1000 ] [ { 4 4 4 4 } score-dice ] unit-test
[ { } 1000 ] [ { 5 5 5 5 } score-dice ] unit-test
[ { } 1000 ] [ { 6 6 6 6 } score-dice ] unit-test
[ { } 700 ] [ { 6 6 6 1 } score-dice ] unit-test
[ { } 450 ] [ { 4 4 4 5 } score-dice ] unit-test
[ { 4 } 300 ] [ { 3 3 3 4 } score-dice ] unit-test
[ { 2 3 4 } 100 ] [ { 1 2 3 4 } score-dice ] unit-test
[ { 3 4 6 } 50 ] [ { 3 4 5 6 } score-dice ] unit-test
[ { 2 3 4 6 } 0 ] [ { 2 3 4 6 } score-dice ] unit-test
[ { } 2000 ] [ { 1 1 1 1 1 } score-dice ] unit-test
[ { } 2000 ] [ { 2 2 2 2 2 } score-dice ] unit-test
[ { } 2000 ] [ { 3 3 3 3 3 } score-dice ] unit-test
[ { } 2000 ] [ { 4 4 4 4 4 } score-dice ] unit-test
[ { } 2000 ] [ { 5 5 5 5 5 } score-dice ] unit-test
[ { } 2000 ] [ { 6 6 6 6 6 } score-dice ] unit-test
[ { } 3000 ] [ { 1 1 1 1 1 1 } score-dice ] unit-test
[ { } 3000 ] [ { 2 2 2 2 2 2 } score-dice ] unit-test
[ { } 3000 ] [ { 3 3 3 3 3 3 } score-dice ] unit-test
[ { } 3000 ] [ { 4 4 4 4 4 4 } score-dice ] unit-test
[ { } 3000 ] [ { 5 5 5 5 5 5 } score-dice ] unit-test
[ { } 3000 ] [ { 6 6 6 6 6 6 } score-dice ] unit-test
[ { } 2500 ] [ { 1 1 1 2 2 2 } score-dice ] unit-test
[ { } 2500 ] [ { 3 3 3 4 4 4 } score-dice ] unit-test
[ { } 2500 ] [ { 5 5 5 6 6 6 } score-dice ] unit-test
[ { } 1500 ] [ { 1 1 2 2 3 3 } score-dice ] unit-test
[ { } 1500 ] [ { 4 4 5 5 6 6 } score-dice ] unit-test
[ { } 1500 ] [ { 1 1 1 1 2 2 } score-dice ] unit-test
[ { } 1500 ] [ { 3 3 3 3 4 4 } score-dice ] unit-test
[ { } 1500 ] [ { 5 5 5 5 6 6 } score-dice ] unit-test

[ t ] [ { 1 2 3 4 } { 1 2 3 } contains-values? ] unit-test
[ t ] [ { 3 2 1 4 } { 1 2 3 } contains-values? ] unit-test
[ t ] [ { 3 1 3 3 } { 3 1 3 } contains-values? ] unit-test
[ t ] [ { 4 4 4 4 } { 4 4 4 4 } contains-values? ] unit-test
[ f ] [ { 1 4 } { 1 2 3 } contains-values? ] unit-test
[ f ] [ { 1 } { 1 2 3 } contains-values? ] unit-test
[ f ] [ { } { 1 2 3 } contains-values? ] unit-test
[ t ] [ { 1 } { } contains-values? ] unit-test
