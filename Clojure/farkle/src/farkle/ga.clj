(ns farkle.ga
  )

(defn rand-int01 []
  (rand-int 2))
(defn rand-int02 []
  (rand-int 3))
(defn rand-range-50-3500 []
  (rand-nth (range 0 3501 50)))


(defn find-converging-individual [population]
  (let [[frequency individual]
	(first
	 (reverse
	  (sort
	   (map-invert
	    (into (hash-map) (frequencies population))))))]
    [(/ frequency (count population))
     individual]))


(defn run-ga [population-size max-generations mutation-rate crossover-rate
	      new-individual-fn fitness-fn crossover-fn mutation-fn]
  (loop [generation 0
	 population (repeatedly population-size new-individual-fn)]
    (let [mating-pool (map fitness-fn
			    (repeatedly population-size #(rand-nth population))
			    (repeatedly population-size #(rand-nth population)))
	  crossed-pool (mapcat identity (map (fn [i1 i2]
						(if (< (rand) crossover-rate)
						  (crossover-fn i1 i2)
						  [i1 i2]))
					      (repeatedly population-size #(rand-nth mating-pool))
					      (repeatedly population-size #(rand-nth mating-pool))))
	  mutated-pool (map (fn [i]
			       (if (< (rand) mutation-rate)
				 (mutation-fn i)
				 i))
			     (repeatedly population-size #(rand-nth crossed-pool)))]
      (let [[convergence most-common-individual] (find-converging-individual mutated-pool)]
	(if (or (> convergence 0.95)
		(> generation max-generations))
	  (str "Most common individual: " most-common-individual ", " convergence ", " generation ", " (str (vec mutated-pool)))
	  (do
	    (format "Generation %d" generation)
	    (recur (inc generation) mutated-pool)))))))




      
(defn generate-random-individual []
  (vec (repeatedly 10 #(rand-int 10))))

(generate-random-individual)
	
(defn evaluate-fitness [individual1 individual2]
  (letfn [(evaluate-fn [individual] (reduce + (map #(if (= %1 %2) 1 0)
						 individual
						 (range 10))))]
    (if (> (evaluate-fn individual1)
	   (evaluate-fn individual2))
      individual1
      individual2)))

(deftest evaluate-fitness-test
  
  (is (= (evaluate-fitness [0 1 2 3 4 5 6 7 8 9] [9 8 7 6 5 4 3 2 1 0]) [0 1 2 3 4 5 6 7 8 9]))
  )

	
(defn do-crossover  [individual1 individual2]
  (let [pivot (rand-int 10)
	[fst-front fst-back] (split-at pivot individual1)
	[snd-front snd-back] (split-at pivot individual2)]
    [(vec (concat fst-front snd-back))
     (vec (concat snd-front fst-back))]))

(do-crossover (generate-random-individual)
	      (generate-random-individual))

(defn do-mutation [individual]
  (let [pivot (rand-int 10)]
    (assoc individual pivot (rand-int 10))))

(do-mutation [0 1 2 3 4 5 6 7 8 9])
