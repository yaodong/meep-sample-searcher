(define-param linput {__L_INPUT__})                    ; length of input waveguide
(define-param winput 0.6)                    ; width of input waveguide
(define-param hsilicon 0.25)					; height of silicon
(define-param lPIC {__PIXEL_LENGTH__})                           ; length of pixel
(define-param wPIC {__PIXEL_WIDTH__})                           ; width of pixel
(define-param loutput {__L_OUTPUT__})                        ; length of output waveguide
(define-param woutput 0.6)                      ; width of output waveguide
(define-param wairbound 0.1)                    ; air surrounding the PIC in Y direction
(define-param wgraphene {__PIXEL_WIDTH__})              ; width of graphene sheet
(define-param lgraphene {__GRAPH_LENGTH__})                ; length of graphene sheet
(define-param hgraphene 0.02)            ; thickness of graphene sheet
(define-param nx {__LAYOUT_LENGTH__})                    ; number of pixels in x direction
(define-param ny {__LAYOUT_WIDTH__})                    ; number of pixels in y direction
(define-param lpixel (/ lPIC nx))                    ; thickness of pixel in propagation direction
(define-param wpixel (/ wPIC ny))                    ; height of pixel in Y direction
(define-param dpml 0.6)                    ; thickness of pml
(define-param sx (+ linput lPIC loutput))                  ; size of structure cell in X
(define-param sy (+ wairbound wPIC wairbound))                  ; size of structure cell in Y
(define-param sz (+ wairbound hgraphene hsilicon wairbound)) ; size of structure cell in Z
(define-param sxvert (+ sx (* 2 dpml))) ; computation size in X
(define-param syvert (+ sy (* 2 dpml))) ; computation size in Y
(define-param szvert (+ sz (* 2 dpml))) ; computation size in Z
(define-param 0x (/ sxvert 2))            ; half computation size in X direction


(define-param 0y (/ syvert 2))            ; half computation size in Y direction


(define-param 0z (/ szvert 2))            ; half computation size in Z direction


(define-param wave 1.53)                   ; wavelength
(define-param res {__RESOLUTION__})                     ; resolution
(define-param theta (/ (* pi 0) 180))      ; incident angle
(define-param T 200)                       ; output time
(define-param T2 180)                      ; output time


(set! default-material air)               ; automatically define material as air
(set! resolution res)                     ; resolution
(set! force-complex-fields? true)        ; not complex fields simulation
(set! ensure-periodicity true)            ; periodicity
(set! eps-averaging? true)                ; epsilon averaged
(set! pml-layers (list (make pml (thickness dpml) ))); PML boundary condition surrouding the structure


(set! geometry-lattice (make lattice (size sxvert syvert szvert))) ;computational cell


(set! geometry
(list

  (make block                             ; input waveguide
  {__INPUT_WAVEGUIDE__}
  (size (+ dpml linput) winput hsilicon)
  (material (make dielectric (epsilon 10.24))))
