

 ; pixel y: {__Y__} z: {__Z__} construction
 (make block
 (center (- (+ dpml Lsilicon (/ Lpixel 2)) 0x) (+ (* -0.5 wPIC) (* 0.5 wpixel) (* (- {__Y__} 1) wpixel)) (- (+ dpml (* (- {__Z__} 1) zpixel) (/ zpixel 2)) 0z))
 (size Lpixel wpixel zpixel)
 (material (make dielectric (epsilon 10.24))))

