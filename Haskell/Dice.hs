module Dice where

import Data.List
import Debug.Trace
import Data.Monoid
import Text.Printf

--the extreme power of haskell makes me strive to write the most compact code possible - other languages don't seem to do this for me
--haskell is very dense, I like that - no wasted space like in C languages
--I feel like I should know how to use monads, and that I should be using them to make this code even simpler than it is already
--perhaps I can now understand the not at all gentle "A Gentle Introduction to Haskell"
--hoogle is really helpful for looking up functions - I wish it was built in to Vim

data Player = Player { name :: String
                     , score :: Int
                     , kind :: PlayerType
                     } deriving (Show)

data PlayerType = HumanPlayer | GreedyAIPlayer | GAPlayer deriving (Show)

main :: IO ()
main = do putStrLn "Purely functional Farkle in Haskell!"
          let players = [Player {name = "David", score = 0, kind = HumanPlayer}
                        ,Player {name = "AI Bob", score = 0, kind = GreedyAIPlayer}
                        ]
          
          return ()


(defn take-turn [player total-scores]
  (loop [turn-score 0
         set-aside []
         remaining (roll-dice 6)]
    (if (is-farkle remaining)
      (do
        (warn-farkle player remaining)
        0)
      (let [new-set-aside (get-validated-set-aside player remaining set-aside turn-score total-scores)
            new-turn-score (+ turn-score (get-score new-set-aside))]
        (if (query-stop player remaining set-aside new-turn-score total-scores)
          new-turn-score
          (recur new-turn-score
                 (concat set-aside new-set-aside)
                 (roll-dice (let [die-count (- (count remaining)
                                               (count new-set-aside))]
                              (if (> die-count 0)
                                die-count
                                6)))))))))

(defn play-farkle [players]
  (if (= (count players) 0)
    (println "Not enough players!")
    (loop [rotation (cycle players)
	   scores (zipmap players (repeat 0))]
      (let [player (first rotation)
	    updated-score (+ (scores player)
                         (take-turn player (take (count players)
                                                 (vec
                                                   (map val scores)))))]
        (if (>= updated-score 10000)
          player
          (recur (rest rotation)
                 (assoc scores player updated-score)))))))

(defn main []
  (let [winner (play-farkle [(HumanPlayer. "David")
                             (GreedyAIPlayer. "Samuel" 800)])]
    (println "The winner is" (str (get-name winner) "!"))))




--queryHumanPlayer :: [Int] -> [Int] -> Int -> Int -> IO String
--queryHumanPlayer remaining set_aside turn_score total_scores = do
--    putStrLn "\n\nScores:\n"
--    --uncurry: convert a two argument function to a one argument function that operates on a pair
--    mapM_ (uncurry $ printf "Player %d: %d\n") (zip [1..] total_scores)
--
--    putStrLn "Turn score: " ++ show turn_score
--    putStrLn "\nSet Aside:"
--    putStrLn $ show set_aside
--
--    putStrLn "\nYou roll the dice:"
--    putStrLn $ show remaining
--    putStrLn "\nIndicate the dice you want to set aside by entering their numbers separated by spaces.\n"
--    choice <- getLine
--    return ()
--
--    --try:
--        --return [int(choice) for choice in choices.split()]
--    --except ValueError:
--        --return ''
--
--parseChoice :: String -> Maybe [Int]
--parseChoice choice =
--    map read $ words choice
    


--query_stop remaining, set_aside, turn_score, total_scores = do
--    choice = raw_input("You have {0} points.  Hit enter to continue rolling, or type 'stop' to end your turn.\n".format(turn_score))
--    if choice == '':
--       return False
--       else:
--       return True
--
--def warn_invalid_set_aside(self):
--    print "That set aside is invalid!"
--
--warnFarkle :: [Int]
--warnFarkle dice =
--    "You got a farkle!\nDice: " + roll.get_values_as_string()



sortByFrequency :: (Ord a, Eq a) => [a] -> [a]
sortByFrequency lst = sortBy moreInList lst
    where moreInList x y = ((numInList y) `compare` (numInList x)) `mappend` (x `compare` y)
          --use the Ord monoid to sort by different criteria; if the first gives an EQ, the second applies
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
findScore :: [Int] -> Int
findScore dice =
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
