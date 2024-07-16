(define (domain baba)
    (:requirements :strips :negative-preconditions :equality :conditional-effects)

    (:types 
        word word_instance object_instance location orientation
    )

    (:predicates
        (control_rule ?obj_name - object_instance ?word2 - word ?word3 - word)
        (at ?obj - object_instance ?loc - location)
        (overlapping ?obj1 - object_instance ?obj2 - object_instance)
    )

    (:action move_to
        :parameters (?obj - object_instance ?to)
        :precondition (and
            (not (at ?obj ?to))
            (control_rule ?obj is you)
        )
        :effect (and
            (at ?obj ?to)
            (overlapping ?obj ?to)
        )
    )

)
