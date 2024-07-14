(define (problem level5)
    (:domain baba0)

    (:objects
        baba
        rock
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
        (rule_formed rock is flag)
        (overlapping baba flag)
         ))

)
