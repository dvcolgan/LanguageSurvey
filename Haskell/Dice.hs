module Dice where

import Data.List
import Debug.Trace
import Data.Monoid

--data Die = One | Two | Three | Four | Five | Six
--data Score = SixOfAKind | FiveOfAKind | FourOfAKind | ThreeOnes | ThreeTwos | ThreeThrees
--type Roll = [Int]

sortByFrequency :: (Ord a, Eq a) => [a] -> [a]
sortByFrequency lst = sortBy moreInList lst
    where moreInList x y = ((numInList y) `compare` (numInList x)) `mappend` (x `compare` y)  --use the Ord monoid to sort by different criteria; if the first gives an EQ, the second applies
          numInList e = length $ filter (== e) lst



--broken - fails for the test case mostCommonElement [1,2,3,2,5], returns (1,5)
--mostCommonElement ::  [Int] -> (Int, Int)
--mostCommonElement lst = foldl majorityVote (0, head lst) lst
--    where majorityVote :: (Int, Int) -> Int -> (Int, Int)
--          majorityVote (cnt, val) x =
--              let newCnt = if val == x then cnt+1 else cnt-1
--              in if newCnt == 0 then trace (show (1, x)) (1, x) else trace (show (newCnt, val)) (newCnt, val)

--not sure if I could use a monad here?  Chaining score and remaining dice filtering functions
              --
score :: [Int] -> Int
score dice =
    fst $ remove1s5s . (removeNOfAKind 3) . (removeNOfAKind 4) . (removeNOfAKind 5) . remove222 . remove33 . remove42 . removeStraight . (removeNOfAKind 6) $ (0, sortByFrequency dice) 

-- Expects the dice to be sorted by frequency

remove42 :: (Int, [Int]) -> (Int, [Int])
remove42 (score, dice)
    | length dice /= 6 = (score, dice)
    | all (== head first4) first4 && all (== head last2) last2 = (score + 1500, [])
    | otherwise = (score, dice)
    where (first4, last2) = splitAt 4 dice

remove33 :: (Int, [Int]) -> (Int, [Int])
remove33 (score, dice)
    | length dice /= 6 = (score, dice)
    | all (== head first3) first3 && all (== head last3) last3 = (score + 2500, [])
    | otherwise = (score, dice)
    where (first3, last3) = splitAt 3 dice

remove222 :: (Int, [Int]) -> (Int, [Int])
remove222 (score, dice)
    | length dice /= 6 = (score, dice)
    | all (== head first2) first2 && all (== head mid2) mid2 && all (== head last2) last2 = (score + 2500, [])
    | otherwise = (score, dice)
    where (first2, rest) = splitAt 2 dice
          (mid2, last2) = splitAt 2 rest

remove1s5s :: (Int, [Int]) -> (Int, [Int])
remove1s5s (score, dice) =
    let (onesAndFives, rest) = partition (\x -> x == 1 || x == 5) dice
        valOf1s5s = sum $ map getScore onesAndFives
    in (score + valOf1s5s, rest)
    where getScore 1 = 100
          getScore 5 = 50

removeStraight :: (Int, [Int]) -> (Int, [Int])
removeStraight (score, dice)
    | sort dice == [1,2,3,4,5,6] = (score + 1500, [])
    | otherwise = (score, dice)

removeNOfAKind :: Int -> (Int, [Int]) -> (Int, [Int])
removeNOfAKind n (score, dice)
    | length dice < n = (score, dice)
    | all (== head dice) firstN = (score + scoreNOfAKind firstN, drop n dice)
    | otherwise = (score, dice)
    where firstN = take n dice
          scoreNOfAKind dice =
              case length dice of 
                   6 -> 3000
                   5 -> 2000
                   4 -> 1000
                   3 -> if head dice == 1 then 300 else (head dice) * 100
                   otherwise -> error "Should not try to take another n of a kind"


    



--          score6 (score, (x:xs)) = all
--removeSixOfAKind :: (Int, [Int]) -> (Int, [Int])
--removeSixOfAKind (score, dice)
----    | all (== (head dice)) dice = (score + 3000, [])
--removeFiveOfAKind :: [Int] -> Bool
--removeFourOfAKind :: [Int] -> Bool
--removeThreeOfAKind :: [Int] -> Bool
--haveSixOfAKind :: [Int] -> Bool
--haveSixOfAKind :: [Int] -> Bool
--haveSixOfAKind :: [Int] -> Bool
--haveSixOfAKind :: [Int] -> Bool
--haveSixOfAKind :: [Int] -> Bool
