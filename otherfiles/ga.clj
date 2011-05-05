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
