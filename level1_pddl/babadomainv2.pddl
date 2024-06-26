(define (domain babadomainv2)
    (:requirements :strips :negative-preconditions :equality :conditional-effects)

    (:predicates
        (rule_formed ?word1 ?word2 ?word3)
        (at ?obj ?loc)
        (unoccupied ?loc)
        (adjacent ?loc1 ?loc2 ?orientation)
    )

    (:action move_to
        :parameters (?obj ?from ?to)
        :precondition (and
            (at ?obj ?from)
            (not (at ?obj ?to))
            (rule_formed baba_word is_word_1 you_word)
            (rule_formed flag_word is_word_2 win_word) ;; Ensure the rule is formed
            (= ?obj baba_obj)
            (or (unoccupied ?to) (at flag_obj ?to))
        )
        :effect (and
            (not (at ?obj ?from))
            (at ?obj ?to)
            (unoccupied ?from)
            (not (unoccupied ?to))
        )
    )


     (:action move_word
        :parameters (?word ?from ?to)
        :precondition (and
            (at ?word ?from)
            (unoccupied ?to)
        )
        :effect (and
            (not (at ?word ?from))
            (at ?word ?to)
            (unoccupied ?from)
            (not (unoccupied ?to))
        )
    )

    (:action form_rule
        :parameters (?word1 ?word2 ?word3 ?loc1 ?loc2 ?loc3 ?orientation)
        :precondition (and
            (at ?word1 ?loc1)
            (at ?word2 ?loc2)
            (at ?word3 ?loc3)
            (adjacent ?loc1 ?loc2 ?orientation)
            (adjacent ?loc2 ?loc3 ?orientation)
            (not (rule_formed ?word1 ?word2 ?word3))
        )
        :effect (and
            (rule_formed ?word1 ?word2 ?word3)
        )
    )
   
)

