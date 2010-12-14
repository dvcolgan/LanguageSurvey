myLast :: [a] -> a
myLast (x:[]) = x
myLast (x:xs) = myLast xs

myButLast :: [a] -> a
myButLast (x:y:[]) = x
myButLast (x:y:xs) = myButLast (y:xs)

elementAt 1 (x:xs) = x
elementAt n (x:xs) = elementAt (n-1) xs

isPalindrome xs = xs == (reverse xs)

compress [] = []
compress [x] = [x]
compress (x:y:xs) 
    | x == y    = x:compress xs
    | otherwise = x:compress (y:xs)
