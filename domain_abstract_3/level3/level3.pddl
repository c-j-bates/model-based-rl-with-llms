(define (problem level3)
    (:domain baba)

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
        is_word_1 - word_instance
        is_word_2 - word_instance
        win_word_1 - word_instance
        baba_word_1 - word_instance
        you_word_1 - word_instance
        baba_obj_1 - object_instance
        horizontal - orientation
        vertical - orientation
        baba - word
        is - word
        you - word
        win - word
    )

    (:init

         ;; Initial locations for entities
        (at is_word_1 loc-2-5)
        (at is_word_2 loc-5-7)
        (at win_word_1 loc-2-4)
        (at baba_word_1 loc-4-7)
        (at you_word_1 loc-6-7)
        (at baba_obj_1 loc-5-4)

        ; manual for now
        (control_rule baba_obj_1 is you)

    )

    (:goal (and
        ; Specify your goal here
        (rule_formed baba is win)
         ))
)
