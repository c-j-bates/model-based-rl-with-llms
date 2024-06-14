(define (domain baba_is_you)
    (:requirements :strips :negative-preconditions :equality :conditional-effects)

    (:predicates
        (rule_formed ?word1 ?word2 ?word3) 
        (at ?obj ?loc) 
        (unoccupied ?loc)
    )

    (:action move_to
        :parameters (?obj ?from ?to)
        :precondition (and
            (at ?obj ?from)
            (not (at ?obj ?to))
            (rule_formed baba_word is_word_1 you_word)
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

)
