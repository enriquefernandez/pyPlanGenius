(define (domain simpleworld-domain)
	(:requirements :strips :typing)
	(:types object)

	(:predicates
		(state-a ?o - object)
		(state-b ?o - object)
		(state-c ?o - object)
		(state-d ?o - object)
		(state-f ?o - object)
		(state-e ?o - object)
		
	)
	

	(:action operator-a
		:parameters (?o - object)
		:precondition (and		)

		:effect 	(and (state-a ?o))
	)

	(:action operator-b
		:parameters (?o - object)
		:precondition (and		)

		:effect 	(and (state-b ?o))
	)


	(:action operator-d
		:parameters (?o - object)
		:precondition (and		)

		:effect 	(and 	(state-d ?o))
	)

	(:action operator-e
		:parameters (?o - object)
		:precondition (and		)

		:effect 	(and 	(state-e ?o))
	)

	(:action operator-c
		:parameters (?o - object)
		:precondition (and	(state-a ?o)(state-b ?o))

		:effect 	(and 	(state-c ?o))
	)

	(:action operator-f
		:parameters (?o - object)
		:precondition (and	(state-d ?o)(state-c ?o))

		:effect 	(and 	(state-f ?o))
	)
	
)

