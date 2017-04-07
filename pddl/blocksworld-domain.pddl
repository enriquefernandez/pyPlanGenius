(define (domain blocksworld-domain)
	(:requirements :strips :typing)
	(:types robot block cart)

	(:predicates
		(holding ?r - robot ?t - block)
		(empty-gripper ?r - robot)
		(clear-above ?t - block)
		(clear-cart ?c - cart)
		(can-reach ?r - robot ?t - block)
		(can-reach-cart ?r - robot ?c - cart)
		(on ?t ?b - block)
		(on-ground ?t - block)
		(on-cart ?t - block ?c - cart)
	)
	

	(:action pick-up-block-from-ground
		:parameters (?r - robot ?t - block)
		:precondition (and	(clear-above ?t)
							(empty-gripper ?r)
							(can-reach ?r ?t)
							(on-ground ?t))		
		:effect 	(and 	(not (empty-gripper ?r))
							(not (on-ground ?t))
							(holding ?r ?t)
							(not (clear-above ?t)))
	)


	(:action pick-up-block
		:parameters (?r - robot ?t ?b - block)
		:precondition (and	(clear-above ?t)
							(empty-gripper ?r)
							(can-reach ?r ?t)
							(on ?t ?b))

		:effect 	(and 	(not (empty-gripper ?r))
							(not (on ?t ?b))
							(holding ?r ?t)
							(clear-above ?b)
							(not (clear-above ?t)))
	)

	(:action pick-up-block-from-cart
		:parameters (?r - robot ?t - block ?c - cart)
		:precondition (and	(clear-above ?t)
							(empty-gripper ?r)
							(can-reach ?r ?t)
							(on-cart ?t ?c))

		:effect 	(and 	(not (empty-gripper ?r))
							(not (on-cart ?t ?c))
							(holding ?r ?t)
							(clear-cart ?c)
							(not (clear-above ?t)))
	)

	(:action stack-block
		:parameters (?r - robot ?t ?b - block)
		:precondition (and	(holding ?r ?t)
							(clear-above ?b))

		:effect		(and	(empty-gripper ?r)
							(on ?t ?b)
							(not (clear-above ?b))
							(not (holding ?r ?t))
							(clear-above ?t))
	)

	(:action put-block-on-ground
		:parameters (?r - robot ?t - block)
		:precondition (and 	(holding ?r ?t))

		:effect 	(and 	(empty-gripper ?r)
							(not (holding ?r ?t))					
							(on-ground ?t)
							(clear-above ?t))
	)

	(:action put-block-on-cart
		:parameters (?r - robot ?t - block ?c - cart)
		:precondition (and	(holding ?r ?t)
							(clear-cart ?c)
							(can-reach-cart ?r ?c))

		:effect		(and	(empty-gripper ?r)
							(on-cart ?t ?c)
							(not (holding ?r ?t))
							(clear-above ?t))
	)
)

