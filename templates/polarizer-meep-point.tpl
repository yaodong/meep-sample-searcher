

 ; pixel z y
 ; pixel ZZZ YYY construction
 (make block
 (center (- (+ dpml Lsilicon (/ Lpixel 2)) 0x) (+ (* -0.5 wPIC) (* 0.5 wpixel) (* (- {__Z__} {__Y__}) wpixel)) (- (+ dpml (* (- {__Z__} {__Y__}) zpixel) (/ zpixel 2)) 0z))
 (size Lpixel wpixel zpixel)
 (material (make dielectric (epsilon 10.24))))

