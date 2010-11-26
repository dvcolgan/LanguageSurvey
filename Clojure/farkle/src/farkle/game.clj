(ns farkle.game
  (:use clojure.contrib.str-utils)
  (:use clojure.test clojure.set)
)

(defn third [x]
  (first (next (next x))))


(deftest test-third
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
  (is (= (sort-by-frequency [1 3 3 3 4 4]) '([3 3] [4 2] [1 1])))
  (is (= (sort-by-frequency [1 1 1]) '([1 3])))
  )

(defn value-of-extra-1s-and-5s [dice]
  (let [freqs (frequencies dice)]
    (+ (if (<= (freqs 1 0) 2)
         (* (freqs 1 0) 100)
         0)
       (if (<= (freqs 5 0) 2)
         (* (freqs 5 0) 50)
         0))))

(deftest value-of-extra-1s-and-5s-test
  (is (= (value-of-extra-1s-and-5s [1]) 100))
  (is (= (value-of-extra-1s-and-5s [5]) 50))
  (is (= (value-of-extra-1s-and-5s [1 5]) 150))
  (is (= (value-of-extra-1s-and-5s [5 1 1 5]) 300))
  (is (= (value-of-extra-1s-and-5s [1 1 1]) 0))
  (is (= (value-of-extra-1s-and-5s [1]) 100))
  (is (= (value-of-extra-1s-and-5s [5 5]) 100))
  (is (= (value-of-extra-1s-and-5s [5 1 1 5 3]) 300))
  )


(defn have-straight? [dice]
  (= (sort dice)
     (range 1 7)))

(deftest test-have-straight
  (is (have-straight? [1 2 3 4 5 6]))
  (is (have-straight? [2 1 4 3 6 5]))
  )

(defn roll-has-nonscoring-dice [dice]
  (let [die-map (frequencies dice)]
    (not
      (every? true? (map #(or (or (= (val %) 0)
                                  (<= 3 (val %) 6))
                              (= (key %) 1)
                              (= (key %) 5))
                         die-map)))))

(deftest test-roll-has-nonscoring-dice
  (is (= (roll-has-nonscoring-dice [1]) false))
  (is (= (roll-has-nonscoring-dice [2]) true))
  (is (= (roll-has-nonscoring-dice [3]) true))
  (is (= (roll-has-nonscoring-dice [4]) true))
  (is (= (roll-has-nonscoring-dice [5]) false))
  (is (= (roll-has-nonscoring-dice [6]) true))
  (is (= (roll-has-nonscoring-dice [1 2]) true))
  (is (= (roll-has-nonscoring-dice [1 3]) true))
  (is (= (roll-has-nonscoring-dice [1 4]) true))
  (is (= (roll-has-nonscoring-dice [1 5]) false))
  (is (= (roll-has-nonscoring-dice [1 6]) true))
  (is (= (roll-has-nonscoring-dice [5 1 1 5]) false))
  )


(defn get-score
  ([dice] (get-score dice false))
  ([dice zero-for-extra]
   (if (= (count dice) 0)
     (do (println "here")
     0)
     (let [die-counts (sort-by-frequency dice)
           [fst-die fst-cnt] (first die-counts)
           [snd-die snd-cnt] (second die-counts)
           [trd-die trd-cnt] (third die-counts)
           single-dice-value (value-of-extra-1s-and-5s dice)]
       (cond
         (and (= fst-cnt 4) (= snd-cnt 2)) 1500
         (and (= fst-cnt 3) (= snd-cnt 3)) 2500
         (and (= fst-cnt 2) (= snd-cnt 2) (= trd-cnt 2)) 1500
         (have-straight? dice) 1500
         (= fst-cnt 6) 3000
         (and zero-for-extra (roll-has-nonscoring-dice dice)) 0
         (= fst-cnt 5) (+ single-dice-value 2000)
         (= fst-cnt 4) (+ single-dice-value 1000)
         (= fst-cnt 3) (+ single-dice-value
                          (if (= fst-die 1)
                            300
                            (* fst-die 100)))
         :else single-dice-value)))))



(deftest get-score-test
  (is (= (get-score [1]) 100))
  (is (= (get-score [5]) 50))
  (is (= (get-score [2]) 0))
  (is (= (get-score [3]) 0))
  (is (= (get-score [4]) 0))
  (is (= (get-score [6]) 0))
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
  (is (= (get-score [1 2] true) 0))
  (is (= (get-score [1 3] true) 0))
  (is (= (get-score [1 4] true) 0))
  (is (= (get-score [1 6] true) 0))
  (is (= (get-score [2 3] true) 0))
  (is (= (get-score [4 6] true) 0))
  (is (= (get-score [2 3 4] true) 0))
  (is (= (get-score [1 5 6] true) 0))
  (is (= (get-score [3 5 6] true) 0))
  (is (= (get-score [3 3 3 4] true) 0))
  (is (= (get-score [2 2 2 4] true) 0))
  (is (= (get-score [2 2 2 3] true) 0))
  (is (= (get-score [6 6 6 4] true) 0))
  (is (= (get-score [6 6 6 3] true) 0))
  (is (= (get-score [1 2 3 4] true) 0))
  (is (= (get-score [3 4 5 6] true) 0))
  (is (= (get-score [2 3 4 6] true) 0))
  (is (= (get-score [5 1 1 5] true) 300))
  )

(defn contains-values [first-vals second-vals]
  (loop [container (sort first-vals)
         containee (sort second-vals)]
    (if (= (count containee) 0)
      true
      (if (= (count container) 0)
        false
        (if (= (first container)
               (first containee))
          (recur (rest container)
                 (rest containee))
          (recur (rest container)
                 containee))))))

(defn is-valid-set-aside [remaining new-set-aside]
  (and (contains-values remaining new-set-aside)
       (> (get-score new-set-aside true) 0)))

(deftest test-is-valid-set-aside
  (is (= (is-valid-set-aside [5 1 1 5] [5 1 1 5]) true))
  (is (= (is-valid-set-aside [1 4 5 1 1 5] [4 5 1 1 5]) false))
  )



(defn is-farkle [dice]
  (= (get-score dice) 0))


(defprotocol FarklePlayer
  (get-name [this])
  (query-set-aside [this remaining set-aside turn-score total-scores])
  (query-stop [this remaining set-aside turn-score total-scores])
  (warn-invalid-set-aside [this])
  (warn-farkle [this roll]))



(deftype GAPlayer []
  FarklePlayer
  (get-name [this]
    "GAPlayer")

  (query-set-aside [this remaining set-aside turn-score total-scores]
    [])

  (query-stop [this remaining set-aside turn-score total-scores]
    true)
  
  (warn-invalid-set-aside [this]
    (println "I don't know what you did, but the GA player should never invalid set aside."))

  (warn-farkle [this roll]
    nil)
  )




(deftype GreedyAIPlayer [name stop-threshold]
  FarklePlayer
  (get-name [this]
    name)
  (query-set-aside [this remaining set-aside turn-score total-scores]
    (println "AI player rolled" remaining)
    (if (and (= (count remaining) 6)
	     (> (get-score remaining) 1000))
      remaining
      (let [freqs (frequencies remaining)
            new-set-aside (filter #(or (= (freqs %) 3)
                                       (= % 1)
                                       (= % 5))
                                  remaining)]
        (do
          (println "AI player set aside" new-set-aside)
          new-set-aside))))

  (query-stop [this remaining set-aside turn-score total-scores]
    (> turn-score stop-threshold))
    
  (warn-invalid-set-aside [this]
    (println "AI player made an invalid set aside!"))

  (warn-farkle [this roll]
    (println "AI player got a farkle!")
    (println "Dice:" roll))
  )

(deftest test-GreedyAIPlayer
  (is (=
       (query-set-aside (GreedyAIPlayer. "David" 500)
			[1 2 3 4 5] [1] 100 [])
       [1 5]))
  (is (=
       (query-stop (GreedyAIPlayer. "David" 500)
		   [2 3 4] [1 1 5] 250 [])
       false))
)


(deftype HumanPlayer [name]
  FarklePlayer
  (get-name [this]
    name)
  (query-set-aside [this remaining set-aside turn-score total-scores]
    (println "\n\nScores:\n")
    (doseq [[i score] (map-indexed vector total-scores)]
      (println (format "Player %d: %d" i score)))
    (println "Turn score:" turn-score)
    
    (println "Set Aside:")
    (println set-aside)
    
    (println "You roll the dice:")
    (println remaining)
    (println "Indicate the dice you want to set aside by entering their numbers separated by spaces.")

    ;;TODO this throws an exception and crashes on invalid input, tried using try/catch, couldn't get it to work
    (let [choices (read-line)]
      (map #(Integer/parseInt %) (re-split #" " choices))))

  (query-stop [this remaining set-aside turn-score total-scores]
    (println
      (format
        "You have %d points.  Hit enter to continue rolling, or type 'stop' to end your turn."
        turn-score))
    (let [choice (read-line)]
      (if (= choice "")
        false
        true)))

  (warn-invalid-set-aside [this]
    (println "That set aside is invalid!"))

  (warn-farkle [this roll]
    (println "You got a farkle!")
    (println "Dice:" roll))
)


(defn roll-dice [num-to-roll]
  (for [die (range num-to-roll)]
    (inc (rand-int 6))))


(deftest test-roll-dice
  (is (every? #(<= 1 % 6) (roll-dice 1000))))





(defn get-validated-set-aside [player remaining set-aside turn-score total-scores]
  (loop [new-set-aside (query-set-aside player remaining set-aside turn-score total-scores)]
    (if (is-valid-set-aside remaining new-set-aside)
      new-set-aside
      (do
        (warn-invalid-set-aside player)
        (recur (query-set-aside player remaining set-aside turn-score total-scores))))))

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







  
	

(run-tests)
;(main)
