(ns farkle.core
  (:use clojure.contrib.str-utils)
  (:use clojure.test clojure.set)
  (:use farkle.game farkle.ga)
  (:gen-class))


(defn -main [& args]
  (let [winner (play-farkle [(GreedyAIPlayer. "David" 600)
			     (GreedyAIPlayer. "Samuel" 1000)])]
    (println "The winner is" (get-name winner) "!")))






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

