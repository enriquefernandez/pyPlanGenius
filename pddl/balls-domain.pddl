(define (domain balls-domain)
	(:requirements :strips :typing)
	(:types ball basket)

	(:predicates
		(found ?r - robot ?b - ball)
		(holding ?r - robot ?b - ball)
		(ball-in-basket ?b - ball ?s - basket)
		(empty-gripper ?r - robot)

	)
	

	(:action find-ball
		:parameters (?r - robot ?b - ball)
		:precondition (and	)
		:effect 	(and (found ?r ?b))
							
	)

	(:action pickup-ball
		:parameters (?r - robot ?b - ball)
		:precondition (and	(found ?r ?b)(empty-gripper ?r))

		:effect 	(and (holding ?r ?b)(not(empty-gripper ?r)))
							
	)

	(:action drop-ball
		:parameters (?r - robot ?b - ball ?s - basket)
		:precondition (and	(holding ?r ?b))

		:effect 	(and (empty-gripper ?r)(not(holding ?r ?b))(ball-in-basket ?b ?s))
							
	)

	
)

