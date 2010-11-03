(use 'clojure.test)




;(defstruct player :name :strategy










(defn third [x]
  (first (next (next x))))

(deftest third-test
  (is (= 1 (third [3 2 1])))
  (is (= nil (third [3 2])))
  (is (= 1 (third [3 2 1 0])))
  )


(defn sort-by-frequency [lst]
  (let [counts (seq (frequencies lst))]
    (sort
     (fn [a b]
       (let [comp (compare (second b)
			   (second a))]
	 (if (= comp 0)
	   (compare (first a)
		    (first b))
	   comp)))
     counts)))

(deftest sort-by-frequency-test
  (is (= (sort-by-frequency []) '()))
  (is (= (sort-by-frequency [1]) '([1 1])))
  (is (= (sort-by-frequency [1 1]) '([1 2])))
  (is (= (sort-by-frequency [1 1 1]) '([1 3])))
  (is (= (sort-by-frequency [1 1 1 1]) '([1 4])))
  (is (= (sort-by-frequency [1 1 1 1 1]) '([1 5])))
  (is (= (sort-by-frequency [1 1 1 1 1 1]) '([1 6])))
  (is (= (sort-by-frequency [1 2 3 4 5 6]) '([1 1] [2 1] [3 1] [4 1] [5 1] [6 1])))
  (is (= (sort-by-frequency [1 1 1]) '([1 3])))
  )

(defn value-of-extra-1s-and-5s [die-counts]
  (let [die-map (into (hash-map) die-counts)]
    (+ (if (<= (die-map 1 0) 2)
	 (* (die-map 1 0) 100)
	 0)
       (if (<= (die-map 5 0) 2)
	 (* (die-map 5 0) 50)
	 0))))
(deftest value-of-extra-1s-and-5s-test
  (is (= (value-of-extra-1s-and-5s '()) 0))
  (is (= (value-of-extra-1s-and-5s '([1 1])) 100))
  (is (= (value-of-extra-1s-and-5s '([5 1])) 50))
  (is (= (value-of-extra-1s-and-5s '([1 1] [5 1])) 150))
  (is (= (value-of-extra-1s-and-5s '([1 2] [5 2])) 300))
  (is (= (value-of-extra-1s-and-5s '([1 3] [5 3])) 0))
  (is (= (value-of-extra-1s-and-5s '([1 1] [5 3])) 100))
  (is (= (value-of-extra-1s-and-5s '([1 3] [5 2])) 100))
  (is (= (value-of-extra-1s-and-5s '([2 3] [1 2] [5 1])) 250))
  )


(defn have-straight? [dice]
  (= (sort dice)
     (range 1 7)))


(defn get-score [dice]
  (let [die-counts (sort-by-frequency dice)
	[fst-die fst-cnt] (first die-counts)
	[snd-die snd-cnt] (second die-counts)
    	[trd-die trd-cnt] (third die-counts)
	single-dice-value (value-of-extra-1s-and-5s die-counts)]
  (cond
   (and (= fst-cnt 4) (= snd-cnt 2)) 1500
   (and (= fst-cnt 3) (= snd-cnt 3)) 2500
   (and (= fst-cnt 2) (= snd-cnt 2) (= trd-cnt 2)) 1500
   (have-straight? dice) 1500
   (= fst-cnt 6) 3000
   (= fst-cnt 5) (+ single-dice-value 2000)
   (= fst-cnt 4) (+ single-dice-value 1000)
   (= fst-cnt 3) (+ single-dice-value
		    (if (= fst-die 1)
		      300
		      (* fst-die 100)))
   :else single-dice-value)))

(deftest get-score-test
  (is (= (get-score [1 ]) 100))
  (is (= (get-score [5 ]) 50))
  (is (= (get-score [2 ]) 0))
  (is (= (get-score [3 ]) 0))
  (is (= (get-score [4 ]) 0))
  (is (= (get-score [6 ]) 0))
  (is (= (get-score [1 5]) 150))
  (is (= (get-score [1 1]) 200))
  (is (= (get-score [5 5]) 100))
  (is (= (get-score [2 3]) 0))
  (is (= (get-score [4 6]) 0))
  (is (= (get-score [1 1 1]) 300))
  (is (= (get-score [2 2 2]) 200))
  (is (= (get-score [3 3 3]) 300))
  (is (= (get-score [4 4 4]) 400))
  (is (= (get-score [5 5 5]) 500))
  (is (= (get-score [6 6 6]) 600))
  (is (= (get-score [2 3 4]) 0))
  (is (= (get-score [1 5 6]) 150))
  (is (= (get-score [3 5 6]) 50))
  (is (= (get-score [1 1 1 1]) 1000))
  (is (= (get-score [2 2 2 2]) 1000))
  (is (= (get-score [3 3 3 3]) 1000))
  (is (= (get-score [4 4 4 4]) 1000))
  (is (= (get-score [5 5 5 5]) 1000))
  (is (= (get-score [6 6 6 6]) 1000))
  (is (= (get-score [6 6 6 1]) 700))
  (is (= (get-score [4 4 4 5]) 450))
  (is (= (get-score [3 3 3 4]) 300))
  (is (= (get-score [1 2 3 4]) 100))
  (is (= (get-score [3 4 5 6]) 50))
  (is (= (get-score [2 3 4 6]) 0))
  (is (= (get-score [1 1 1 1 1]) 2000))
  (is (= (get-score [2 2 2 2 2]) 2000))
  (is (= (get-score [3 3 3 3 3]) 2000))
  (is (= (get-score [4 4 4 4 4]) 2000))
  (is (= (get-score [5 5 5 5 5]) 2000))
  (is (= (get-score [6 6 6 6 6]) 2000))
  (is (= (get-score [1 1 1 1 1 1]) 3000))
  (is (= (get-score [2 2 2 2 2 2]) 3000))
  (is (= (get-score [3 3 3 3 3 3]) 3000))
  (is (= (get-score [4 4 4 4 4 4]) 3000))
  (is (= (get-score [5 5 5 5 5 5]) 3000))
  (is (= (get-score [6 6 6 6 6 6]) 3000))
  (is (= (get-score [1 1 1 2 2 2]) 2500))
  (is (= (get-score [3 3 3 4 4 4]) 2500))
  (is (= (get-score [5 5 5 6 6 6]) 2500))
  (is (= (get-score [1 1 2 2 3 3]) 1500))
  (is (= (get-score [4 4 5 5 6 6]) 1500))
  (is (= (get-score [1 1 1 1 2 2]) 1500))
  (is (= (get-score [3 3 3 3 4 4]) 1500))
  (is (= (get-score [5 5 5 5 6 6]) 1500))
  )
   


    
    

(run-tests)
