(define (domain babadomainv3)
    (:requirements :strips :negative-preconditions :equality :conditional-effects)

    (:types word object location )


    (:predicates
        (rule_formed ?word1 - word ?word2 - word ?word3 - word)
        (at ?obj - object ?loc - location)
        (unoccupied ?loc - location)
        (adjacent ?loc1 - location ?loc2 - location ?orientation)
        (is-controllable ?obj - object)
    )

    (:action move_to
        :parameters (?obj - object ?from - location ?to - location)
        :precondition (and
            (at ?obj ?from)
            (not (at ?obj ?to))
            (is-controllable ?obj)    
            (or (unoccupied ?to) (at flag_obj ?to))
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

    ; (:action move_word
    ;     :parameters (?word - word ?from - location ?to - location)
    ;     :precondition (and
    ;         (at ?word ?from)
    ;         (unoccupied ?to)
    ;     )
    ;     :effect (and
    ;         (not (at ?word ?from))
    ;         (at ?word ?to)
    ;         (unoccupied ?from)
    ;         (not (unoccupied ?to))
    ;     )
    ; )

    ; (:action push_word
    ;     :parameters (?obj - object ?word - word ?from - location ?to - location)
    ;     :precondition (and
    ;         (at ?obj ?from)
    ;         (at ?word ?from)
    ;         (adjacent ?from ?to ?orientation)
    ;         (unoccupied ?to)
    ;         (is-controllable ?obj)
    ;     )
    ;     :effect (and
    ;         (not (at ?word ?from))
    ;         (at ?word ?to)
    ;         (unoccupied ?from)
    ;         (not (unoccupied ?to))
    ;     )
    ; )

    (:action push_to
        :parameters (?obj - object ?word - word ?from - location ?to - location ?adj_from - location ?adj_to - location ?orientation)
        :precondition (and
            (at ?obj ?adj_from)
            (at ?word ?from)
            (adjacent ?adj_from ?from ?orientation)
            (adjacent ?from ?to ?orientation)
            (adjacent ?adj_to ?to ?orientation)
            (unoccupied ?to)
            (is-controllable ?obj)
        )
        :effect (and
            (not (at ?word ?from))
            (at ?word ?to)
            (unoccupied ?from)
            (not (unoccupied ?to))
            (not (at ?obj ?adj_from))
            (at ?obj ?adj_to)
            (unoccupied ?adj_from)
            (not (unoccupied ?adj_to))
        )
    )

    


    (:action form_rule
        :parameters (?word1 - word ?word2 - word ?word3 - word ?loc1 - location ?loc2 - location ?loc3 - location ?orientation)
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
