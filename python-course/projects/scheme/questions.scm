(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cadar x) (car (cdr (car x))))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

;; Problem 14
;; Returns a list of two-element lists
(define (enumerate s)
  ; BEGIN PROBLEM 14
  (define (enumerate-helper i e) 
    (if (null? e) '() 
      (append (list (list i (car e))) (enumerate-helper (+ i 1) (cdr e)))
    )
  )
  (enumerate-helper 0 s)
  ; END PROBLEM 14
)

;; Problem 15

;; Return the value for a key in a dictionary list
(define (get dict key)
  ; BEGIN PROBLEM 15
  (if (null? dict) #f
      (if (equal? (caar dict) key) (cadar dict) (get (cdr dict) key))
  )
  ; END PROBLEM 15
)

;; Return a dictionary list with a (key value) pair
(define (set dict key val)
  ; BEGIN PROBLEM 15
  (define dict-list '())
  (if (not (get dict key)) (append dict (list (list key val))) 
    (if (equal? (caar dict) key) (append dict-list (list (list key val)) (cdr dict))
        (append (list (car dict)) (set (cdr dict) key val))
    )
  )
  ; END PROBLEM 15
)

;; Problem 16

;; implement solution-code
(define (solution-code problem solution)
  ; BEGIN PROBLEM 16
  (define p-list '())
  (if (null? problem) p-list
    (if (list? (car problem)) (append p-list (list (solution-code (car problem) solution)) (solution-code (cdr problem) solution))
      (if (equal? (car problem) '_____) (append p-list (list solution))
        (append p-list (list (car problem)) (solution-code (cdr problem) solution))
      )
    )
  )
)
