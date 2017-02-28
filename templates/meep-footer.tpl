
  (make block                             ; output waveguide 2
    (center (- (+ dpml linput lPIC (/ (+ loutput dpml) 2)) 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))
    (size (+ loutput dpml) woutput hsilicon)
    (material (make dielectric (epsilon 10.24))))

  (make block                             ; graphene sheet
    (center  0 0 (- (+ dpml wairbound hsilicon (/ hgraphene 2)) 0z))
    (size lgraphene wgraphene hgraphene)
    {__MAX_MIN__}
    )
))

(set! k-point (vector3 7.3 0 0))

(set! sources
  (list
    (make eigenmode-source (src (make continuous-src (wavelength wave) (width 10)))
    (component Ez) (center (- dpml 0x) 0 0) (size 0 winput hsilicon) (eig-kpoint k-point)
    (eig-parity TM)
    )))

(use-output-directory)

(run-until T
  (at-beginning output-epsilon)
  (at-end output-efield-y)
  (at-end output-efield-z)
  (at-end output-efield-x)
)
