(define (problem level1)
    (:domain baba0)

    (:objects
        baba
        flag
        is
        you
    )

    (:init

        ; Formed rules
        (rule_formed baba is you)        

    )

    (:goal (and
        ; Specify your goal here
        (overlapping baba flag)
         ))
)
