					;code is data - homoiconic

					;+ - * >= > <= /
					;quot rem
					;Big decimal - append M
(class (* 1000 10000 1000 10000 10000 10000000000))
(.toUpperCase "Hello")
\c ;character
(apply str (interleave "I would like to go to the store"
		       "I like your shoes"))

(apply str (take-nth 2 "II  wloiukled  yloiukre  sthoo egs"))

					;() != false
					;0 != false
					;predicates end in a ? instead of p
(find-doc #"\?$")

(def inventors {"Lisp" "McCarthy"
		"Clojure" "Hickey"
		})
(inventors "Lisp")
(get inventors "aou", "Not found")
(def inventors {:Lisp "McCarthy"
		:Clojure "Hickey"
		})
(:Lisp inventors)

(defstruct book :title :author)

(def b (struct book "A book" "An author"))

					;reader macros change the
					;interpreter's execution, are
					;prefixed by a special
					;character

					;' or quote prevents execution

					;defn - define function
(defn greeting
  "Returns a greeting of the form 'Helo, username.'"
  ([]
     (greeting "world"))
  ([username]
     (str "Hello, " username)))

(defn whole-numbers [] (iterate inc 0))
					;argument after & is bound to
					;the rest

					;fn or just #(body) for
					;anonymous function, %, %1, %2
					;for arguments
(use 'clojure.contrib.str-utils)
(filter #(> (count %) 2) (re-split #"\W+" "A fine day it is"))
;;use anonymous functions whenever it makse the code clear.er

;;variables
(def foo 10)

;;destructuring
(defn greet-author [{fname :first-name}]
  (println "Hello, " fname))
(let [[_ _ z] [1 2 3]]
  z)
(let [[x _ z :as coords] [1 2 3]]
  )

(defn ellipsize [words]
  (let [[w1 w2 w3] (re-split #"\s+" words)]
    (str-join " " [w1 w2 w3 "..."])))

(ellipsize "Hi there everyone how are you")

(defn indexed2 [coll] (map vector (iterate inc 0) coll))
(defn index-filter [pred coll]
  (when pred
    (for [[idx elt] (indexed2 coll) :when (pred elt)] idx)))
(defn index-of-any [pred coll]
  (first (index-filter pred coll)))

;;metadata
(def stu {:name "Stu" :email "stu@thinkrelevance.com"})
(def serializable-stu (with-meta stu {:serializable true}))
(meta serializable-stu)





;;chapter 4
;;sequences are always immutable
(def lst '(1 2 3))
(first lst)
(rest lst)
(cons 1 lst)
(seq lst)
(next lst)
(sorted-set :hi :there :everybody)
(sorted-map :c 3 :b 2 :a 1)
;;conj - insert elements into a seq
;;into - join two seq
;;range - like Python range
;;repeat - repeats argument
;;iterate - lazily applies argument to second argument
;;take - get argument elements
;;cycle - repeat a seq
;;interleave - alternate two lists until one runs out
;;interpose - insert 1st argument between 2nd
;;str-join
;;list, vector, hash-set, hash-map
(take 10 (filter even? (whole-numbers)))
;;take-while get elements from 2nd as long as 1st is true
;;sets act as functions that test membership
;;drop-while
;;split-at, split-with
(split-at 5 (range 10))
(split-with #(<= % 10) (range 0 20 2))
(every? odd? [1 3 5])
(some even? [1 2 3])
(some even? [1 3 5])
(some identity [nil false 1 nil 2])
;;not-every?, not-any?
(map #(format "<p>%s</p>" %) ["the" "quick" "brown" "fox"])
(map #(format "<%s>%s</%s>" %1 %2 %1)
     ["h1" "h2" "h3" "h1"] ["the" "quick" "brown" "fox"])

(reduce + (range 1 11))

(sort > [3 5 1 2 3])
(sort-by str [31 5 11 2 3])

(for [word ["the" "quick" "brown" "fox"]]
  (format "<p>%s</p>" word))

(take 10 (for [n (whole-numbers) :when (even? n)] n)) ;also :while
(for [file "ABDEFGH" rank (range 1 9)] (format "%c%d" file rank))

;;lazy sequences
(use 'clojure.contrib.lazy-seqs)

(def ordinals-and-primes (map vector (iterate inc 1) primes))
(take 10 ordinals-and-primes) ;nice

;;does not print anything because the sequence is lazy:
(def x (for [i (range 1 3)] (do (println i) i)))
(doall x)
(dorun x) ;;does not keep results in memory
;;use these functions sparingly, relate to side effects

;;most Java collections are seq-able
(re-seq #"\w+" "the quick brown fox")
(sort (re-seq #"\w+" "the quick brown fox"))
(drop 2 (re-seq #"\w+" "the quick brown fox"))
(map #(.toUpperCase %) (re-seq #"\w+" "the quick brown fox"))

;;file operations use Java.io
(import '(java.io File))
(defn minutes-to-millis [mins] (* mins 1000 60))
(defn recently-modified? [file]
  (> (.lastModified file)
     (- (System/currentTimeMillis) (minutes-to-millis 30))))

(filter recently-modified? (file-seq (File. ".")))

(use 'clojure.contrib.duck-streams)
(with-open [rdr (reader "src/learning/chapter2.clj")]
  (count (filter #(re-find #"\S" %) (line-seq rdr))))


(defn non-blank? [line] (if (re-find #"\S" line) true false))

(defn non-svn? [file] (not (.contains (.toString file) ".svn")))

(defn non-backup? [file] (and (not (.contains (str file) "~"))
			      (not (.contains (str file) "#"))))

(defn clojure-source? [file] (.endsWith (.toString file) ".clj"))

(defn clojure-loc [base-file]
  (reduce
   +
   (for [file (file-seq base-file)
	 :when (and (clojure-source? file)
		    (non-svn? file)
		    (non-backup? file))]
     (with-open [rdr (reader file)]
       (count (filter non-blank? (line-seq rdr)))))))

(clojure-loc (File. "."))

;;can treat xml like a seq too
;;xml-seq

;;there are some data-structure specific functions for performance, sub-vec

					;(keys map)
					;(vals map)
({:breakfast "good", :lunch "meh", :dinner "wee"} :lunch)
(:lunch {:breakfast "good", :lunch "meh", :dinner "wee"})

;;assoc, dissoc, select keys, merge for maps


;;set operations in clojure.set


;;chapter 5 immutable data structures in Clojure share structure to
;;save space when possible

;;benefits of functional programming:
;;-easier to write because the parameter list is the only state
;;-easier to read because of the same
;;-easier to test because the function needs no environment setup
;;-are completely encapsulated and composable, leading to true reuse

;;Rules of FP in Clojure:
;;don't use direct recursion - no direct tail-call optimization
;;use recur when getting a scalar value back or small finite seqs - this is optimized, but not lazy
;;use lazy sequences when dealing with large amounts of data
;;don't realize too much of a lazy sequence
;;learn the sequence library functions well
;;if you decompose problems into smaller parts, there is usually a function for that

(defn stack-consuming-fibo [n]
  (cond
   (= n 0) 0
   (= n 1) 1
   :else (+ (stack-consuming-fibo (- n 1))
	    (stack-consuming-fibo (- n 2)))))

(stack-consuming-fibo 10)

(defn tail-fibo [n]
  (letfn [(fib
	   [current next n]
	   (if (zero? n)
	     current
	     (fib next (+ current next) (dec n))))]
    (fib 0 1 n)))

(tail-fibo 10)
;;clojure can't do tail call optimization because Java doesn't
;;letfn - create a local function that can call itself

(defn recur-fibo [n]
  (letfn [(fib
	   [current next n]
	   (if (zero? n)
	     current
	     (recur next (+ current next) (dec n))))]
    (fib 0 1 n)))

(recur-fibo 1000000)

(lazy-seq [1 2 3 4])
;;does not evaluate the list, and also memoizes itself

(defn lazy-seq-fibo
  ([]
     (concat [0 1] (lazy-seq-fibo 0 1)))
  ([a b]
     (let [n (+ a b)]
       (lazy-seq
	(cons n (lazy-seq-fibo b n))))))
;;wrap the recursive part with lazy-seq to make it lazy
(rem (nth (lazy-seq-fibo) 200000) 100000000)

;;this function does not seem any faster the second time it is evaluated -- is this not what memoizing it means?

(defn fibo []
  (map first (iterate (fn [[a b]] [b (+ a b)]) [0 1])))

(take 5 (fibo))

(def lots-o-fibs (take 1000000000 (fibo))) ;defining lazily

(set! *print-length* 10) ;make it so that the REPL will not print out all of a lazy seq

;;"You should normally expose lazy sequences as a function that returns the sequence, not as a var that contains the sequence.

(def count-if (comp count filter))

(count-if
 (fn [pair] (every? #(= :h %) pair))
 (partition 2 1 [:h :t :h :h :t :t :h :h :h :h]))

(defn count-runs [n pred coll]
  (count-if #(every? pred %) (partition n 1 coll)))

(def add-3 (partial + 3))

(add-3 4)

(declare my-odd? my-even?) ;;define names without binding for mutual recursion

(defn my-odd? [n]
  (if (= n 0)
    false
    (my-even? (dec n))))

(defn my-even? [n]
  (if (= n 0)
    true
    (my-odd? (dec n))))

;;trampoline can do mutual recursion

;;using laziness prevents the need for stack-breaking recursion

;;how does simply making a function lazy mitigate the need for recursion?


(def current-track (ref "Russian song"))
(def current-composer (ref "Tolstoy"))

(deref current-track)
@current-track

(dosync (ref-set current-track "Other song"))

;;these happen at the same time from other codes' perspective
(dosync
 (ref-set current-track "Other song")
 (ref-set current-composer "Some guy from a zoo"))


(defstruct message :sender :text)

(struct message "stu" "test message")

(def messages (ref ()))

(defn add-message [msg]
  (dosync (alter messages conj msg)))

(add-message (struct message "user 1" "hello"))
(add-message (struct message "user 2" "howdy"))

;;commute, like alter but is faster at the cost of potential reordering of operations, is dangerous, don't use it much

;;refs can take a validation function

(def current-track (atom "a track"))

(reset! current-track "aoeu")
					;swap - update an atom with a function passed

(def counter (agent 0))

@counter

(send counter inc)

(def backup-agent (agent "messages-backup.clj"))


;;create a thread-local variable
(binding [foo 42] foo)

(defn slow-double [n]
  (Thread/sleep 1000)
  (* n 2))

(defn calls-slow-double []
  (map slow-double [1 2 1 2 1 2 1 2]))

(time (dorun (calls-slow-double)))

(defn demo-memoize []
  (time
   (dorun
    (binding [slow-double (memoize slow-double)]
      (calls-slow-double)))))

(demo-memoize)

