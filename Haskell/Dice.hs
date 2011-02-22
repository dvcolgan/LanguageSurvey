module Dice where

import Data.List

--data Die = One | Two | Three | Four | Five | Six
--data Score = SixOfAKind | FiveOfAKind | FourOfAKind | ThreeOnes | ThreeTwos | ThreeThrees
--type Roll = [Int]

--sortByFrequency lst = sortBy (

--broken - fails for the test case mostCommonElement [1,2,3,2,5], returns (1,5)
mostCommonElement :: (Eq a) => [a] -> (Int, a)
mostCommonElement lst = foldl' majorityVote (0, head lst) lst
    where majorityVote (cnt, val) x =
              let newCnt = if val == x then cnt+1 else cnt-1
              in if newCnt == 0 then (1, x) else (newCnt, val)

--not sure if I could use a monad here?  Chaining score and remaining dice filtering functions
--removeSixOfAKind :: (Int, [Int]) -> (Int, [Int])
--removeSixOfAKind (score, dice)
--    | all (== (head dice)) dice = (score + 3000, [])
--haveFiveOfAKind :: [Int] -> Bool
--haveFourOfAKind :: [Int] -> Bool
--haveThreeOfAKind :: [Int] -> Bool
--haveSixOfAKind :: [Int] -> Bool
--haveSixOfAKind :: [Int] -> Bool
--haveSixOfAKind :: [Int] -> Bool
--haveSixOfAKind :: [Int] -> Bool
--haveSixOfAKind :: [Int] -> Bool
