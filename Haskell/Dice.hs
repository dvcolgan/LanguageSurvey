module Dice where

import Data.List
import Debug.Trace
import Data.Monoid
import Text.Printf
import System.Random


type Individual = [

class GAProblem a where
    createRandomIndividual :: IO Individual
    runTournament :: Individual -> Individual -> Individual
    mateIndividuals :: Individual -> Individual -> (Individual, Individual)
    mutateIndividual :: Individual -> Individual

instance GAProblem Sequence where
    createRandomIndividual = sequence $ replicate 10 $ getStdRandom $ randomR (0,9)
    runTournament individual1 individual2 =
        where evaluate individual = zip individual

              --WORKING HERE '#!^#%$*^%&($*&&#F%YIPUXQINTG<IPA

  (run-tournament [this individual1 individual2]
    (letfn [(evaluate-fn [individual] (reduce + (map #(if (= %1 %2) 1 0)
                                                     individual
                                                     (range 10))))]
      (if (> (evaluate-fn individual1)
	     (evaluate-fn individual2))
	individual1
	individual2)))

  (mate-individuals [this individual1 individual2]
    (let [pivot (rand-int 10)
	  [fst-front fst-back] (split-at pivot individual1)
	  [snd-front snd-back] (split-at pivot individual2)]
      [(vec (concat fst-front snd-back))
       (vec (concat snd-front fst-back))]))

  (mutate-individual [this individual]
    (let [pivot (rand-int 10)]
      (assoc individual pivot (rand-int 10))))
  )

data Player = Player { name :: String
                     , score :: Int
                     , kind :: PlayerType
                     } deriving (Show)

--maybe this should be in the state monad eh?
data TurnState = TurnState { remaining :: [Int]
                           , setAside :: [Int]
                           , turnScore :: Int }

data PlayerType = HumanPlayer | GreedyAIPlayer | GAPlayer deriving (Show)

main :: IO ()
main = do putStrLn "Purely functional Farkle in Haskell!"
          --are the players something that could use the state monad?
          let players = [Player {name = "David", score = 0, kind = HumanPlayer}
                        ,Player {name = "AI Bob", score = 0, kind = GreedyAIPlayer}
                        ]

          winner <- playFarkle players
          putStrLn $ "The winner is " ++ name winner ++ "!"


playFarkle :: [Player] -> IO Player
playFarkle players@(curPlayer:otherPlayers) = do
    newCurPlayer <- takeTurn curPlayer (getScores players)
    if score newCurPlayer >= 10000
       then return newCurPlayer
       else do
           playFarkle $ otherPlayers ++ [newCurPlayer]

getScores :: [Player] -> [Int]
getScores players =
    map score players


--It would appear that the game structure, being very procedural in nature, does not benefit from a purely functional model
takeTurn :: Player -> [Int] -> IO Player
takeTurn player totalScores = do
    initialDice <- rollDice [0,0,0,0,0,0]
    turnLoop TurnState {remaining = initialDice, setAside = [], turnScore = 0} 
    where turnLoop turnState
            | isFarkle $ remaining turnState = do
                warnFarkle (kind player) (remaining turnState)
                return player
            | otherwise = do
                newSetAside <- querySetAside (kind player) turnState totalScores
                newRoll <- rollDice
                            (if length (setAside turnState) + length newSetAside == 6
                                then [0,0,0,0,0,0]
                                else removeElems newSetAside (remaining turnState))
                let newTurnState =
                        TurnState { remaining = newRoll
                                  , setAside = (if length newRoll == 6 then [] else setAside turnState ++ newSetAside)
                                  , turnScore = turnScore turnState + fst (findScore newSetAside) }
                choice <- queryStop (kind player) newTurnState totalScores
                if choice == True
                   then do return $ player { score = score player + turnScore newTurnState }
                   else do turnLoop newTurnState


removeElems :: (Eq a) => [a] -> [a] -> [a]
removeElems [] lst = lst
removeElems (x:xs) lst = removeElems xs (delete x lst)


rollDice :: [Int] -> IO [Int]
rollDice dice = do
    newDice <- sequence $ replicate (length dice) $ getStdRandom $ randomR (1,6)
    return newDice

isFarkle :: [Int] -> Bool
isFarkle dice = fst (findScore dice) == 0

querySetAside :: PlayerType -> TurnState -> [Int] -> IO [Int]
querySetAside HumanPlayer turnState totalScores = do
    putStrLn "\n\nScores:\n"
    --uncurry: convert a two argument function to a one argument function that operates on a pair
    mapM_ (uncurry $ printf "Player %d: %d\n") ((zip ([1..] :: [Int]) totalScores))

    putStrLn $ "Turn score: " ++ show (turnScore turnState)
    putStrLn "\nSet Aside:"
    putStrLn $ show $ setAside turnState

    putStrLn "\nYou roll the dice:"
    putStrLn $ show $ remaining turnState
    putStrLn "\nIndicate the dice you want to set aside by entering their numbers separated by spaces.\n"
    choice <- getLine
    let setAside = map read (words choice)
    if (length setAside > 0) && containsValues setAside (remaining turnState) && length (snd (findScore setAside)) == 0
       then return setAside
       else do
           putStrLn "That set aside is not valid!"
           querySetAside HumanPlayer turnState totalScores

querySetAside GreedyAIPlayer turnState totalScores = do
    putStrLn $ "AI player rolled" ++ show (remaining turnState)
    if length (remaining turnState) == 6 && fst (findScore (remaining turnState)) > 1000
       then return $ remaining turnState
       else do
           let newSetAside = filter isScoringDie (remaining turnState)
           putStrLn $ "AI player set aside" ++ show newSetAside
           return newSetAside
    where isScoringDie die =
              die == 1 || die == 5 || (length (filter (== die) (remaining turnState)) == 3)


containsValues :: (Eq a, Ord a) => [a] -> [a] -> Bool
containsValues firstVals secondVals =
    containsValues' (sort firstVals) (sort secondVals)
    where containsValues' [] _ = True
          containsValues' _ [] = False
          containsValues' (x:xs) (y:ys)
            | x == y = containsValues' xs ys
            | otherwise = containsValues' (x:xs) ys

    
queryStop :: PlayerType -> TurnState -> [Int] -> IO Bool
queryStop HumanPlayer turnState totalScores = do
    putStrLn $ "You have " ++ (show $ turnScore turnState) ++ ".  Hit enter to continue rolling, or type 'stop' to end your turn.\n"
    choice <- getLine
    if choice == "" then do return False else do return True

queryStop GreedyAIPlayer turnState totalScores = do
    return $ turnScore turnState > 700


warnFarkle :: PlayerType -> [Int] -> IO ()
warnFarkle HumanPlayer dice = do
    putStrLn $ "You got a farkle!\nDice: " ++ show dice

warnFarkle GreedyAIPlayer dice = do
    putStrLn $ "AI player got a farkle!\nDice: " ++ show dice

sortByFrequency :: (Ord a, Eq a) => [a] -> [a]
sortByFrequency lst = sortBy moreInList lst
    where moreInList x y = ((numInList y) `compare` (numInList x)) `mappend` (x `compare` y)
          --use the Ord monoid to sort by different criteria; if the first gives an EQ, the second applies
          numInList e = length $ filter (== e) lst


--not sure if I could use a monad here?  Chaining score and remaining dice filtering functions
findScore :: [Int] -> (Int, [Int])
findScore dice =
    remove1s5s . (removeNOfAKind 3) . (removeNOfAKind 4) . (removeNOfAKind 5) . remove222 . remove33 . remove42 . removeStraight . (removeNOfAKind 6) $ (0, sortByFrequency dice) 

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

