(define (problem balls-problem)
	(:domain balls-domain)
	(:objects
		yellowball - ball
		greenball - ball
		redbasket - basket
		PR2 - robot
		
	)

	(:init 	(empty-gripper PR2)
			

	)

	(:goal
		(and 	(ball-in-basket yellowball redbasket)(ball-in-basket greenball redbasket)
				)
)

)
