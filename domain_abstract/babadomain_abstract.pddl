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

(:action form_rule
    :parameters (?word1 - word ?from1 - location ?to1 - location 
                 ?word2 - word ?from2 - location ?to2 - location 
                 ?word3 - word ?from3 - location ?to3 - location 
                 ?orientation - orientation)
    :precondition (and
        (or
            ; One word moves
            (and (at ?word1 ?from1) (at ?word2 ?to2) (= ?to2 ?from2) (at ?word3 ?to3) (= ?to3 ?from3))
            (and (at ?word1 ?to1) (= ?to1 ?from1) (at ?word2 ?from2) (at ?word3 ?to3) (= ?to3 ?from3))
            (and (at ?word1 ?to1) (= ?to1 ?from1) (at ?word2 ?to2) (= ?to2 ?from2) (at ?word3 ?from3))
        )
        (or
          ; Two words move
            (and (at ?word1 ?from1) (at ?word2 ?from2) (at ?word3 ?to3) (= ?to3 ?from3))
            (and (at ?word1 ?from1) (at ?word2 ?to2) (= ?to2 ?from2) (at ?word3 ?from3))
            (and (at ?word1 ?to1) (= ?to1 ?from1) (at ?word2 ?from2) (at ?word3 ?from3))
        )
        (or
          (and (at ?word1 ?from1) (at ?word2 ?from2) (at ?word3 ?from3))
        )
        (adjacent ?to1 ?to2 ?orientation)
        (adjacent ?to2 ?to3 ?orientation)
        (valid_rule ?word1 ?word2 ?word3)
        (not (rule_formed ?word1 ?word2 ?word3))
    )
    :effect (and
        (when (and (not (= ?to1 ?from1)) (not (= ?to2 ?from2)) (not (= ?to3 ?from3)))
              (and (not (at ?word1 ?from1)) (at ?word1 ?to1)
                   (not (at ?word2 ?from2)) (at ?word2 ?to2)
                   (not (at ?word3 ?from3)) (at ?word3 ?to3)))
        (when (and (not (= ?to1 ?from1)) (not (= ?to2 ?from2)) (= ?to3 ?from3))
              (and (not (at ?word1 ?from1)) (at ?word1 ?to1)
                   (not (at ?word2 ?from2)) (at ?word2 ?to2)))
        (when (and (not (= ?to1 ?from1)) (= ?to2 ?from2) (not (= ?to3 ?from3)))
              (and (not (at ?word1 ?from1)) (at ?word1 ?to1)
                   (not (at ?word3 ?from3)) (at ?word3 ?to3)))
        (when (and (= ?to1 ?from1) (not (= ?to2 ?from2)) (not (= ?to3 ?from3)))
              (and (not (at ?word2 ?from2)) (at ?word2 ?to2)
                   (not (at ?word3 ?from3)) (at ?word3 ?to3)))
        (when (and (not (= ?to1 ?from1)) (= ?to2 ?from2) (= ?to3 ?from3))
              (and (not (at ?word1 ?from1)) (at ?word1 ?to1)))
        (when (and (= ?to1 ?from1) (not (= ?to2 ?from2)) (= ?to3 ?from3))
              (and (not (at ?word2 ?from2)) (at ?word2 ?to2)))
        (when (and (= ?to1 ?from1) (= ?to2 ?from2) (not (= ?to3 ?from3)))
              (and (not (at ?word3 ?from3)) (at ?word3 ?to3)))
        (rule_formed ?word1 ?word2 ?word3)
    )
)

)
