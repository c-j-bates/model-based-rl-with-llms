(define (problem level2)
    (:domain baba0)

    (:objects
        baba
        flag
        
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
        (rule_formed flag is win)
        (overlapping baba flag)
         ))
)
