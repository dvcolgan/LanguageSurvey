(ns farkle.core
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
     0
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

(defprotocol FarklePlayer
  (get-name [this])
  (query-set-aside [this remaining set-aside turn-score total-scores])
  (query-stop [this remaining set-aside turn-score total-scores])
  (warn-invalid-set-aside [this])
  (warn-farkle [this roll]))

(deftype GreedyAIPlayer [name stop-threshold]
  FarklePlayer
  (get-name [this]
    name)
  (query-set-aside [this remaining set-aside turn-score total-scores]
    (let [dice-score (get-score remaining)]
      (if (and (= (count remaining) 6)
               (or (= dice-score 1500)
                   (= dice-score 2500)
                   (= dice-score 3000)))
        remaining
        (let [freqs (frequencies remaining)
              new-set-aside (filter #(or (>= (freqs %) 3)
                                         (= % 1)
                                         (= % 5))
                                    remaining)]
          (do
           ; (println "AI player set aside" new-set-aside)
            new-set-aside)))))

  (query-stop [this remaining set-aside turn-score total-scores]
    (> turn-score stop-threshold))
    
  (warn-invalid-set-aside [this]
    ;(println "AI player made an invalid set aside!")
                          )

  (warn-farkle [this roll]
    ;(println "AI player got a farkle!")
    ;(println "Dice:" roll)
               )
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

(defn -main [& args]
  (loop [times 10000]
    (let [winner (play-farkle [(GreedyAIPlayer. "Greedy Player 1" 300)
                               (GreedyAIPlayer. "Greedy Player 2" 500)
                               (GreedyAIPlayer. "Greedy Player 3" 800)
                               (GreedyAIPlayer. "Greedy Player 4" 1000)])]
      (do
        ;(println "The winner is" (get-name winner) "!")
        (if (= (mod times 1000) 0) (println times " games left."))
        (if (> times 0)
          (recur (- times 1))
          (println "Done"))))))
