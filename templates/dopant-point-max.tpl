; pixel {__LENGTH_OFFSET__} {__WIDTH_OFFSET__} construction
(make block
    (center (- (+ dpml linput (* lpixel (- {__LENGTH_OFFSET__} 1)) (/ lpixel 2)) 0x) (+ (* -0.5 wPIC) (* 0.5 wpixel) (* (- {__WIDTH_OFFSET__} 1) wpixel)) (- (+ dpml wairbound (/ hsilicon 2)) 0z))
    (size lpixel wpixel hsilicon)
    (material (make dielectric (epsilon 10.24) (D-conductivity (/ (* 2 pi 0.6452 0.0000671) 10.24)))))
