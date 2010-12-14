doubleMe x = x + x
doubleUs x y = x*2 + y*2

doubleSmallNumber x = if x > 100
                         then x
                         else x*2

factorial :: (Integral a) => a -> a
factorial 0 = 1
factorial n = n * factorial (n - 1)

length' :: (Num b) => [a] -> b
length' [] = 0
length' (_:xs) = 1 + length' xs

myCompare :: (Ord a) => a -> a -> Ordering
a `myCompare` b
    | a > b     = GT
    | a == b    = EQ
    | otherwise = LT


bmiTell ::  (Fractional a, Ord a) => a -> a -> [Char]
bmiTell weight height
    | bmi <= skinny = "Skinny"
    | bmi <= normal = "Normal"
    | bmi <= fat    = "Fat"
    | otherwise     = "Obese"
    where bmi = weight / height ^ 2
          skinny = 18.5
          normal = 25.0
          fat = 30.0

maximum' :: (Ord a) => [a] -> a  
maximum' [] = error "maximum of empty list"  
maximum' [x] = x  
maximum' (x:xs)   
    | x > maxTail = x  
    | otherwise = maxTail  
    where maxTail = maximum' xs  

maximum' :: (Ord a) => [a] -> a  
maximum' [] = error "maximum of empty list"  
maximum' [x] = x  
maximum' (x:xs) = max x (maximum' xs)

take' _ [] = []
take' 0 _ = []
take' n (x:xs) = x:take' (n-1) xs

reverse' [] = []
reverse' (x:xs) = reverse' xs ++ [x]

zip' [] _ = []
zip' _ [] = []
zip' (x:xs) (y:ys) = (x, y):zip' xs ys
