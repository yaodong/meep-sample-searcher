; lattice size
(define-param Lsilicon 50)              ; The thickness of Silicon
(define-param Wsilicon 1000)           ; The width of Silicon
(define-param Hsilicon 1000)
(define-param Lpixel   5)                ; The thickness of Pixel
(define-param wPIC    1000)              ; The length of Pixel
(define-param hPIC    1000)              ; The height of Pixel
(define-param airbound 300)              ; The thickness of Air
(define-param ny 20)                    ; number of pixels in y direction
(define-param nz 20)                    ; number of pixels in z direction
(define-param wpixel (/ wPIC ny))                    ; width of pixel in propagation direction
(define-param zpixel (/ hPIC ny))                    ; height of pixel in z direction
(define-param dpml 50)                    ; thickness of pml

(define-param sx (+ Lsilicon Lpixel airbound))                  ; size of structure cell in X
(define-param sy wPIC)                  ; size of structure cell in Y
(define-param sz hPIC)                  ; size of structure cell in Z
(define-param sxvert (+ sx (* 2 dpml))) ; computation size in X
(define-param syvert (+ sy (* 2 dpml))) ; computation size in Y
(define-param szvert (+ sz (* 2 dpml))) ; computation size in Z
(define-param 0x (/ sxvert 2))            ; half computation size in X direction
(define-param 0y (/ syvert 2))            ; half computation size in Y direction
(define-param 0z (/ szvert 2))            ; half computation size in Z direction

(define-param wave 300)                   ; wavelength
(define-param res 0.5)                     ; resolution
(define-param theta (/ (* pi 0) 180))      ; incident angle
(define-param T 300)                       ; output time
(define-param T2 180)                      ; output time

(set! default-material air)               ; automatically define material as air
(set! resolution res)                     ; resolution
(set! force-complex-fields? false)        ; not complex fields simulation
(set! ensure-periodicity true)            ; periodicity
(set! eps-averaging? true)                ; epsilon averaged
(set! pml-layers (list (make pml (thickness dpml))))   ; PML boundary condition surrouding the structure
(set! geometry-lattice (make lattice (size sxvert syvert szvert))) ;computational cell

(set! geometry
(list

 (make block                             ; Silicon
 (center (- (/ (+ dpml Lsilicon) 2) 0x) 0 0)
 (size (+ dpml Lsilicon) (+ dpml Wsilicon dpml) (+ dpml Hsilicon dpml))
 (material (make dielectric (epsilon 10.24))))



 ; pixel z y
 ; pixel ZZZ YYY construction
 (make block
 (center (- (+ dpml Lsilicon (/ Lpixel 2)) 0x) (+ (* -0.5 wPIC) (* 0.5 wpixel) (* (- ZZZ YYY) wpixel)) (- (+ dpml (* (- ZZZ YYY) zpixel) (/ zpixel 2)) 0z))
 (size Lpixel wpixel zpixel)
 (material (make dielectric (epsilon 10.24))))


)
)
(set! sources
(list

(make source (src (make continuous-src (wavelength wave) (width 10)))
(component Ey) (center (- dpml 0x) 0 0) (size 0 Wsilicon Hsilicon)
)
)
)

(use-output-directory)


(run-until T

(at-beginning output-epsilon)
(at-end output-efield-y)
(at-end output-efield-x)
)
