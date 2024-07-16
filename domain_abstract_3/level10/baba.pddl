(define (domain baba)
    (:requirements :strips :negative-preconditions :equality :conditional-effects :typing)

    (:types 
        word word_instance object_instance location orientation
    )

    (:predicates
        (control_rule ?obj_name - object_instance ?word2 - word ?word3 - word)
        (at ?obj ?loc)
        (overlapping ?obj1 - object_instance ?obj2 - object_instance)
        (rule_formed ?word1 - word ?word2 - word ?word3 - word)
        (movable_rule ?obj_name - object_instance ?word2 - word ?word3 - word)
        (path-clear)
    )

    (:action move_to
        :parameters (?obj - object_instance ?to)
        :precondition (and
            (not (at ?obj ?to))
            (control_rule ?obj is you)
            (path-clear)
        )
        :effect (and
            (at ?obj ?to)
            (overlapping ?obj ?to)
        )
    )

    (:action form_rule
        :parameters (?word1 - word ?word2 - word ?word3 - word)
        :precondition (not (rule_formed ?word1 ?word2 ?word3))
        :effect (rule_formed ?word1 ?word2 ?word3)
    )

     (:action break_rule
        :parameters (?word1 - word ?word2 - word ?word3 - word)
        :precondition (rule_formed ?word1 ?word2 ?word3)
        :effect (and 
        (not (rule_formed ?word1 ?word2 ?word3))
        (path-clear)
        ))
    

     (:action push
        :parameters (?obj - object_instance)
        :precondition (and
            (movable_rule ?obj is push)
        )
        :effect (and
            (path-clear)
        )
    )

    (:action wait
        :parameters (?obj - object_instance)
        :precondition (and (rule_formed keke is move))
        :effect (and (control_rule ?obj is you))
    )
    
    
)
