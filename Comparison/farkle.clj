(ns farkle
  (:use clojure.contrib.str-utils)
  (:use clojure.test clojure.set)
  (:gen-class)
  )

(defn third [x]
  (first (next (next x))))

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

(defn value-of-extra-1s-and-5s [dice]
  (let [freqs (frequencies dice)]
    (+ (if (<= (freqs 1 0) 2)
         (* (freqs 1 0) 100)
         0)
       (if (<= (freqs 5 0) 2)
         (* (freqs 5 0) 50)
         0))))

(defn have-straight? [dice]
  (= (sort dice)
     (range 1 7)))

(defn roll-has-nonscoring-dice [dice]
  (let [die-map (frequencies dice)]
    (not
      (every? true? (map #(or (or (= (val %) 0)
                                  (<= 3 (val %) 6))
                              (= (key %) 1)
                              (= (key %) 5))
                         die-map)))))

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

(defn is-farkle [dice]
  (= (get-score dice) 0))

(defn contains-one-scoring-die [dice]
  (let [freqs (frequencies dice)]
    (and (< (freqs 2) 3)
         (< (freqs 3) 3)
         (< (freqs 4) 3)
         (< (freqs 6) 3)
         (or (and (= (freqs 1) 1)
                  (= (freqs 5) 0))
             (and (= (freqs 1) 0)
                  (= (freqs 5) 1))))))

(defn contains-only-three-of-a-kind [dice]
  (let [freqs (frequencies dice)]
    (and (not (<= 1 (freqs 1) 2))
         (not (<= 1 (freqs 5) 2))
         (= (reduce + (map #(if (= (val %) 3) 1 0) freqs)) 1))))

(defn all-dice-score [dice]
  ;;TODO
  )

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

(defn rand-int01 []
  (rand-int 2))

(defn rand-int02 []
  (rand-int 3))

(defn rand-range-50-3500 []
  (rand-nth (range 0 3501 50)))

(def gene-mutator
     [
      rand-int01, ;0, rolled 3, two 1's: 0=take one, 1=take two
      rand-int01, ;1, rolled 3, two 5's: 0=take one, 1=take two
      rand-int01, ;2, rolled 3, one 1 and one 5: 0=take 1, 1=take both

      rand-int01, ;3, rolled 4, two 1's: 0=take one, 1=take two
      rand-int01, ;4, rolled 4, two 5's: 0=take one, 1=take two
      rand-int01, ;5, rolled 4, one 1 and one 5: 0=take 1, 1=take both

      rand-int02, ;6, rolled 5, three 1's and a 5: 0=take one, 1=take three, 2=take four
      rand-int02, ;7, rolled 5, three 2's and a 1 or 5: 0=take one, 1=take three, 2=take four
      rand-int02, ;8, rolled 5, three 3's and a 1 or 5: 0=take one, 1=take three, 2=take four
      rand-int02, ;9, rolled 5, three 4's and a 1 or 5: 0=take one, 1=take three, 2=take four
      rand-int02, ;10, rolled 5, three 5's and a 1: 0=take one, 1=take three, 2=take four
      rand-int02, ;11, rolled 5, three 6's and a 1 or 5: 0=take one, 1=take three, 2=take four

      rand-int01, ;12, rolled 5, two 1's: 0=take one, 1=take two
      rand-int01, ;13, rolled 5, two 5's: 0=take one, 1=take two
      rand-int01, ;14, rolled 5, one 1 and one 5: 0=take 1, 1=take both

      rand-int02, ;15, rolled 6, three 1's and two 5's: 0=take one, 1=take three, 2=take five
      rand-int02, ;16, rolled 6, three 2's and two others: 0=take one, 1=take three, 2=take five
      rand-int02, ;17, rolled 6, three 3's and two others: 0=take one, 1=take three, 2=take five
      rand-int02, ;18, rolled 6, three 4's and two others: 0=take one, 1=take three, 2=take five
      rand-int02, ;19, rolled 6, three 5's and two 1's: 0=take one, 1=take three, 2=take five
      rand-int02, ;20, rolled 6, three 6's and two others: 0=take one, 1=take three, 2=take five

      rand-int02, ;21, rolled 6, three 1's and a 5: 0=take one, 1=take three, 2=take four
      rand-int02, ;22, rolled 6, three 2's and a 1 or 5: 0=take one, 1=take three, 2=take four
      rand-int02, ;23, rolled 6, three 3's and a 1 or 5: 0=take one, 1=take three, 2=take four
      rand-int02, ;24, rolled 6, three 4's and a 1 or 5: 0=take one, 1=take three, 2=take four
      rand-int02, ;25, rolled 6, three 5's and a 1: 0=take one, 1=take three, 2=take four
      rand-int02, ;26, rolled 6, three 6's and a 1 or 5: 0=take one, 1=take three, 2=take four

      rand-int01, ;27, rolled 6, two 1's: 0=take one, 1=take two
      rand-int01, ;28, rolled 6, two 5's: 0=take one, 1=take two
      rand-int01, ;29, rolled 6, one 1 and one 5: 0=take 1, 1=take both

      rand-range-50-3500, ;30, if have 1 dice left, threshold to stop at
      rand-range-50-3500, ;31, if have 2 dice left, threshold to stop at
      rand-range-50-3500, ;32, if have 3 dice left, threshold to stop at
      rand-range-50-3500, ;33, if have 4 dice left, threshold to stop at
      rand-range-50-3500, ;34, if have 5 dice left, threshold to stop at
      rand-range-50-3500, ;35, if have 6 dice left, threshold to stop at
      ])

(defn create-random-gene []
  (for [chromosome-mutator gene-mutator]
    (chromosome-mutator)))

(deftype GAPlayer [gene]
  FarklePlayer
  (query-set-aside [this remaining set-aside turn-score total-scores]
    (let [die-counts (frequencies remaining)]
      (cond
       (or (contains-one-scoring-die remaining)
	   (contains-only-three-of-a-kind remaining)
	   (>= (get-score remaining) 1000)
	   (all-dice-score remaining)) (get-most-valuable-set-aside remaining)
       

       (= (count remaining) 2) (get-most-valuable-set-aside remaining)

       (= (count remaining) 3) (cond
				(= (die-counts 1) 2) (cond
						      (= (nth gene 0) 0) [1]
						      (= (nth gene 0) 1) [1,1])
				(= (die-counts 5) 2) (cond
						      (= (nth gene 1) 0) [5]
						      (= (nth gene 1) 1) [5,5])
				(and (= (die-counts 1) 1)
				     (= (die-counts 5) 1)) (cond
							    (= (nth gene 2) 0) [1]
							    (= (nth gene 2) 1) [1,5]))

       (= (count remaining) 4) (cond
				(= (die-counts 1) 2) (cond
						      (= (nth gene 3) 0) [1]
						      (= (nth gene 3) 1) [1,1])
				(= (die-counts 5) 2) (cond
						      (= (nth gene 4) 0) [5]
						      (= (nth gene 4) 1) [5,5])
				(and (= (die-counts 1) 1)
				     (= (die-counts 5) 1)) (cond
							    (= (nth gene 5) 0) [1]
							    (= (nth gene 5) 1) [1,5]))

       (= (count remaining) 5) (cond
				(contains-three-of-a-kind-and-one-other remaining 1) (cond
										      (= (nth gene 6) 0) (get-most-valuable-single-die remaining)
										      (= (nth gene 6) 1) (get-three-of-a-kind remaining)
										      (= (nth gene 6) 2) (get-most-valuable-set-aside remaining))
				(contains-three-of-a-kind-and-one-other remaining 2) (cond
										      (= (nth gene 7) 0) (get-most-valuable-single-die remaining)
										      (= (nth gene 7) 1) (get-three-of-a-kind remaining)
										      (= (nth gene 7) 2) (get-most-valuable-set-aside remaining))
				(contains-three-of-a-kind-and-one-other remaining 3) (cond
										      (= (nth gene 8) 0) (get-most-valuable-single-die remaining)
										      (= (nth gene 8) 1) (get-three-of-a-kind remaining)
										      (= (nth gene 8) 2) (get-most-valuable-set-aside remaining))
				(contains-three-of-a-kind-and-one-other remaining 4) (cond
										      (= (nth gene 9) 0) (get-most-valuable-single-die remaining)
										      (= (nth gene 9) 1) (get-three-of-a-kind remaining)
										      (= (nth gene 9) 2) (get-most-valuable-set-aside remaining))
				(contains-three-of-a-kind-and-one-other remaining 5) (cond
										      (= (nth gene 10) 0) (get-most-valuable-single-die remaining)
										      (= (nth gene 10) 1) (get-three-of-a-kind remaining)
										      (= (nth gene 10) 2) (get-most-valuable-set-aside remaining))
				(contains-three-of-a-kind-and-one-other remaining 6) (cond
										      (= (nth gene 11) 0) (get-most-valuable-single-die remaining)
										      (= (nth gene 11) 1) (get-three-of-a-kind remaining)
										      (= (nth gene 11) 2) (get-most-valuable-set-aside remaining))
										    
				(= (die-counts 1) 2) (cond
						      (= (nth gene 12) 0) [1]
						      (= (nth gene 12) 1) [1,1])
				(= (die-counts 5) 2) (cond
						      (= (nth gene 13) 0) [5]
						      (= (nth gene 13) 1) [5,5])
				(and (= (die-counts 1) 1)
				     (= (die-counts 5) 1)) (cond
							    (= (nth gene 14) 0) [1]
							    (= (nth gene 14) 1) [1,5]))
	     

       (= (count remaining) 6) (cond
				(contains-three-of-a-kind-and-two-others remaining 1) (cond
										      (= (nth gene 15) 0) (get-most-valuable-single-die remaining)
										      (= (nth gene 15) 1) (get-three-of-a-kind remaining)
										      (= (nth gene 15) 2) (get-most-valuable-set-aside remaining))
				(contains-three-of-a-kind-and-two-others remaining 2) (cond
										      (= (nth gene 16) 0) (get-most-valuable-single-die remaining)
										      (= (nth gene 16) 1) (get-three-of-a-kind remaining)
										      (= (nth gene 16) 2) (get-most-valuable-set-aside remaining))
				(contains-three-of-a-kind-and-two-others remaining 3) (cond
										      (= (nth gene 17) 0) (get-most-valuable-single-die remaining)
										      (= (nth gene 17) 1) (get-three-of-a-kind remaining)
										      (= (nth gene 17) 2) (get-most-valuable-set-aside remaining))
				(contains-three-of-a-kind-and-two-others remaining 4) (cond
										      (= (nth gene 18) 0) (get-most-valuable-single-die remaining)
										      (= (nth gene 18) 1) (get-three-of-a-kind remaining)
										      (= (nth gene 18) 2) (get-most-valuable-set-aside remaining))
				(contains-three-of-a-kind-and-two-others remaining 5) (cond
										      (= (nth gene 19) 0) (get-most-valuable-single-die remaining)
										      (= (nth gene 19) 1) (get-three-of-a-kind remaining)
										      (= (nth gene 19) 2) (get-most-valuable-set-aside remaining))
				(contains-three-of-a-kind-and-two-others remaining 6) (cond
										      (= (nth gene 20) 0) (get-most-valuable-single-die remaining)
										      (= (nth gene 20) 1) (get-three-of-a-kind remaining)
										      (= (nth gene 20) 2) (get-most-valuable-set-aside remaining))

				(contains-three-of-a-kind-and-one-other remaining 1) (cond
										      (= (nth gene 21) 0) (get-most-valuable-single-die remaining)
										      (= (nth gene 21) 1) (get-three-of-a-kind remaining)
										      (= (nth gene 21) 2) (get-most-valuable-set-aside remaining))
				(contains-three-of-a-kind-and-one-other remaining 2) (cond
										      (= (nth gene 22) 0) (get-most-valuable-single-die remaining)
										      (= (nth gene 22) 1) (get-three-of-a-kind remaining)
										      (= (nth gene 22) 2) (get-most-valuable-set-aside remaining))
				(contains-three-of-a-kind-and-one-other remaining 3) (cond
										      (= (nth gene 23) 0) (get-most-valuable-single-die remaining)
										      (= (nth gene 23) 1) (get-three-of-a-kind remaining)
										      (= (nth gene 23) 2) (get-most-valuable-set-aside remaining))
				(contains-three-of-a-kind-and-one-other remaining 4) (cond
										      (= (nth gene 24) 0) (get-most-valuable-single-die remaining)
										      (= (nth gene 24) 1) (get-three-of-a-kind remaining)
										      (= (nth gene 24) 2) (get-most-valuable-set-aside remaining))
				(contains-three-of-a-kind-and-one-other remaining 5) (cond
										      (= (nth gene 25) 0) (get-most-valuable-single-die remaining)
										      (= (nth gene 25) 1) (get-three-of-a-kind remaining)
										      (= (nth gene 25) 2) (get-most-valuable-set-aside remaining))
				(contains-three-of-a-kind-and-one-other remaining 6) (cond
										      (= (nth gene 26) 0) (get-most-valuable-single-die remaining)
										      (= (nth gene 26) 1) (get-three-of-a-kind remaining)
										      (= (nth gene 26) 2) (get-most-valuable-set-aside remaining))
										    

				(= (die-counts 1) 2) (cond
						      (= (nth gene 27) 0) [1]
						      (= (nth gene 27) 1) [1,1])
				(= (die-counts 5) 2) (cond
						      (= (nth gene 28) 0) [5]
						      (= (nth gene 28) 1) [5,5])
				(and (= (die-counts 1) 1)
				     (= (die-counts 5) 1)) (cond
							    (= (nth gene 29) 0) [1]
							    (= (nth gene 29) 1) [1,5])))))

            

  (query-stop [this remaining set-aside turn-score total-scores]
    (let [die-count (count remaining)]
      (cond
       (= die-count 1) (>= turn-score (nth gene 30))
       (= die-count 2) (>= turn-score (nth gene 31))
       (= die-count 3) (>= turn-score (nth gene 32))
       (= die-count 4) (>= turn-score (nth gene 33))
       (= die-count 5) (>= turn-score (nth gene 34))
       (= die-count 6) (>= turn-score (nth gene 35))
       :else true)))
       
  (warn-invalid-set-aside [this]
    nil)

  (warn-farkle [this roll]
    nil)
  )

(defn roll-dice [num-to-roll]
  (for [die (range num-to-roll)]
    (inc (rand-int 6))))

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

(defprotocol GAProblem
  (create-random-individual [this])
  (run-tournament [this individual1 individual2])
  (mate-individuals [this individual1 individual2])
  (mutate-individual [this individual]))

(deftype FarkleProblem []
  GAProblem
  (create-random-individual [this]
    (farkle.game/GAPlayer.))

  (run-tournament [this individual1 individual2]
    (loop [p1-wins 0 p2-wins 0]
      (if (= (play-farkle [individual1 individual2]) individual1)
	(recur (inc p1-wins) p2-wins)
	(recur p1-wins (inc p2-wins)))))

  (mate-individuals [this individual1 individual2]
    (let [pivot (rand-int 10)]
      [(concat (take pivot individual1) (drop pivot individual2))
       (concat (take pivot individual2) (drop pivot individual1))]))

  (mutate-individual [this individual]
    (let [pivot (rand-int 10)]
      ;do something to mutate this individual
      individual))
)
		  
(deftype SequenceProblem []
  GAProblem
  (create-random-individual [this]
    (vec (repeatedly 10 #(rand-int 10))))

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

(defn find-converging-individual [population]
  (let [[frequency individual]
	(first
	 (reverse
	  (sort
	   (map-invert
	    (into (hash-map) (frequencies population))))))]
    [(/ frequency (count population))
     individual]))

(defn run-ga [problem-manager population-size max-generations mutation-rate crossover-rate]
  (loop [generation 0
	 population (repeatedly population-size #(create-random-individual problem-manager))]
    (let [mating-pool (map (fn [i1 i2] (run-tournament problem-manager i1 i2))
			    (repeatedly population-size #(rand-nth population))
			    (repeatedly population-size #(rand-nth population)))

	  crossed-pool (mapcat identity (map (fn [i1 i2]
						(if (< (rand) crossover-rate)
						  (mate-individuals problem-manager i1 i2)
						  [i1 i2]))
					      (repeatedly population-size #(rand-nth mating-pool))
					      (repeatedly population-size #(rand-nth mating-pool))))
	  mutated-pool (map (fn [i]
			       (if (< (rand) mutation-rate)
				 (mutate-individual problem-manager i)
				 i))
			     (repeatedly population-size #(rand-nth crossed-pool)))]
      (let [[convergence most-common-individual] (find-converging-individual mutated-pool)]
	(if (or (> convergence 0.95)
		(> generation max-generations))
	  (str "Most common individual: "
	       most-common-individual ", "
	       convergence ", "
	       generation ", "
	       (str (vec mutated-pool)))
	  (do
	    (println (format "Generation %d" generation))
	    (recur (inc generation) mutated-pool)))))))

(defn -main [& args]
  (let [winner (play-farkle [(GreedyAIPlayer. "David" 600)
			     (GreedyAIPlayer. "Samuel" 1000)])]
    (println "The winner is" (get-name winner) "!")))
