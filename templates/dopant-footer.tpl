  (make block                             ; output waveguide 2
  (center (- (+ dpml linput lPIC (/ (+ loutput dpml) 2)) 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))
  (size (+ loutput dpml) woutput hsilicon)
  (material (make dielectric (epsilon 10.24))))

)
)

;(set! k-point (vector3 7.3 0 0))

(set! sources
(list

  (make source (src (make continuous-src (wavelength wave) (width 10)))
  (component Ez) (center (- dpml 0x) 0 0) (size 0 winput hsilicon)
  )

)
)


(use-output-directory)


(run-until T

(at-beginning output-epsilon)
(at-end output-efield-y)
(at-end output-efield-z)
(at-end output-efield-x)
(at-end output-hfield-x)
)
