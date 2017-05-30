 )
)
(set! sources
(list

  (make source (src (make continuous-src (wavelength wave) (width 10)))
  (component Ez) (center (- dpml 0x) 0 0) (size 0 Wsilicon Hsilicon)
  )
)
)

(use-output-directory)


(run-until T

(at-beginning output-epsilon)
(at-end output-efield-y)
(at-end output-efield-z)
(at-end output-hfield-x)
)
