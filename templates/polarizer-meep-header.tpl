(define-param Lsilicon 600)              ; The thickness of Silicon
(define-param Wsilicon 2000)           ; The width of pixel surface
(define-param Hsilicon 2000)           ; The height of Silicon
(define-param Lpixel   500)                ; The thickness of Pixel
(define-param wPIC   5000)              ; The length of Pixel
(define-param hPIC   5000)              ; The height of Pixel
(define-param airbound 1000)              ; The thickness of Air
(define-param ny 20)                    ; number of pixels in y direction
(define-param nz 20)                    ; number of pixels in z direction
(define-param wpixel (/ Wsilicon ny))                    ; width of pixel in propagation direction
(define-param zpixel (/ Hsilicon ny))                    ; height of pixel in z direction
(define-param dpml 200)                    ; thickness of pml
(define-param sx (+ Lsilicon Lpixel airbound))                  ; size of structure cell in X
(define-param sy wPIC)                  ; size of structure cell in Y
(define-param sz hPIC)                  ; size of structure cell in Z
(define-param sxvert (+ sx (* 2 dpml))) ; computation size in X
(define-param syvert (+ sy (* 2 dpml))) ; computation size in Y
(define-param szvert (+ sz (* 2 dpml))) ; computation size in Z
(define-param 0x (/ sxvert 2))            ; half computation size in X direction
(define-param 0y (/ syvert 2))            ; half computation size in Y direction
(define-param 0z (/ szvert 2))            ; half computation size in Z direction

(define-param wave 1500)                   ; wavelength
(define-param res 0.05)                     ; resolution
(define-param theta (/ (* pi 0) 180))      ; incident angle
(define-param T 10000)                       ; output time
(define-param T2 180)                      ; output time

(set! default-material air)               ; automatically define material as air
(set! resolution res)                     ; resolution
(set! force-complex-fields? true)        ; not complex fields simulation
(set! ensure-periodicity true)            ; periodicity
(set! eps-averaging? true)                ; epsilon averaged
(set! pml-layers (list (make pml (thickness dpml))))   ; PML boundary condition surrouding the structure

(set! geometry-lattice (make lattice (size sxvert syvert szvert))) ;computational cell

(set! geometry
(list
 (make block                             ; Silicon
 (center (- (/ (+ dpml Lsilicon) 2) 0x) 0 0)
 (size (+ dpml Lsilicon) Wsilicon Hsilicon)
 (material (make dielectric (epsilon 10.24))))
