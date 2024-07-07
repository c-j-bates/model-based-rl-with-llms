(define (domain babadomain_abstract_v6)
    (:requirements :strips :negative-preconditions :equality :conditional-effects)

    (:types word object location orientation)

    (:predicates
        (rule_formed ?word1 - word ?word2 - word ?word3 - word)
        (at ?obj - object ?loc - location)
        (unoccupied ?loc - location)
        (adjacent ?loc1 - location ?loc2 - location ?orientation - orientation)
        (is-controllable ?obj - object)
        (valid_rule ?word1 - word ?word2 - word ?word3 - word)
        (movable ?obj - object)
        (clear_path ?from - location)
        (wait_formation)
    )

     (:action move_to
        :parameters (?obj - object ?from - location ?to - location)
        :precondition (and
            (at ?obj ?from)
            (not (at ?obj ?to))
            (is-controllable ?obj)
            (clear_path ?from) ; Ensure path is clear
        )
        :effect (and
            (not (at ?obj ?from))
            (at ?obj ?to)
            (unoccupied ?from)
            (not (unoccupied ?to))
            ; (forall (?loc1 - location ?loc2 - location)
            ;     (when (and (adjacent ?from ?loc1 ?orientation)
            ;                (adjacent ?loc1 ?loc2 ?orientation))
            ;         (clear_path ?loc1 ?loc2))
            ; )
        )
    )

    ; (:action wait
    ;     :parameters ()
    ;     :precondition (and
    ;         (wait_formation)
    ;     )
    ;     :effect (and
    ;         (not (wait_formation))
    ;     )
    ; )


    (:action push_to
            :parameters (?babaobj - object ?obj - object ?from - location ?to - location ?orientation - orientation)
            :precondition (and
                (at ?obj ?from)
                (unoccupied ?to)
                (movable ?obj)
                (adjacent ?from ?to ?orientation)
                ; (adjacent ?from ?to ?orientation)
                (not (is-controllable ?obj))
                (is-controllable ?babaobj)
                (not (clear_path ?from))
                (not (clear_path ?to))
                ; (rule_formed rock_word is_word)
                ; (rule_formed rock_word is_word_3 push_word)
            )
            :effect (and
                (not (at ?obj ?from))
                (at ?obj ?to)
                (unoccupied ?from)
                (not (unoccupied ?to))
                (when (at ?obj3 ?to)
                    (and
                        (not (at ?obj3 ?to))
                        (at ?obj3 ?next_to)
                        (unoccupied ?to)
                        (not (unoccupied ?next_to))
                        (clear_path ?next_to)
                    )
                )
                (clear_path ?from)
                (clear_path ?to)
                (at ?babaobj ?from))
            )


    (:action form_rule
        :parameters (?word1 - word ?from1 - location ?to1 - location 
                     ?word2 - word ?from2 - location ?to2 - location 
                     ?word3 - word ?from3 - location ?to3 - location 
                     ?orientation - orientation)
        :precondition (and
            (valid_rule ?word1 ?word2 ?word3)
            (not (rule_formed ?word1 ?word2 ?word3))
            (or
                (and (at ?word1 ?from1) (at ?word2 ?to2) (= ?to2 ?from2) (at ?word3 ?to3) (= ?to3 ?from3))
                (and (at ?word1 ?to1) (= ?to1 ?from1) (at ?word2 ?from2) (at ?word3 ?to3) (= ?to3 ?from3))
                (and (at ?word1 ?to1) (= ?to1 ?from1) (at ?word2 ?to2) (= ?to2 ?from2) (at ?word3 ?from3))
                ; (and (= ?word1 baba_word_1) (= ?from1 ?to1))
                ; (and (= ?word1 baba_word) (= ?from1 ?to1))

                ; (and (= ?word1 keke_word_1) (= ?from1 ?to1))
            )
            (or 
                (and (at ?word1 ?from1) (at ?word2 ?from2) (at ?word3 ?to3) (= ?to3 ?from3))
                (and (at ?word1 ?from1) (at ?word2 ?to2) (= ?to2 ?from2) (at ?word3 ?from3))
                (and (at ?word1 ?to1) (= ?to1 ?from1) (at ?word2 ?from2) (at ?word3 ?from3))
                ; (and (= ?word1 baba_word) (= ?from1 ?to1))
            )

            (or 
            (and (at ?word1 ?from1) (at ?word2 ?from2) (at ?word3 ?from3))
            ; (and (= ?word1 baba_word) (= ?from1 ?to1))

            )
            (not (= ?to1 ?to2))
            (not (= ?to2 ?to3))
            (not (= ?to3 ?to1))
            (adjacent ?to1 ?to2 ?orientation)
            (adjacent ?to2 ?to3 ?orientation)
            ; (or
            ; ; (not (= ?word1 baba_word))
            ; (and (= ?word1 baba_word) (= ?from1 ?to1))
            ; )

                )
        :effect (and

            (at ?word1 ?to1)
            (at ?word2 ?to2)
            (at ?word3 ?to3)
            (unoccupied ?from1)
            (unoccupied ?from2)
            (unoccupied ?from3)
            (not (unoccupied ?to1))
            (not (unoccupied ?to2))
            (not (unoccupied ?to3))
            ; ; If baba_word is the first word, ensure it doesn't move
            ; (when (= ?word1 baba_word_1)
            ;     (and
            ;         (at baba_word_1 ?from1) ; Ensure baba_word stays at its original position
            ;         (not (at baba_word_1 ?to1))))
            ; ; If baba_word is the first word, ensure it doesn't move
            ; (when (= ?word1 keke_word_1)
            ;       (and (is-controllable keke_obj_1))
            ; )
            ; (when (= ?word1 keke_word_1)
            ;     (and
            ;     (is-controllable keke_obj_1)
            ;     ))
            (when (= ?word1 keke_word_1) ; make this more explicit
                (and
                (is-controllable keke_obj_1)
                ))
            (rule_formed ?word1 ?word2 ?word3)
        )
    )

(:action break_rule
    :parameters (?word - word ?from - location ?to - location ?orientation - orientation ?w1 - word ?word - word ?w3 - word)
    :precondition (and
        (at ?word ?from)
        (unoccupied ?to)
        (adjacent ?from ?to ?orientation)
        ; (is-controllable ?word)
         (or
            (rule_formed ?word ?w2 ?w3)
            (rule_formed ?w1 ?word ?w3)
            (rule_formed ?w1 ?w2 ?word)
            )
    )
    :effect (and
        (not (at ?word ?from))
        (at ?word ?to)
        (unoccupied ?from)
        (not (unoccupied ?to))
        (when (rule_formed ?word ?w2 ?w3)
            (not (rule_formed ?word ?w2 ?w3)))
        (when (rule_formed ?w1 ?word ?w3)
            (not (rule_formed ?w1 ?word ?w3)))
        (when (rule_formed ?w1 ?w2 ?word)
            (not (rule_formed ?w1 ?w2 ?word)))
    )
)

(:action break_rule
    :parameters (?word - word ?from - location ?to - location ?orientation - orientation ?word - word ?w2 - word ?w3 - word)
    :precondition (and
        (at ?word ?from)
        (unoccupied ?to)
        (adjacent ?from ?to ?orientation)
        ; (is-controllable ?word)
         (or
            (rule_formed ?word ?w2 ?w3)
            (rule_formed ?w1 ?word ?w3)
            (rule_formed ?w1 ?w2 ?word)
            )
    )
    :effect (and
        (not (at ?word ?from))
        (at ?word ?to)
        (unoccupied ?from)
        (not (unoccupied ?to))
        (when (rule_formed ?word ?w2 ?w3)
            (not (rule_formed ?word ?w2 ?w3)))
        (when (rule_formed ?w1 ?word ?w3)
            (not (rule_formed ?w1 ?word ?w3)))
        (when (rule_formed ?w1 ?w2 ?word)
            (not (rule_formed ?w1 ?w2 ?word)))
    )
)


(:action break_rule
    :parameters (?word - word ?from - location ?to - location ?orientation - orientation ?w1 - word ?w2 - word ?word - word)
    :precondition (and
        (at ?word ?from)
        (unoccupied ?to)
        (adjacent ?from ?to ?orientation)
        ; (is-controllable ?word)
         (or
            (rule_formed ?word ?w2 ?w3)
            (rule_formed ?w1 ?word ?w3)
            (rule_formed ?w1 ?w2 ?word)
            )
    )
    :effect (and
        (not (at ?word ?from))
        (at ?word ?to)
        (unoccupied ?from)
        (not (unoccupied ?to))
        (when (rule_formed ?word ?w2 ?w3)
            (not (rule_formed ?word ?w2 ?w3)))
        (when (rule_formed ?w1 ?word ?w3)
            (not (rule_formed ?w1 ?word ?w3)))
        (when (rule_formed ?w1 ?w2 ?word)
            (not (rule_formed ?w1 ?w2 ?word)))
    )
)

 

)
