(define (problem level5)
    (:domain domain_abstract)

    (:objects
        loc-0-0 - location
        loc-0-1 - location
        loc-0-2 - location
        loc-0-3 - location
        loc-0-4 - location
        loc-0-5 - location
        loc-0-6 - location
        loc-0-7 - location
        loc-0-8 - location
        loc-0-9 - location
        loc-1-0 - location
        loc-1-1 - location
        loc-1-2 - location
        loc-1-3 - location
        loc-1-4 - location
        loc-1-5 - location
        loc-1-6 - location
        loc-1-7 - location
        loc-1-8 - location
        loc-1-9 - location
        loc-2-0 - location
        loc-2-1 - location
        loc-2-2 - location
        loc-2-3 - location
        loc-2-4 - location
        loc-2-5 - location
        loc-2-6 - location
        loc-2-7 - location
        loc-2-8 - location
        loc-2-9 - location
        loc-3-0 - location
        loc-3-1 - location
        loc-3-2 - location
        loc-3-3 - location
        loc-3-4 - location
        loc-3-5 - location
        loc-3-6 - location
        loc-3-7 - location
        loc-3-8 - location
        loc-3-9 - location
        loc-4-0 - location
        loc-4-1 - location
        loc-4-2 - location
        loc-4-3 - location
        loc-4-4 - location
        loc-4-5 - location
        loc-4-6 - location
        loc-4-7 - location
        loc-4-8 - location
        loc-4-9 - location
        loc-5-0 - location
        loc-5-1 - location
        loc-5-2 - location
        loc-5-3 - location
        loc-5-4 - location
        loc-5-5 - location
        loc-5-6 - location
        loc-5-7 - location
        loc-5-8 - location
        loc-5-9 - location
        loc-6-0 - location
        loc-6-1 - location
        loc-6-2 - location
        loc-6-3 - location
        loc-6-4 - location
        loc-6-5 - location
        loc-6-6 - location
        loc-6-7 - location
        loc-6-8 - location
        loc-6-9 - location
        loc-7-0 - location
        loc-7-1 - location
        loc-7-2 - location
        loc-7-3 - location
        loc-7-4 - location
        loc-7-5 - location
        loc-7-6 - location
        loc-7-7 - location
        loc-7-8 - location
        loc-7-9 - location
        loc-8-0 - location
        loc-8-1 - location
        loc-8-2 - location
        loc-8-3 - location
        loc-8-4 - location
        loc-8-5 - location
        loc-8-6 - location
        loc-8-7 - location
        loc-8-8 - location
        loc-8-9 - location
        loc-9-0 - location
        loc-9-1 - location
        loc-9-2 - location
        loc-9-3 - location
        loc-9-4 - location
        loc-9-5 - location
        loc-9-6 - location
        loc-9-7 - location
        loc-9-8 - location
        loc-9-9 - location

        baba_word - word
        flag_word_1 - word
        flag_word_2 - word
        rock_word - word

        baba_obj - object
        flag_obj - object
        rock_obj - object
    
        is_word_1 - word
        is_word_2 - word
        is_word_3 - word

        you_word - word

        win_word - word

        horizontal - orientation
        vertical - orientation
    )

    (:init

        ; formed rules
        (rule_formed baba_word is_word_1 you_word)
        (rule_formed flag_word_1 is_word_2 win_word)
        (not (rule_formed rock_word is_word_3 flag_word_2))
        (valid_rule rock_word is_word_3 flag_word_2)

        ; needs to form rule_formed rock_word is_word_3 flag_word_2

        (is-controllable baba_obj)
        ; (is-controllable flag_obj)

         ;; Initial locations for words forming rules
        (at baba_word loc-1-8)
        (at flag_word_1 loc-6-8)
        (at flag_word_2 loc-8-1)
        (at rock_word loc-4-3)

        (at baba_obj loc-2-5)
        (at flag_obj loc-7-5)
        (at rock_obj loc-7-5)

        (at is_word_1 loc-2-8)
        (at is_word_2 loc-7-8)
        (at is_word_3 loc-7-1)

        (at you_word loc-3-8)

        (at win_word loc-8-8)

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
        ; (unoccupied loc-1-8)
        (unoccupied loc-1-9)

        (unoccupied loc-2-0) 
        (unoccupied loc-2-1) 
        (unoccupied loc-2-2) 
        (unoccupied loc-2-3)
        (unoccupied loc-2-4)
        ; (unoccupied loc-2-5)
        (unoccupied loc-2-6) 
        (unoccupied loc-2-7)     
        ; (unoccupied loc-2-8)
        (unoccupied loc-2-9)

        (unoccupied loc-3-0) 
        (unoccupied loc-3-1) 
        (unoccupied loc-3-2) 
        (unoccupied loc-3-3) 
        (unoccupied loc-3-4)
        (unoccupied loc-3-5) 
        (unoccupied loc-3-6) 
        (unoccupied loc-3-7) 
        ; (unoccupied loc-3-8)
        (unoccupied loc-3-9)

        (unoccupied loc-4-0) 
        (unoccupied loc-4-1) 
        (unoccupied loc-4-2) 
        ; (unoccupied loc-4-3) 
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
        (unoccupied loc-6-5)         
        (unoccupied loc-6-6) 
        (unoccupied loc-6-7)
        ; (unoccupied loc-6-8) 
        (unoccupied loc-6-9)

        (unoccupied loc-7-0) 
        ; (unoccupied loc-7-1) 
        (unoccupied loc-7-2) 
        (unoccupied loc-7-3) 
        (unoccupied loc-7-4)
        ; (unoccupied loc-7-5) 
        (unoccupied loc-7-6) 
        (unoccupied loc-7-7)            
        ; (unoccupied loc-7-8)
        (unoccupied loc-7-9)

        (unoccupied loc-8-0) 
        ; (unoccupied loc-8-1) 
        (unoccupied loc-8-2) 
        (unoccupied loc-8-3) 
        (unoccupied loc-8-4)
        (unoccupied loc-8-5) 
        (unoccupied loc-8-6) 
        (unoccupied loc-8-7)           
        ; (unoccupied loc-8-8)
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
    

        ; define adjacencies so form_rule can work
        ; define adjacencies so form_rule can work
        ;; Adjacencies for the first row
        (adjacent loc-0-0 loc-0-1 vertical)
        (adjacent loc-0-0 loc-1-0 horizontal)
        (adjacent loc-0-1 loc-0-0 vertical)
        (adjacent loc-0-1 loc-0-2 vertical)
        (adjacent loc-0-1 loc-1-1 horizontal)
        (adjacent loc-0-2 loc-0-1 vertical)
        (adjacent loc-0-2 loc-0-3 vertical)
        (adjacent loc-0-2 loc-1-2 horizontal)
        (adjacent loc-0-3 loc-0-2 vertical)
        (adjacent loc-0-3 loc-0-4 vertical)
        (adjacent loc-0-3 loc-1-3 horizontal)
        (adjacent loc-0-4 loc-0-3 vertical)
        (adjacent loc-0-4 loc-0-5 vertical)
        (adjacent loc-0-4 loc-1-4 horizontal)
        (adjacent loc-0-5 loc-0-4 vertical)
        (adjacent loc-0-5 loc-0-6 vertical)
        (adjacent loc-0-5 loc-1-5 horizontal)
        (adjacent loc-0-6 loc-0-5 vertical)
        (adjacent loc-0-6 loc-0-7 vertical)
        (adjacent loc-0-6 loc-1-6 horizontal)
        (adjacent loc-0-7 loc-0-6 vertical)
        (adjacent loc-0-7 loc-0-8 vertical)
        (adjacent loc-0-7 loc-1-7 horizontal)
        (adjacent loc-0-8 loc-0-7 vertical)
        (adjacent loc-0-8 loc-0-9 vertical)
        (adjacent loc-0-8 loc-1-8 horizontal)
        (adjacent loc-0-9 loc-0-8 vertical)
        (adjacent loc-0-9 loc-1-9 horizontal)

        ;; Adjacencies for the second row
        (adjacent loc-1-0 loc-0-0 horizontal)
        (adjacent loc-1-0 loc-1-1 vertical)
        (adjacent loc-1-0 loc-2-0 horizontal)
        (adjacent loc-1-1 loc-0-1 horizontal)
        (adjacent loc-1-1 loc-1-0 vertical)
        (adjacent loc-1-1 loc-1-2 vertical)
        (adjacent loc-1-1 loc-2-1 horizontal)
        (adjacent loc-1-2 loc-0-2 horizontal)
        (adjacent loc-1-2 loc-1-1 vertical)
        (adjacent loc-1-2 loc-1-3 vertical)
        (adjacent loc-1-2 loc-2-2 horizontal)
        (adjacent loc-1-3 loc-0-3 horizontal)
        (adjacent loc-1-3 loc-1-2 vertical)
        (adjacent loc-1-3 loc-1-4 vertical)
        (adjacent loc-1-3 loc-2-3 horizontal)
        (adjacent loc-1-4 loc-0-4 horizontal)
        (adjacent loc-1-4 loc-1-3 vertical)
        (adjacent loc-1-4 loc-1-5 vertical)
        (adjacent loc-1-4 loc-2-4 horizontal)
        (adjacent loc-1-5 loc-0-5 horizontal)
        (adjacent loc-1-5 loc-1-4 vertical)
        (adjacent loc-1-5 loc-1-6 vertical)
        (adjacent loc-1-5 loc-2-5 horizontal)
        (adjacent loc-1-6 loc-0-6 horizontal)
        (adjacent loc-1-6 loc-1-5 vertical)
        (adjacent loc-1-6 loc-1-7 vertical)
        (adjacent loc-1-6 loc-2-6 horizontal)
        (adjacent loc-1-7 loc-0-7 horizontal)
        (adjacent loc-1-7 loc-1-6 vertical)
        (adjacent loc-1-7 loc-1-8 vertical)
        (adjacent loc-1-7 loc-2-7 horizontal)
        (adjacent loc-1-8 loc-0-8 horizontal)
        (adjacent loc-1-8 loc-1-7 vertical)
        (adjacent loc-1-8 loc-1-9 vertical)
        (adjacent loc-1-8 loc-2-8 horizontal)
        (adjacent loc-1-9 loc-0-9 horizontal)
        (adjacent loc-1-9 loc-1-8 vertical)
        (adjacent loc-1-9 loc-2-9 horizontal)

        ;; Adjacencies for the third row
        (adjacent loc-2-0 loc-1-0 horizontal)
        (adjacent loc-2-0 loc-2-1 vertical)
        (adjacent loc-2-0 loc-3-0 horizontal)
        (adjacent loc-2-1 loc-1-1 horizontal)
        (adjacent loc-2-1 loc-2-0 vertical)
        (adjacent loc-2-1 loc-2-2 vertical)
        (adjacent loc-2-1 loc-3-1 horizontal)
        (adjacent loc-2-2 loc-1-2 horizontal)
        (adjacent loc-2-2 loc-2-1 vertical)
        (adjacent loc-2-2 loc-2-3 vertical)
        (adjacent loc-2-2 loc-3-2 horizontal)
        (adjacent loc-2-3 loc-1-3 horizontal)
        (adjacent loc-2-3 loc-2-2 vertical)
        (adjacent loc-2-3 loc-2-4 vertical)
        (adjacent loc-2-3 loc-3-3 horizontal)
        (adjacent loc-2-4 loc-1-4 horizontal)
        (adjacent loc-2-4 loc-2-3 vertical)
        (adjacent loc-2-4 loc-2-5 vertical)
        (adjacent loc-2-4 loc-3-4 horizontal)
        (adjacent loc-2-5 loc-1-5 horizontal)
        (adjacent loc-2-5 loc-2-4 vertical)
        (adjacent loc-2-5 loc-2-6 vertical)
        (adjacent loc-2-5 loc-3-5 horizontal)
        (adjacent loc-2-6 loc-1-6 horizontal)
        (adjacent loc-2-6 loc-2-5 vertical)
        (adjacent loc-2-6 loc-2-7 vertical)
        (adjacent loc-2-6 loc-3-6 horizontal)
        (adjacent loc-2-7 loc-1-7 horizontal)
        (adjacent loc-2-7 loc-2-6 vertical)
        (adjacent loc-2-7 loc-2-8 vertical)
        (adjacent loc-2-7 loc-3-7 horizontal)
        (adjacent loc-2-8 loc-1-8 horizontal)
        (adjacent loc-2-8 loc-2-7 vertical)
        (adjacent loc-2-8 loc-2-9 vertical)
        (adjacent loc-2-8 loc-3-8 horizontal)
        (adjacent loc-2-9 loc-1-9 horizontal)
        (adjacent loc-2-9 loc-2-8 vertical)
        (adjacent loc-2-9 loc-3-9 horizontal)

        ;; Adjacencies for the fourth row
        (adjacent loc-3-0 loc-2-0 horizontal)
        (adjacent loc-3-0 loc-3-1 vertical)
        (adjacent loc-3-0 loc-4-0 horizontal)
        (adjacent loc-3-1 loc-2-1 horizontal)
        (adjacent loc-3-1 loc-3-0 vertical)
        (adjacent loc-3-1 loc-3-2 vertical)
        (adjacent loc-3-1 loc-4-1 horizontal)
        (adjacent loc-3-2 loc-2-2 horizontal)
        (adjacent loc-3-2 loc-3-1 vertical)
        (adjacent loc-3-2 loc-3-3 vertical)
        (adjacent loc-3-2 loc-4-2 horizontal)
        (adjacent loc-3-3 loc-2-3 horizontal)
        (adjacent loc-3-3 loc-3-2 vertical)
        (adjacent loc-3-3 loc-3-4 vertical)
        (adjacent loc-3-3 loc-4-3 horizontal)
        (adjacent loc-3-4 loc-2-4 horizontal)
        (adjacent loc-3-4 loc-3-3 vertical)
        (adjacent loc-3-4 loc-3-5 vertical)
        (adjacent loc-3-4 loc-4-4 horizontal)
        (adjacent loc-3-5 loc-2-5 horizontal)
        (adjacent loc-3-5 loc-3-4 vertical)
        (adjacent loc-3-5 loc-3-6 vertical)
        (adjacent loc-3-5 loc-4-5 horizontal)
        (adjacent loc-3-6 loc-2-6 horizontal)
        (adjacent loc-3-6 loc-3-5 vertical)
        (adjacent loc-3-6 loc-3-7 vertical)
        (adjacent loc-3-6 loc-4-6 horizontal)
        (adjacent loc-3-7 loc-2-7 horizontal)
        (adjacent loc-3-7 loc-3-6 vertical)
        (adjacent loc-3-7 loc-3-8 vertical)
        (adjacent loc-3-7 loc-4-7 horizontal)
        (adjacent loc-3-8 loc-2-8 horizontal)
        (adjacent loc-3-8 loc-3-7 vertical)
        (adjacent loc-3-8 loc-3-9 vertical)
        (adjacent loc-3-8 loc-4-8 horizontal)
        (adjacent loc-3-9 loc-2-9 horizontal)
        (adjacent loc-3-9 loc-3-8 vertical)
        (adjacent loc-3-9 loc-4-9 horizontal)

        ;; Adjacencies for the fifth row
        (adjacent loc-4-0 loc-3-0 horizontal)
        (adjacent loc-4-0 loc-4-1 vertical)
        (adjacent loc-4-0 loc-5-0 horizontal)
        (adjacent loc-4-1 loc-3-1 horizontal)
        (adjacent loc-4-1 loc-4-0 vertical)
        (adjacent loc-4-1 loc-4-2 vertical)
        (adjacent loc-4-1 loc-5-1 horizontal)
        (adjacent loc-4-2 loc-3-2 horizontal)
        (adjacent loc-4-2 loc-4-1 vertical)
        (adjacent loc-4-2 loc-4-3 vertical)
        (adjacent loc-4-2 loc-5-2 horizontal)
        (adjacent loc-4-3 loc-3-3 horizontal)
        (adjacent loc-4-3 loc-4-2 vertical)
        (adjacent loc-4-3 loc-4-4 vertical)
        (adjacent loc-4-3 loc-5-3 horizontal)
        (adjacent loc-4-4 loc-3-4 horizontal)
        (adjacent loc-4-4 loc-4-3 vertical)
        (adjacent loc-4-4 loc-4-5 vertical)
        (adjacent loc-4-4 loc-5-4 horizontal)
        (adjacent loc-4-5 loc-3-5 horizontal)
        (adjacent loc-4-5 loc-4-4 vertical)
        (adjacent loc-4-5 loc-4-6 vertical)
        (adjacent loc-4-5 loc-5-5 horizontal)
        (adjacent loc-4-6 loc-3-6 horizontal)
        (adjacent loc-4-6 loc-4-5 vertical)
        (adjacent loc-4-6 loc-4-7 vertical)
        (adjacent loc-4-6 loc-5-6 horizontal)
        (adjacent loc-4-7 loc-3-7 horizontal)
        (adjacent loc-4-7 loc-4-6 vertical)
        (adjacent loc-4-7 loc-4-8 vertical)
        (adjacent loc-4-7 loc-5-7 horizontal)
        (adjacent loc-4-8 loc-3-8 horizontal)
        (adjacent loc-4-8 loc-4-7 vertical)
        (adjacent loc-4-8 loc-4-9 vertical)
        (adjacent loc-4-8 loc-5-8 horizontal)
        (adjacent loc-4-9 loc-3-9 horizontal)
        (adjacent loc-4-9 loc-4-8 vertical)
        (adjacent loc-4-9 loc-5-9 horizontal)

        ;; Adjacencies for the sixth row
        (adjacent loc-5-0 loc-4-0 horizontal)
        (adjacent loc-5-0 loc-5-1 vertical)
        (adjacent loc-5-0 loc-6-0 horizontal)
        (adjacent loc-5-1 loc-4-1 horizontal)
        (adjacent loc-5-1 loc-5-0 vertical)
        (adjacent loc-5-1 loc-5-2 vertical)
        (adjacent loc-5-1 loc-6-1 horizontal)
        (adjacent loc-5-2 loc-4-2 horizontal)
        (adjacent loc-5-2 loc-5-1 vertical)
        (adjacent loc-5-2 loc-5-3 vertical)
        (adjacent loc-5-2 loc-6-2 horizontal)
        (adjacent loc-5-3 loc-4-3 horizontal)
        (adjacent loc-5-3 loc-5-2 vertical)
        (adjacent loc-5-3 loc-5-4 vertical)
        (adjacent loc-5-3 loc-6-3 horizontal)
        (adjacent loc-5-4 loc-4-4 horizontal)
        (adjacent loc-5-4 loc-5-3 vertical)
        (adjacent loc-5-4 loc-5-5 vertical)
        (adjacent loc-5-4 loc-6-4 horizontal)
        (adjacent loc-5-5 loc-4-5 horizontal)
        (adjacent loc-5-5 loc-5-4 vertical)
        (adjacent loc-5-5 loc-5-6 vertical)
        (adjacent loc-5-5 loc-6-5 horizontal)
        (adjacent loc-5-6 loc-4-6 horizontal)
        (adjacent loc-5-6 loc-5-5 vertical)
        (adjacent loc-5-6 loc-5-7 vertical)
        (adjacent loc-5-6 loc-6-6 horizontal)
        (adjacent loc-5-7 loc-4-7 horizontal)
        (adjacent loc-5-7 loc-5-6 vertical)
        (adjacent loc-5-7 loc-5-8 vertical)
        (adjacent loc-5-7 loc-6-7 horizontal)
        (adjacent loc-5-8 loc-4-8 horizontal)
        (adjacent loc-5-8 loc-5-7 vertical)
        (adjacent loc-5-8 loc-5-9 vertical)
        (adjacent loc-5-8 loc-6-8 horizontal)
        (adjacent loc-5-9 loc-4-9 horizontal)
        (adjacent loc-5-9 loc-5-8 vertical)
        (adjacent loc-5-9 loc-6-9 horizontal)

        ;; Adjacencies for the seventh row
        (adjacent loc-6-0 loc-5-0 horizontal)
        (adjacent loc-6-0 loc-6-1 vertical)
        (adjacent loc-6-0 loc-7-0 horizontal)
        (adjacent loc-6-1 loc-5-1 horizontal)
        (adjacent loc-6-1 loc-6-0 vertical)
        (adjacent loc-6-1 loc-6-2 vertical)
        (adjacent loc-6-1 loc-7-1 horizontal)
        (adjacent loc-6-2 loc-5-2 horizontal)
        (adjacent loc-6-2 loc-6-1 vertical)
        (adjacent loc-6-2 loc-6-3 vertical)
        (adjacent loc-6-2 loc-7-2 horizontal)
        (adjacent loc-6-3 loc-5-3 horizontal)
        (adjacent loc-6-3 loc-6-2 vertical)
        (adjacent loc-6-3 loc-6-4 vertical)
        (adjacent loc-6-3 loc-7-3 horizontal)
        (adjacent loc-6-4 loc-5-4 horizontal)
        (adjacent loc-6-4 loc-6-3 vertical)
        (adjacent loc-6-4 loc-6-5 vertical)
        (adjacent loc-6-4 loc-7-4 horizontal)
        (adjacent loc-6-5 loc-5-5 horizontal)
        (adjacent loc-6-5 loc-6-4 vertical)
        (adjacent loc-6-5 loc-6-6 vertical)
        (adjacent loc-6-5 loc-7-5 horizontal)
        (adjacent loc-6-6 loc-5-6 horizontal)
        (adjacent loc-6-6 loc-6-5 vertical)
        (adjacent loc-6-6 loc-6-7 vertical)
        (adjacent loc-6-6 loc-7-6 horizontal)
        (adjacent loc-6-7 loc-5-7 horizontal)
        (adjacent loc-6-7 loc-6-6 vertical)
        (adjacent loc-6-7 loc-6-8 vertical)
        (adjacent loc-6-7 loc-7-7 horizontal)
        (adjacent loc-6-8 loc-5-8 horizontal)
        (adjacent loc-6-8 loc-6-7 vertical)
        (adjacent loc-6-8 loc-6-9 vertical)
        (adjacent loc-6-8 loc-7-8 horizontal)
        (adjacent loc-6-9 loc-5-9 horizontal)
        (adjacent loc-6-9 loc-6-8 vertical)
        (adjacent loc-6-9 loc-7-9 horizontal)

        ;; Adjacencies for the eighth row
        (adjacent loc-7-0 loc-6-0 horizontal)
        (adjacent loc-7-0 loc-7-1 vertical)
        (adjacent loc-7-0 loc-8-0 horizontal)
        (adjacent loc-7-1 loc-6-1 horizontal)
        (adjacent loc-7-1 loc-7-0 vertical)
        (adjacent loc-7-1 loc-7-2 vertical)
        (adjacent loc-7-1 loc-8-1 horizontal)
        (adjacent loc-7-2 loc-6-2 horizontal)
        (adjacent loc-7-2 loc-7-1 vertical)
        (adjacent loc-7-2 loc-7-3 vertical)
        (adjacent loc-7-2 loc-8-2 horizontal)
        (adjacent loc-7-3 loc-6-3 horizontal)
        (adjacent loc-7-3 loc-7-2 vertical)
        (adjacent loc-7-3 loc-7-4 vertical)
        (adjacent loc-7-3 loc-8-3 horizontal)
        (adjacent loc-7-4 loc-6-4 horizontal)
        (adjacent loc-7-4 loc-7-3 vertical)
        (adjacent loc-7-4 loc-7-5 vertical)
        (adjacent loc-7-4 loc-8-4 horizontal)
        (adjacent loc-7-5 loc-6-5 horizontal)
        (adjacent loc-7-5 loc-7-4 vertical)
        (adjacent loc-7-5 loc-7-6 vertical)
        (adjacent loc-7-5 loc-8-5 horizontal)
        (adjacent loc-7-6 loc-6-6 horizontal)
        (adjacent loc-7-6 loc-7-5 vertical)
        (adjacent loc-7-6 loc-7-7 vertical)
        (adjacent loc-7-6 loc-8-6 horizontal)
        (adjacent loc-7-7 loc-6-7 horizontal)
        (adjacent loc-7-7 loc-7-6 vertical)
        (adjacent loc-7-7 loc-7-8 vertical)
        (adjacent loc-7-7 loc-8-7 horizontal)
        (adjacent loc-7-8 loc-6-8 horizontal)
        (adjacent loc-7-8 loc-7-7 vertical)
        (adjacent loc-7-8 loc-7-9 vertical)
        (adjacent loc-7-8 loc-8-8 horizontal)
        (adjacent loc-7-9 loc-6-9 horizontal)
        (adjacent loc-7-9 loc-7-8 vertical)
        (adjacent loc-7-9 loc-8-9 horizontal)

        ;; Adjacencies for the ninth row
        (adjacent loc-8-0 loc-7-0 horizontal)
        (adjacent loc-8-0 loc-8-1 vertical)
        (adjacent loc-8-0 loc-9-0 horizontal)
        (adjacent loc-8-1 loc-7-1 horizontal)
        (adjacent loc-8-1 loc-8-0 vertical)
        (adjacent loc-8-1 loc-8-2 vertical)
        (adjacent loc-8-1 loc-9-1 horizontal)
        (adjacent loc-8-2 loc-7-2 horizontal)
        (adjacent loc-8-2 loc-8-1 vertical)
        (adjacent loc-8-2 loc-8-3 vertical)
        (adjacent loc-8-2 loc-9-2 horizontal)
        (adjacent loc-8-3 loc-7-3 horizontal)
        (adjacent loc-8-3 loc-8-2 vertical)
        (adjacent loc-8-3 loc-8-4 vertical)
        (adjacent loc-8-3 loc-9-3 horizontal)
        (adjacent loc-8-4 loc-7-4 horizontal)
        (adjacent loc-8-4 loc-8-3 vertical)
        (adjacent loc-8-4 loc-8-5 vertical)
        (adjacent loc-8-4 loc-9-4 horizontal)
        (adjacent loc-8-5 loc-7-5 horizontal)
        (adjacent loc-8-5 loc-8-4 vertical)
        (adjacent loc-8-5 loc-8-6 vertical)
        (adjacent loc-8-5 loc-9-5 horizontal)
        (adjacent loc-8-6 loc-7-6 horizontal)
        (adjacent loc-8-6 loc-8-5 vertical)
        (adjacent loc-8-6 loc-8-7 vertical)
        (adjacent loc-8-6 loc-9-6 horizontal)
        (adjacent loc-8-7 loc-7-7 horizontal)
        (adjacent loc-8-7 loc-8-6 vertical)
        (adjacent loc-8-7 loc-8-8 vertical)
        (adjacent loc-8-7 loc-9-7 horizontal)
        (adjacent loc-8-8 loc-7-8 horizontal)
        (adjacent loc-8-8 loc-8-7 vertical)
        (adjacent loc-8-8 loc-8-9 vertical)
        (adjacent loc-8-8 loc-9-8 horizontal)
        (adjacent loc-8-9 loc-7-9 horizontal)
        (adjacent loc-8-9 loc-8-8 vertical)
        (adjacent loc-8-9 loc-9-9 horizontal)

    )


    (:goal (and
        ;; Ensure the rule is formed
        (rule_formed rock_word is_word_3 flag_word_2)
        ;; Ensure baba_obj is at the location of win
        (at baba_obj loc-7-5)
        
    ))
    
)
