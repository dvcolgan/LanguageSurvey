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

(deftest test-third
  (is (= 1 (third [3 2 1])))
  (is (= nil (third [3 2])))
  (is (= 1 (third [3 2 1 0])))
  )

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

(deftest test-have-straight
  (is (have-straight? [1 2 3 4 5 6]))
  (is (have-straight? [2 1 4 3 6 5]))
  )

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

(deftest test-is-valid-set-aside
  (is (= (is-valid-set-aside [5 1 1 5] [5 1 1 5]) true))
  (is (= (is-valid-set-aside [1 4 5 1 1 5] [4 5 1 1 5]) false))
  )

(deftest test-contains-one-scoring-die
  (is (= (contains-one-scoring-die [1 2 3 2 4 6]) true))
  (is (= (contains-one-scoring-die [1 1 3 2 4 6]) false))
  (is (= (contains-one-scoring-die [5 3 2 4 6]) true))
  (is (= (contains-one-scoring-die [1 5 3 2 4 6]) false))
  (is (= (contains-one-scoring-die [5 5 3 2 4 6]) false))
  (is (= (contains-one-scoring-die [3 3 3 1 4 6]) false))
  )

(deftest test-contains-only-three-of-a-kind
  (is (= (contains-only-three-of-a-kind [1 1 1 3 2 4]) true))
  (is (= (contains-only-three-of-a-kind [1 1 1 1 2 4]) false))
  (is (= (contains-only-three-of-a-kind [1 3 3 3 2 4]) false))
  (is (= (contains-only-three-of-a-kind [2 5 5 5 2 4]) true))
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

(deftest test-roll-dice
  (is (every? #(<= 1 % 6) (roll-dice 1000))))
