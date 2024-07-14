(define (problem level4)
    (:domain baba0)

    (:objects
        baba
        flag
        grass
        love
        
        is
        you
        win
    )

    (:init

        ; Formed rules
        (rule_formed baba is win)  
        (rule_formed grass is win)
        (rule_formed flag is you)
        (rule_formed love is you)      

    )

    (:goal (and
        ; Specify your goal here
        (overlapping flag baba)
         ))

    (:goal (and
        ; Specify your goal here
        (overlapping love grass)
         ))

    (:goal (and
        ; Specify your goal here
        (overlapping flag grass)
         ))

    (:goal (and
        ; Specify your goal here
        (overlapping love baba)
         ))
)
