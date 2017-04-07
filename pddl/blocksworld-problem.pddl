(define (problem blocksworld-problem)
	(:domain blocksworld-domain)
	(:objects
		WAM7 - robot
		BlueBlock - block
		RedBlock - block
		MediumPinkBlock - block
		LimeBlock - block
		Cart - cart
	)

	(:init (empty-gripper WAM7)
		(on-ground BlueBlock)
		(can-reach WAM7 RedBlock)
		(can-reach WAM7 MediumPinkBlock)
		(can-reach WAM7 LimeBlock)
		(can-reach WAM7 BlueBlock)
		(can-reach-cart WAM7 Cart)
		(on MediumPinkBlock BlueBlock)
		(on-ground LimeBlock)
		(on RedBlock LimeBlock)
		(clear-above RedBlock)
		(clear-above MediumPinkBlock)
		(clear-cart Cart))

	(:goal
		(and(on-cart RedBlock Cart)(on-cart MediumPinkBlock Cart))
)

)
