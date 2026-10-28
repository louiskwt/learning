(define (over-or-under num1 num2) 
  (cond 
    ((< num1 num2) -1)
    ((= num1 num2) 0)
    (else 1)
  )
)

(define (composed f g) 
  (define (cf x) 
    (f (g x))
  )
  cf
)

(define (repeat f n)
  (lambda (x) 
      (define repeater (composed f f))
      (cond 
        ((= n 0) x)
        ((= n 1) (f x))
        (else (begin 
          (define x (repeater x))
          ((repeat f (- n 2)) x)
        ))
      )
  )
)

(define (max a b)
  (if (> a b)
      a
      b))

(define (min a b)
  (if (> a b)
      b
      a))

(define (gcd a b) 
  (define min_val (min a b))
  (define max_val (max a b))
  (cond
    ((zero? (modulo a b)) min_val)
    (else (gcd min_val (modulo max_val min_val)))
  )
)


(define (exp b n)
  (define (helper n so-far) 
    (cond 
      ((zero? n) so-far)
      ((= n 1) (* b so-far))
      (else 
        (define updated-so-far (* b so-far))
        (helper (- n 1) updated-so-far)
      )
    )
  )
  (helper n 1))

(define (swap s)
  (define (helper remaining acc)
    (cond
      ((null? remaining) acc)
      ((null? (cdr remaining)) (append acc (list (car remaining))))
      (else
        (if (null? acc)
          (define new-acc (list (car (cdr remaining)) (car remaining)))
          (define new-acc (append acc (list (car (cdr remaining)) (car remaining)))) 
        )
        (helper (cdr (cdr remaining)) new-acc)
      )
    )
  )
  (helper s ())
)

(define (make-adder num) 
  (lambda (inc) (+ num inc))
)
