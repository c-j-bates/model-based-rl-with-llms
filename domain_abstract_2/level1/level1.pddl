(define (problem level1)
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
        (rule_formed flag is win)        

    )

    (:goal (and
        ; Specify your goal here
        (overlapping baba flag)
         ))
)
