(define (domain baba0)
    (:requirements :strips)

    (:predicates
        (rule_formed ?word1 ?word2 ?word3)
        (overlapping ?obj1 ?obj2)
    )
    
     (:action move_to
        :parameters (?obj1 ?obj2)
        :precondition (and
            (not (overlapping ?obj1 ?obj2))
            (rule_formed ?obj1 is you)
        )
        :effect (and
            (when (rule_formed ?obj2 is win)
            (overlapping ?obj1 ?obj2)
            )
            )
        )
    
     (:action form_rule
        :parameters (?word1 ?word2 ?word3)
        :precondition (and
            (not (rule_formed ?word1 ?word2 ?word3))
        )
        :effect (and
            (rule_formed ?word1 ?word2 ?word3)
        )
    )

)
