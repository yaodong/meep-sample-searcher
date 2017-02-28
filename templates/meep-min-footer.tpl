
  (make block                             ; output waveguide 2
  {__OUTPUT_WAVEGUIDE__}
  (size (+ loutput dpml) woutput hsilicon)
  (material (make dielectric (epsilon 10.24))))

  (make block                             ; graphene sheet
  (center  0 0 (- (+ dpml wairbound hsilicon (/ hgraphene 2)) 0z))
  (size lgraphene wgraphene hgraphene)
  (material mygraphene)   ; Minimum absorption
  )

)
)

;(set! k-point (vector3 7.3 0 0))

(set! sources
(list

  (make source (src (make continuous-src (wavelength wave) (width 10)))
  {__EZ__}
  )

)
)


(use-output-directory)


(run-until T

(at-beginning output-epsilon)
(at-end output-efield-y)
(at-end output-efield-z)
(at-end output-efield-x)
)
