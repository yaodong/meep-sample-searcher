(make block
 (center (- (+ dpml (/ {__X__} 2)) 0x) (+ (* -0.5 Wsilicon) (* 0.5 wpixel) (* (- {__Y__} 1) wpixel)) (+ (* -0.5 Hsilicon) (* 0.5 zpixel) (* (- {__Z__} 1) zpixel)))
 (size {__X__} wpixel zpixel)
 (material (make dielectric (epsilon 10.24))))
