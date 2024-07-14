(define (problem level3)
    (:domain baba0)

    (:objects
        baba
        
        is
        you
        win
    )

    (:init

        ; Formed rules
        (rule_formed baba is you)        

    )

    (:goal (and
        ; Specify your goal here
        (rule_formed baba is win)
         ))
)
