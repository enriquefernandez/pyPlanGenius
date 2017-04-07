(define (domain hammerworld-domain)
	(:requirements :strips :typing)
	(:types object)

	(:predicates
		(has ?o - object)
		(stored ?o - object)
		(hammered ?o - object)
		(located ?o - object)
		(eaten ?f - food)
		
	)
	

	(:action find-object
		:parameters (?o - object)
		:precondition (and	(stored ?o)	)
		:effect 	(and 	(located ?o)
							(not (stored ?o)))
							
	)

	(:action pickup-object
		:parameters (?o - object)
		:precondition (and	(located ?o))

		:effect 	(and (has ?o)(not (located ?o)))
							
	)


	(:action hammer-nail
		:parameters (?h - hammer ?n - nail)
		:precondition (and	(has ?h)(has ?n))

		:effect 	(and (hammered ?n)(not(has ?n)))
	)

	(:action store-object
		:parameters (?o - object)
		:precondition (and(has ?o))

		:effect 	(and (stored ?o)(not(has ?o)))
	)

	(:action eat-something
		:parameters (?f - food)
		:precondition (and )

		:effect 	(and (eaten ?f))
	)

	

	
)

