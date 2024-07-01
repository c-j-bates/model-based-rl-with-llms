(define (domain babadomain_abstract)
    (:requirements :strips :negative-preconditions :equality :conditional-effects)

    (:types word object location orientation)

    (:predicates
        (rule_formed ?word1 - word ?word2 - word ?word3 - word)
        (at ?obj - object ?loc - location)
        (unoccupied ?loc - location)
        (adjacent ?loc1 - location ?loc2 - location ?orientation - orientation)
        (is-controllable ?obj - object)
        (valid_rule ?word1 - word ?word2 - word ?word3 - word)
    )

    (:action move_to
        :parameters (?obj - object ?from - location ?to - location)
        :precondition (and
            (at ?obj ?from)
            (not (at ?obj ?to))
            (is-controllable ?obj)    
            ; (or (unoccupied ?to) (at flag_obj ?to))
        )
        :effect (and
            (not (at ?obj ?from))
            (at ?obj ?to)
            (unoccupied ?from)
            (not (unoccupied ?to))
            ; (when (unoccupied ?to) (unoccupied ) (= ?word3 win_word))  ;when type is word then split object somehow
            ;     (ready_to_move)) ; Set the predicate when the rule is formed
        )
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
            )
            (or 
                (and (at ?word1 ?from1) (at ?word2 ?from2) (at ?word3 ?to3) (= ?to3 ?from3))
                (and (at ?word1 ?from1) (at ?word2 ?to2) (= ?to2 ?from2) (at ?word3 ?from3))
                (and (at ?word1 ?to1) (= ?to1 ?from1) (at ?word2 ?from2) (at ?word3 ?from3))
            )

            (or 
            (and (at ?word1 ?from1) (at ?word2 ?from2) (at ?word3 ?from3))
            
            )
            (not (= ?to1 ?to2))
            (not (= ?to2 ?to3))
            (not (= ?to3 ?to1))
            (adjacent ?to1 ?to2 ?orientation)
            (adjacent ?to2 ?to3 ?orientation)
            
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
            (rule_formed ?word1 ?word2 ?word3)
        )
    )
)



