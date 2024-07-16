(define (problem lvtest)
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
        flag_word_1 - word_instance
        is_word_1 - word_instance
        is_word_2 - word_instance
        is_word_3 - word_instance
        you_word_1 - word_instance
        win_word_1 - word_instance
        goop_word_1 - word_instance
        sink_word_1 - word_instance
        goop_obj_1 - object_instance
        goop_obj_2 - object_instance
        goop_obj_3 - object_instance
        goop_obj_4 - object_instance
        goop_obj_5 - object_instance
        goop_obj_6 - object_instance
        goop_obj_7 - object_instance
        goop_obj_8 - object_instance
        goop_obj_9 - object_instance
        goop_obj_10 - object_instance
        goop_obj_11 - object_instance
        goop_obj_12 - object_instance
        goop_obj_13 - object_instance
        goop_obj_14 - object_instance
        goop_obj_15 - object_instance
        goop_obj_16 - object_instance
        goop_obj_17 - object_instance
        goop_obj_18 - object_instance
        goop_obj_19 - object_instance
        goop_obj_20 - object_instance
        goop_obj_21 - object_instance
        goop_obj_22 - object_instance
        goop_obj_23 - object_instance
        goop_obj_24 - object_instance
        goop_obj_25 - object_instance
        goop_obj_26 - object_instance
        goop_obj_27 - object_instance
        goop_obj_28 - object_instance
        goop_obj_29 - object_instance
        goop_obj_30 - object_instance
        baba_obj_1 - object_instance
        flag_obj_1 - object_instance
        is - word
        win - word
        goop - word
        sink - word
        flag - word
        you - word
        baba - word
        horizontal - orientation
        vertical - orientation
    )

    (:init

         ;; Initial locations for entities
        (at baba_word_1 loc-1-8)
        (at flag_word_1 loc-1-7)
        (at is_word_1 loc-2-8)
        (at is_word_2 loc-2-7)
        (at is_word_3 loc-7-2)
        (at you_word_1 loc-3-8)
        (at win_word_1 loc-3-7)
        (at goop_word_1 loc-6-2)
        (at sink_word_1 loc-8-2)
        (at goop_obj_1 loc-1-6)
        (at goop_obj_2 loc-1-5)
        (at goop_obj_3 loc-1-4)
        (at goop_obj_4 loc-1-3)
        (at goop_obj_5 loc-1-2)
        (at goop_obj_6 loc-1-1)
        (at goop_obj_7 loc-2-1)
        (at goop_obj_8 loc-3-6)
        (at goop_obj_9 loc-3-5)
        (at goop_obj_10 loc-3-4)
        (at goop_obj_11 loc-3-3)
        (at goop_obj_12 loc-3-1)
        (at goop_obj_13 loc-4-8)
        (at goop_obj_14 loc-4-7)
        (at goop_obj_15 loc-4-6)
        (at goop_obj_16 loc-4-5)
        (at goop_obj_17 loc-4-4)
        (at goop_obj_18 loc-4-3)
        (at goop_obj_19 loc-4-1)
        (at goop_obj_20 loc-5-8)
        (at goop_obj_21 loc-5-7)
        (at goop_obj_22 loc-5-6)
        (at goop_obj_23 loc-5-5)
        (at goop_obj_24 loc-5-4)
        (at goop_obj_25 loc-6-5)
        (at goop_obj_26 loc-6-4)
        (at goop_obj_27 loc-7-5)
        (at goop_obj_28 loc-7-4)
        (at goop_obj_29 loc-8-5)
        (at goop_obj_30 loc-8-4)
        (at baba_obj_1 loc-2-6)
        (at flag_obj_1 loc-7-7)

         ; formed rules

       
        (rule_formed baba is you)
        (rule_formed flag is win)
        (rule_formed goop is sink)

         ; control rules

        (control_rule baba_obj_1 is you)

         ; fully granular rules (commented)

        ; (rule_formed goop_obj_6 goop_obj_7 goop_obj_12)
        ; (rule_formed goop_obj_6 goop_obj_5 goop_obj_4)
        ; (rule_formed goop_obj_5 goop_obj_4 goop_obj_3)
        ; (rule_formed goop_obj_4 goop_obj_3 goop_obj_2)
        ; (rule_formed goop_obj_3 goop_obj_2 goop_obj_1)
        ; (rule_formed goop_obj_2 goop_obj_1 flag_word_1)
        ; (rule_formed goop_obj_1 baba_obj_1 goop_obj_8)
        ; (rule_formed goop_obj_1 flag_word_1 baba_word_1)
        ; (rule_formed flag_word_1 is_word_2 win_word_1)
        ; (rule_formed baba_word_1 is_word_1 you_word_1)
        ; (rule_formed goop_obj_7 goop_obj_12 goop_obj_19)
        ; (rule_formed baba_obj_1 goop_obj_8 goop_obj_15)
        ; (rule_formed baba_obj_1 is_word_2 is_word_1)
        ; (rule_formed is_word_2 win_word_1 goop_obj_14)
        ; (rule_formed is_word_1 you_word_1 goop_obj_13)
        ; (rule_formed goop_obj_11 goop_obj_10 goop_obj_9)
        ; (rule_formed goop_obj_10 goop_obj_17 goop_obj_24)
        ; (rule_formed goop_obj_10 goop_obj_9 goop_obj_8)
        ; (rule_formed goop_obj_9 goop_obj_16 goop_obj_23)
        ; (rule_formed goop_obj_9 goop_obj_8 win_word_1)
        ; (rule_formed goop_obj_8 goop_obj_15 goop_obj_22)
        ; (rule_formed goop_obj_8 win_word_1 you_word_1)
        ; (rule_formed win_word_1 goop_obj_14 goop_obj_21)
        ; (rule_formed you_word_1 goop_obj_13 goop_obj_20)
        ; (rule_formed goop_obj_18 goop_obj_17 goop_obj_16)
        ; (rule_formed goop_obj_17 goop_obj_24 goop_obj_26)
        ; (rule_formed goop_obj_17 goop_obj_16 goop_obj_15)
        ; (rule_formed goop_obj_16 goop_obj_23 goop_obj_25)
        ; (rule_formed goop_obj_16 goop_obj_15 goop_obj_14)
        ; (rule_formed goop_obj_15 goop_obj_14 goop_obj_13)
        ; (rule_formed goop_obj_24 goop_obj_26 goop_obj_28)
        ; (rule_formed goop_obj_24 goop_obj_23 goop_obj_22)
        ; (rule_formed goop_obj_23 goop_obj_25 goop_obj_27)
        ; (rule_formed goop_obj_23 goop_obj_22 goop_obj_21)
        ; (rule_formed goop_obj_22 goop_obj_21 goop_obj_20)
        ; (rule_formed goop_word_1 is_word_3 sink_word_1)
        ; (rule_formed goop_obj_26 goop_obj_28 goop_obj_30)
        ; (rule_formed goop_obj_25 goop_obj_27 goop_obj_29)

    )

    (:goal (and
        ; Specify your goal here
        (overlapping baba_obj_1 flag_obj_1)
         ))
)
