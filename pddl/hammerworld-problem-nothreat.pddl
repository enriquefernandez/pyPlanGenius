(define (problem hammerworld-problem)
	(:domain hammerworld-domain)
	(:objects
		hammer - object
		hammer - hammer
		nail - object
		nail - nail
		sandwich - food
		pizza - food
		
	)

	(:init 	(stored hammer)
			(stored nail)

	)

	(:goal
		(and 	(hammered nail)
				)
)

)
