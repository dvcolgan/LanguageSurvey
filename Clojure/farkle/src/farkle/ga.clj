(ns farkle.ga
  (:use clojure.test clojure.set)
  (:use farkle.game)
  )

(defn rand-int01 []
  (rand-int 2))
(defn rand-int02 []
  (rand-int 3))
(defn rand-range-50-3500 []
  (rand-nth (range 0 3501 50)))

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




      
