(define (problem level2)
    (:domain babadomain)

    (:objects
        loc-0-0 loc-0-1 loc-0-2 loc-0-3 loc-0-4 loc-0-5 loc-0-6 loc-0-7 loc-0-8 loc-0-9
        loc-1-0 loc-1-1 loc-1-2 loc-1-3 loc-1-4 loc-1-5 loc-1-6 loc-1-7 loc-1-8 loc-1-9
        loc-2-0 loc-2-1 loc-2-2 loc-2-3 loc-2-4 loc-2-5 loc-2-6 loc-2-7 loc-2-8 loc-2-9
        loc-3-0 loc-3-1 loc-3-2 loc-3-3 loc-3-4 loc-3-5 loc-3-6 loc-3-7 loc-3-8 loc-3-9
        loc-4-0 loc-4-1 loc-4-2 loc-4-3 loc-4-4 loc-4-5 loc-4-6 loc-4-7 loc-4-8 loc-4-9
        loc-5-0 loc-5-1 loc-5-2 loc-5-3 loc-5-4 loc-5-5 loc-5-6 loc-5-7 loc-5-8 loc-5-9
        loc-6-0 loc-6-1 loc-6-2 loc-6-3 loc-6-4 loc-6-5 loc-6-6 loc-6-7 loc-6-8 loc-6-9
        loc-7-0 loc-7-1 loc-7-2 loc-7-3 loc-7-4 loc-7-5 loc-7-6 loc-7-7 loc-7-8 loc-7-9
        loc-8-0 loc-8-1 loc-8-2 loc-8-3 loc-8-4 loc-8-5 loc-8-6 loc-8-7 loc-8-8 loc-8-9
        loc-9-0 loc-9-1 loc-9-2 loc-9-3 loc-9-4 loc-9-5 loc-9-6 loc-9-7 loc-9-8 loc-9-9
        baba_word is_word_1 is_word_2 you_word win_word flag_word
        baba_obj flag_obj
    )

    (:init
        (rule_formed baba_word is_word_1 you_word)
        (not (rule_formed flag_word is_word_2 win_word))
        ; (not (overlapping baba_obj flag_obj))

        ;; Initial locations for words forming rules
        (at baba_word loc-1-8)
        (at is_word_1 loc-2-8)
        (at you_word loc-3-8)

        (at flag_word loc-6-5)
        (at is_word_2 loc-7-8)
        (at win_word loc-8-8)

        ;; Initial locations for objects
        (at baba_obj loc-2-4)
        (at flag_obj loc-7-4)

        ;; Unoccupied locations
        (unoccupied loc-0-0) 
        (unoccupied loc-0-1) 
        (unoccupied loc-0-2) 
        (unoccupied loc-0-3) 
        (unoccupied loc-0-4)
        (unoccupied loc-0-5) 
        (unoccupied loc-0-6) 
        (unoccupied loc-0-7) 
        (unoccupied loc-0-8) 
        (unoccupied loc-0-9)

        (unoccupied loc-1-0) 
        (unoccupied loc-1-1) 
        (unoccupied loc-1-2) 
        (unoccupied loc-1-3) 
        (unoccupied loc-1-4)
        (unoccupied loc-1-5) 
        (unoccupied loc-1-6) 
        (unoccupied loc-1-7)                      
        (unoccupied loc-1-9)

        (unoccupied loc-2-0) 
        (unoccupied loc-2-1) 
        (unoccupied loc-2-2) 
        (unoccupied loc-2-3)

        (unoccupied loc-2-5) 
        (unoccupied loc-2-6) 
        (unoccupied loc-2-7)     

        (unoccupied loc-2-9)

        (unoccupied loc-3-0) 
        (unoccupied loc-3-1) 
        (unoccupied loc-3-2) 
        (unoccupied loc-3-3) 
        (unoccupied loc-3-4)
        (unoccupied loc-3-5) 
        (unoccupied loc-3-6) 
        (unoccupied loc-3-7) 

        (unoccupied loc-3-9)

        (unoccupied loc-4-0) 
        (unoccupied loc-4-1) 
        (unoccupied loc-4-2) 
        (unoccupied loc-4-3) 
        (unoccupied loc-4-4)
        (unoccupied loc-4-5) 
        (unoccupied loc-4-6) 
        (unoccupied loc-4-7) 
        (unoccupied loc-4-8) 
        (unoccupied loc-4-9)

        (unoccupied loc-5-0) 
        (unoccupied loc-5-1) 
        (unoccupied loc-5-2) 
        (unoccupied loc-5-3) 
        (unoccupied loc-5-4)
        (unoccupied loc-5-5) 
        (unoccupied loc-5-6) 
        (unoccupied loc-5-7) 
        (unoccupied loc-5-8) 
        (unoccupied loc-5-9)

        (unoccupied loc-6-0) 
        (unoccupied loc-6-1) 
        (unoccupied loc-6-2) 
        (unoccupied loc-6-3) 
        (unoccupied loc-6-4)

                             
        (unoccupied loc-6-6) 
        (unoccupied loc-6-7) 
        (unoccupied loc-6-8) 
        (unoccupied loc-6-9)

        (unoccupied loc-7-0) 
        (unoccupied loc-7-1) 
        (unoccupied loc-7-2) 
        (unoccupied loc-7-3) 

        (unoccupied loc-7-5) 
        (unoccupied loc-7-6) 
        (unoccupied loc-7-7)            

        (unoccupied loc-7-9)

        (unoccupied loc-8-0) 
        (unoccupied loc-8-1) 
        (unoccupied loc-8-2) 
        (unoccupied loc-8-3) 
        (unoccupied loc-8-4)
        (unoccupied loc-8-5) 
        (unoccupied loc-8-6) 
        (unoccupied loc-8-7)           

        (unoccupied loc-8-9)

        (unoccupied loc-9-0) 
        (unoccupied loc-9-1) 
        (unoccupied loc-9-2) 
        (unoccupied loc-9-3) 
        (unoccupied loc-9-4)
        (unoccupied loc-9-5) 
        (unoccupied loc-9-6) 
        (unoccupied loc-9-7) 
        (unoccupied loc-9-8) 
        (unoccupied loc-9-9)

        ;; Initial occupied locations
        (not (unoccupied loc-1-8))
        (not (unoccupied loc-2-8))
        (not (unoccupied loc-3-8))

        (not (unoccupied loc-6-5))
        (not (unoccupied loc-7-8))
        (not (unoccupied loc-8-8))

        (not (unoccupied loc-2-4))
        (not (unoccupied loc-7-4))

        ; define adjacencies so form_rule can work
        (adjacent loc-6-8 loc-7-8)
        (adjacent loc-7-8 loc-8-8)
    )

    (:goal (and
        (rule_formed flag_word is_word_2 win_word)
        (at flag_word loc-6-8)
        (at is_word_2 loc-7-8)
        (at win_word loc-8-8)
        (at baba_obj loc-7-4)
    ))
)
