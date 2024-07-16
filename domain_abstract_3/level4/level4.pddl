(define (problem level4)
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
        baba_word_1 - word_instance
        grass_word_1 - word_instance
        is_word_1 - word_instance
        is_word_2 - word_instance
        is_word_3 - word_instance
        is_word_4 - word_instance
        win_word_1 - word_instance
        win_word_2 - word_instance
        flag_word_1 - word_instance
        love_word_1 - word_instance
        you_word_1 - word_instance
        you_word_2 - word_instance
        baba_obj_1 - object_instance
        grass_obj_1 - object_instance
        flag_obj_1 - object_instance
        love_obj_1 - object_instance
        you - word
        baba - word
        grass - word
        win - word
        love - word
        is - word
        flag - word
        horizontal - orientation
        vertical - orientation
    )

    (:init

         ;; Initial locations for entities
        (at baba_word_1 loc-1-8)
        (at grass_word_1 loc-1-1)
        (at is_word_1 loc-2-8)
        (at is_word_2 loc-2-1)
        (at is_word_3 loc-7-8)
        (at is_word_4 loc-7-1)
        (at win_word_1 loc-3-8)
        (at win_word_2 loc-3-1)
        (at flag_word_1 loc-6-8)
        (at love_word_1 loc-6-1)
        (at you_word_1 loc-8-8)
        (at you_word_2 loc-8-1)
        (at baba_obj_1 loc-2-6)
        (at grass_obj_1 loc-2-3)
        (at flag_obj_1 loc-7-6)
        (at love_obj_1 loc-7-3)

         ; formed rules

        (rule_formed love is you)
        (rule_formed baba is win)
        (rule_formed grass is win)
        (rule_formed flag is you)

         ; control rules

        (control_rule love_obj_1 is you)
        (control_rule flag_obj_1 is you)

         ; fully granular rules (commented)

        ; (rule_formed grass_word_1 is_word_2 win_word_2)
        ; (rule_formed baba_word_1 is_word_1 win_word_1)
        ; (rule_formed love_word_1 is_word_4 you_word_2)
        ; (rule_formed flag_word_1 is_word_3 you_word_1)

    )

    (:goal (and
        ; Specify your goal here
        (overlapping flag_obj_1 baba_obj_1)
         ))

    (:goal (and
        ; Specify your goal here
        (overlapping flag_obj_1 grass_obj_1)
         ))

    (:goal (and
        ; Specify your goal here
        (overlapping love_obj_1 grass_obj_1)
         ))

    (:goal (and
        ; Specify your goal here
        (overlapping love_obj_1 baba_obj_1)
         ))
)
