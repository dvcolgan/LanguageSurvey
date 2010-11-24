(ns farkle.core
  (:use clojure.contrib.str-utils)
  (:use clojure.test clojure.set)
  (:gen-class))



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
  (is (= (sort-by-frequency [1 3 3 3 4 4]) '([3 3] [4 2] [1 1])))
  (is (= (sort-by-frequency [1 1 1]) '([1 3])))
  )

(defn value-of-extra-1s-and-5s [die-counts]
  (let [die-map (into (hash-map) die-counts)]
    (+ (if (<= (die-map 1 0) 2) (* (die-map 1 0) 100) 0)
       (if (<= (die-map 5 0) 2) (* (die-map 5 0) 50) 0))))

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



(defn get-score
  ([dice] (get-score dice false))
  ([dice zero-for-extra]
     (if (= (count dice) 0)
       0
       (let [die-map (frequencies dice)
	     die-counts (sort-by-frequency dice)
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
	  (and zero-for-extra
	       (every? true?
		(map #(<= 1 (val %) 2) die-map))) 0
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
  )

(defn is-valid-set-aside [dice]
  (> (get-score dice true) 0))

(defn is-farkle [dice]
  (= (get-score dice) 0))


(defprotocol FarklePlayer
  (get-name [this])
  (query-set-aside [this remaining set-aside turn-score total-scores])
  (query-stop [this remaining set-aside turn-score total-scores])
  (warn-invalid-set-aside [this])
  (warn-farkle [this roll]))


;(deftype GAPlayer [gene]
;  
;self.gene_mutator = [
;self.randint01, #0, rolled 3, two 1's: 0=take one, 1=take two
;self.randint01, #1, rolled 3, two 5's: 0=take one, 1=take two
;self.randint01, #2, rolled 3, one 1 and one 5: 0=take 1, 1=take both
;
;self.randint01, #3, rolled 4, two 1's: 0=take one, 1=take two
;self.randint01, #4, rolled 4, two 5's: 0=take one, 1=take two
;self.randint01, #5, rolled 4, one 1 and one 5: 0=take 1, 1=take both
;
;self.randint02, #6, rolled 5, three 1's and a 5: 0=take one, 1=take three, 2=take four
;self.randint02, #7, rolled 5, three 2's and a 1 or 5: 0=take one, 1=take three, 2=take four
;self.randint02, #8, rolled 5, three 3's and a 1 or 5: 0=take one, 1=take three, 2=take four
;self.randint02, #9, rolled 5, three 4's and a 1 or 5: 0=take one, 1=take three, 2=take four
;self.randint02, #10, rolled 5, three 5's and a 1: 0=take one, 1=take three, 2=take four
;self.randint02, #11, rolled 5, three 6's and a 1 or 5: 0=take one, 1=take three, 2=take four
;
;self.randint01, #12, rolled 5, two 1's: 0=take one, 1=take two
;self.randint01, #13, rolled 5, two 5's: 0=take one, 1=take two
;self.randint01, #14, rolled 5, one 1 and one 5: 0=take 1, 1=take both
;
;self.randint02, #15, rolled 6, three 1's and two 5's: 0=take one, 1=take three, 2=take five
;self.randint02, #16, rolled 6, three 2's and two others: 0=take one, 1=take three, 2=take five
;self.randint02, #17, rolled 6, three 3's and two others: 0=take one, 1=take three, 2=take five
;self.randint02, #18, rolled 6, three 4's and two others: 0=take one, 1=take three, 2=take five
;self.randint02, #19, rolled 6, three 5's and two 1's: 0=take one, 1=take three, 2=take five
;self.randint02, #20, rolled 6, three 6's and two others: 0=take one, 1=take three, 2=take five
;
;self.randint02, #21, rolled 6, three 1's and a 5: 0=take one, 1=take three, 2=take four
;self.randint02, #22, rolled 6, three 2's and a 1 or 5: 0=take one, 1=take three, 2=take four
;self.randint02, #23, rolled 6, three 3's and a 1 or 5: 0=take one, 1=take three, 2=take four
;self.randint02, #24, rolled 6, three 4's and a 1 or 5: 0=take one, 1=take three, 2=take four
;self.randint02, #25, rolled 6, three 5's and a 1: 0=take one, 1=take three, 2=take four
;self.randint02, #26, rolled 6, three 6's and a 1 or 5: 0=take one, 1=take three, 2=take four
;
;self.randint01, #27, rolled 6, two 1's: 0=take one, 1=take two
;self.randint01, #28, rolled 6, two 5's: 0=take one, 1=take two
;self.randint01, #29, rolled 6, one 1 and one 5: 0=take 1, 1=take both
;
;self.randrange50_3500, #30, if have 1 dice left, threshold to stop at
;self.randrange50_3500, #31, if have 2 dice left, threshold to stop at
;self.randrange50_3500, #32, if have 3 dice left, threshold to stop at
;self.randrange50_3500, #33, if have 4 dice left, threshold to stop at
;self.randrange50_3500, #34, if have 5 dice left, threshold to stop at
;self.randrange50_3500, #35, if have 6 dice left, threshold to stop at
;        ]
;
;        if gene is not None:
;            self.gene = gene
;        else:
;            self.gene = [self.gene_mutator[i]() for i in range(len(self.gene_mutator))]
;
;
;  (query_set_aside [this remaining set-aside turn-score total-scores]
;    (if (remaining.contains_one_scoring_die() or
;            remaining.contains_only_three_of_a_kind() or
;            remaining.get_score() >= 1000 or
;            remaining.all_dice_score()):
;            return remaining.get_most_valuable_set_aside()
;
;        if remaining.count() == 2:
;            return remaining.get_most_valuable_set_aside()
;
;        if remaining.count() == 3:
;            if remaining.get_counts()[1] == 2:
;                if self.gene[0] == 0: return (1,)
;                if self.gene[0] == 1: return (1,1)
;            elif remaining.get_counts()[5] == 2:
;                if self.gene[1] == 0: return (5,)
;                if self.gene[1] == 1: return (5,5)
;            elif remaining.get_counts()[1] == 1 and remaining.get_counts()[5] == 1:
;                if self.gene[2] == 0: return (1,)
;                if self.gene[2] == 1: return (1,5)
;
;        if remaining.count() == 4:
;            if remaining.get_counts()[1] == 2:
;                if self.gene[3] == 0: return (1,)
;                if self.gene[3] == 1: return (1,1)
;            elif remaining.get_counts()[5] == 2:
;                if self.gene[4] == 0: return (5,)
;                if self.gene[4] == 1: return (5,5)
;            elif remaining.get_counts()[1] == 1 and remaining.get_counts()[5] == 1:
;                if self.gene[5] == 0: return (1,)
;                if self.gene[5] == 1: return (1,5)
;
;			    
;        if remaining.count() == 5:
;            if remaining.contains_three_of_a_kind_and_one_other(1):
;                if self.gene[6] == 0:
;                    return remaining.get_most_valuable_single_die()
;                if self.gene[6] == 1:
;                    return (1,1,1)
;                if self.gene[6] == 2:
;                    return remaining.get_most_valuable_set_aside()
;            elif remaining.contains_three_of_a_kind_and_one_other(2):
;                if self.gene[7] == 0:
;                    return remaining.get_most_valuable_single_die()
;                if self.gene[7] == 1:
;                    return (2,2,2)
;                if self.gene[7] == 2:
;                    return remaining.get_most_valuable_set_aside()
;            elif remaining.contains_three_of_a_kind_and_one_other(3):
;                if self.gene[8] == 0:
;                    return remaining.get_most_valuable_single_die()
;                if self.gene[8] == 1:
;                    return (3,3,3)
;                if self.gene[8] == 2:
;                    return remaining.get_most_valuable_set_aside()
;            elif remaining.contains_three_of_a_kind_and_one_other(4):
;                if self.gene[9] == 0:
;                    return remaining.get_most_valuable_single_die()
;                if self.gene[9] == 1:
;                    return (4,4,4)
;                if self.gene[9] == 2:
;                    return remaining.get_most_valuable_set_aside()
;            elif remaining.contains_three_of_a_kind_and_one_other(5):
;                if self.gene[10] == 0:
;                    return remaining.get_most_valuable_single_die()
;                if self.gene[10] == 1:
;                    return (5,5,5)
;                if self.gene[10] == 2:
;                    return remaining.get_most_valuable_set_aside()
;            elif remaining.contains_three_of_a_kind_and_one_other(6):
;                if self.gene[11] == 0:
;                    return remaining.get_most_valuable_single_die()
;                if self.gene[11] == 1:
;                    return (6,6,6)
;                if self.gene[11] == 2:
;                    return remaining.get_most_valuable_set_aside()
;
;            elif remaining.get_counts()[1] == 2:
;                if self.gene[12] == 0: return (1,)
;                if self.gene[12] == 1: return (1,1)
;            elif remaining.get_counts()[5] == 2:
;                if self.gene[13] == 0: return (5,)
;                if self.gene[13] == 1: return (5,5)
;            elif remaining.get_counts()[1] == 1 and remaining.get_counts()[5] == 1:
;                if self.gene[14] == 0: return (1,)
;                if self.gene[14] == 1: return (1,5)
;
;
;        if remaining.count() == 6:
;            if remaining.contains_three_of_a_kind_and_two_others(1):
;                if self.gene[15] == 0:
;                    return remaining.get_most_valuable_single_die()
;                if self.gene[15] == 1:
;                    return (1,1,1)
;                if self.gene[15] == 2:
;                    return remaining.get_most_valuable_set_aside()
;            elif remaining.contains_three_of_a_kind_and_two_others(2):
;                if self.gene[16] == 0:
;                    return remaining.get_most_valuable_single_die()
;                if self.gene[16] == 1:
;                    return (2,2,2)
;                if self.gene[16] == 2:
;                    return remaining.get_most_valuable_set_aside()
;            elif remaining.contains_three_of_a_kind_and_two_others(3):
;                if self.gene[17] == 0:
;                    return remaining.get_most_valuable_single_die()
;                if self.gene[17] == 1:
;                    return (3,3,3)
;                if self.gene[17] == 2:
;                    return remaining.get_most_valuable_set_aside()
;            elif remaining.contains_three_of_a_kind_and_two_others(4):
;                if self.gene[18] == 0:
;                    return remaining.get_most_valuable_single_die()
;                if self.gene[18] == 1:
;                    return (4,4,4)
;                if self.gene[18] == 2:
;                    return remaining.get_most_valuable_set_aside()
;            elif remaining.contains_three_of_a_kind_and_two_others(5):
;                if self.gene[19] == 0:
;                    return remaining.get_most_valuable_single_die()
;                if self.gene[19] == 1:
;                    return (5,5,5)
;                if self.gene[19] == 2:
;                    return remaining.get_most_valuable_set_aside()
;            elif remaining.contains_three_of_a_kind_and_two_others(6):
;                if self.gene[20] == 0:
;                    return remaining.get_most_valuable_single_die()
;                if self.gene[20] == 1:
;                    return (6,6,6)
;                if self.gene[20] == 2:
;                    return remaining.get_most_valuable_set_aside()
;
;            if remaining.contains_three_of_a_kind_and_one_other(1):
;                if self.gene[21] == 0:
;                    return remaining.get_most_valuable_single_die()
;                if self.gene[21] == 1:
;                    return (1,1,1)
;                if self.gene[21] == 2:
;                    return remaining.get_most_valuable_set_aside()
;            elif remaining.contains_three_of_a_kind_and_one_other(2):
;                if self.gene[22] == 0:
;                    return remaining.get_most_valuable_single_die()
;                if self.gene[22] == 1:
;                    return (2,2,2)
;                if self.gene[22] == 2:
;                    return remaining.get_most_valuable_set_aside()
;            elif remaining.contains_three_of_a_kind_and_one_other(3):
;                if self.gene[23] == 0:
;                    return remaining.get_most_valuable_single_die()
;                if self.gene[23] == 1:
;                    return (3,3,3)
;                if self.gene[23] == 2:
;                    return remaining.get_most_valuable_set_aside()
;            elif remaining.contains_three_of_a_kind_and_one_other(4):
;                if self.gene[24] == 0:
;                    return remaining.get_most_valuable_single_die()
;                if self.gene[24] == 1:
;                    return (4,4,4)
;                if self.gene[24] == 2:
;                    return remaining.get_most_valuable_set_aside()
;            elif remaining.contains_three_of_a_kind_and_one_other(5):
;                if self.gene[25] == 0:
;                    return remaining.get_most_valuable_single_die()
;                if self.gene[25] == 1:
;                    return (5,5,5)
;                if self.gene[25] == 2:
;                    return remaining.get_most_valuable_set_aside()
;            elif remaining.contains_three_of_a_kind_and_one_other(6):
;                if self.gene[26] == 0:
;                    return remaining.get_most_valuable_single_die()
;                if self.gene[26] == 1:
;                    return (6,6,6)
;                if self.gene[26] == 2:
;                    return remaining.get_most_valuable_set_aside()
;
;            elif remaining.get_counts()[1] == 2:
;                if self.gene[27] == 0: return (1,)
;                if self.gene[27] == 1: return (1,1)
;            elif remaining.get_counts()[5] == 2:
;                if self.gene[28] == 0: return (5,)
;                if self.gene[28] == 1: return (5,5)
;            elif remaining.get_counts()[1] == 1 and remaining.get_counts()[5] == 1:
;                if self.gene[29] == 0: return (1,)
;                if self.gene[29] == 1: return (1,5)
;            
;
;  (query_stop [this remaining set-aside turn-score total-scores]
;    (let [die-count (count remaining)]
;      (cond
;       (= die-count 1) (>= turn-score (nth gene 30))
;       (= die-count 2) (>= turn-score (nth gene 31))
;       (= die-count 3) (>= turn-score (nth gene 32))
;       (= die-count 4) (>= turn-score (nth gene 33))
;       (= die-count 5) (>= turn-score (nth gene 34))
;       (= die-count 6) (>= turn-score (nth gene 35))
;       :else true)))
;       
;  (warn-invalid-set-aside [this]
;    nil)
;
;  (warn-farkle [this roll]
;    pass)
;  )



    



(deftype GreedyAIPlayer [name stop-threshold]
  FarklePlayer
  (get-name [this]
    name)
  (query-set-aside [this remaining set-aside turn-score total-scores]
    (println "AI player rolled" remaining)
    (if (and (= (count remaining) 6)
	     (> (get-score remaining) 1000))
      remaining
      (let [freqs (frequencies remaining)]
	(filter #(or (= (freqs %) 3)
		     (= % 1)
		     (= % 5))
		remaining))))

  (query-stop [this remaining set-aside turn-score total-scores]
    (> turn-score stop-threshold))
    
  (warn-invalid-set-aside [this]
    nil)

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
    (let [choices (read-line)]
      (map #(Integer/parseInt %) (re-split #" " choices))))

  (query-stop [this remaining set-aside turn-score total-scores]
    (println
     (format
      "You have %d points.  Hit enter to continue rolling, or type 'stop' to end your turn."
      turn-score))
    (let [choice (read-line)]
      (if (= choice "")
	true
	false)))

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
    (if (is-valid-set-aside new-set-aside)
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
	(if (query-stop player remaining set-aside turn-score total-scores)
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
	    updated-score (take-turn player (take (count players)
						  (vec
						   (map val scores))))]
	(if (>= updated-score 10000)
	  (println (get-name player) "is the winner!")
	  (recur (rest rotation)
		 (assoc scores player updated-score)))))))



(defn -main [& args]
  (let [winner (play-farkle [(GreedyAIPlayer. "David" 600)
			     (GreedyAIPlayer. "Samuel" 1000)])]
    (println "The winner is" (get-name winner) "!")))







  
	

(run-tests)
