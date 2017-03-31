CATEGORIES = {
    '30x30': {
        'time': '01:30:00',
        'width': 30,
        'length': 30,
        'graphene_length': 3,
        'matlab': '30x30',
        'meep_linput': 2,
        'meep_loutput': 2,
        'meep_input_waveguide': '(center (- (/ (+ dpml linput) 2) 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_output_waveguide': '(center (- (+ dpml linput lPIC (/ (+ loutput dpml) 2)) 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_ez': '(component Ez) (center (- dpml 0x) 0 0) (size 0 winput hsilicon)',
        'parts': {
            'main': {
                'tweak': 'fish_bone',
                'width': {'offset': 0, 'size': 30},
                'length': {'offset': 0, 'size': 30}
            }
        }
    },
    '15x30': {
        'time': '00:29:58',
        'width': 30,
        'length': 15,
        'graphene_length': 1.5,
        'matlab': '15x30',
        'meep_linput': 2,
        'meep_loutput': 2,
        'meep_input_waveguide': '(center (- (/ (+ dpml linput) 2) 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_output_waveguide': '(center (- (+ dpml linput lPIC (/ (+ loutput dpml) 2)) 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_ez': '(component Ez) (center (- dpml 0x) 0 0) (size 0 winput hsilicon)',
        'parts': {
            'main': {
                'tweak': 'square',
                'width': {'offset': 0, 'size': 30},
                'length': {'offset': 0, 'size': 15}
            }
        }
    },
    '30x30_nov': {
        'time': '01:30:00',
        'width': 30,
        'length': 30,
        'graphene_length': 3,
        'matlab': '30x30',
        'meep_linput': 2,
        'meep_loutput': 2,
        'meep_input_waveguide': '(center (- (/ (+ dpml linput) 2) 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_output_waveguide': '(center (- (+ dpml linput lPIC (/ (+ loutput dpml) 2)) 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_ez': '(component Ez) (center (- dpml 0x) 0 0) (size 0 winput hsilicon)',
        'parts': {
            'main': {
                'tweak': 'square',
                'width': {'offset': 0, 'size': 30},
                'length': {'offset': 0, 'size': 30}
            }
        }
    },
   '30x60_feb': {
        'time': '01:30:00',
        'width': 30,
        'length': 60,
        'graphene_length': 6,
        'meep_linput': 2,
        'meep_loutput': 2,
        'matlab': '30x60',
        'meep_input_waveguide': '(center (- (/ (+ dpml linput) 2) 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_output_waveguide': '(center (- (+ dpml linput lPIC (/ (+ loutput dpml) 2)) 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_ez': '(component Ez) (center (- dpml 0x) 0 0) (size 0 winput hsilicon)',
        'parts': {
            'main': {
                'tweak': 'square',
                'width': {'offset': 0, 'size': 30},
                'length': {'offset': 0, 'size': 60}
            }
        }
    },
   '30x60': {
        'time': '01:30:00',
        'width': 30,
        'length': 60,
        'graphene_length': 6,
        'meep_linput': 2,
        'meep_loutput': 2,
        'matlab': '30x60',
        'meep_input_waveguide': '(center (- (/ (+ dpml linput) 2) 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_output_waveguide': '(center (- (+ dpml linput lPIC (/ (+ loutput dpml) 2)) 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_ez': '(component Ez) (center (- dpml 0x) 0 0) (size 0 winput hsilicon)',
        'parts': {
            'main': {
                'tweak': 'square',
                'width': {'offset': 0, 'size': 30},
                'length': {'offset': 0, 'size': 60}
            }
        }
    },
    '30x30w4': {
        'time': '01:30:00',
        'width': 30,
        'length': 92,
        'graphene_length': 9.2,
        'meep_linput': 4,
        'meep_loutput': 4,
        'matlab': '30x30w4',
        'meep_input_waveguide': '(center (+ (- (/ (+ dpml linput) 2) 0x) 3.1) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_output_waveguide': '(center (- (+ dpml linput lPIC (/ (+ loutput dpml) 2)) 3.1 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_ez': '(component Ez) (center (- (+ dpml 3.1) 0x) 0 0) (size 0 winput hsilicon)',
        'parts': {
            'main': {
                'tweak': 'keep',
                'width': {'offset': 0, 'size': 30},
                'length': {'offset': 31, 'size': 30},
            },
            'left_top': {
                'tweak': 'square',
                'width': {'offset': 0, 'size': 11},
                'length': {'offset': 0, 'size': 30}
            },
            'left_bottom': {
                'tweak': 'square',
                'width': {'offset': 19, 'size': 11},
                'length': {'offset': 0, 'size': 30}
            },
            'right_top': {
                'tweak': 'square',
                'width': {'offset': 0, 'size': 11},
                'length': {'offset': 62, 'size': 30}
            },
            'right_bottom': {
                'tweak': 'square',
                'width': {'offset': 19, 'size': 11},
                'length': {'offset': 62, 'size': 30}
            },
        }
    },
    '30x30w4s': {
        'time': '01:59:00',
        'width': 30,
        'length': 92,
        'graphene_length': 3,
        'matlab': '30x30w4s',
        'meep_linput': 4,
        'meep_loutput': 4,
        'meep_input_waveguide': '(center (+ (- (/ (+ dpml linput) 2) 0x) 3.1) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_output_waveguide': '(center (- (+ dpml linput lPIC (/ (+ loutput dpml) 2)) 3.1 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_ez': '(component Ez) (center (- (+ dpml 3.1) 0x) 0 0) (size 0 winput hsilicon)',
        'parts': {
            'main': {
                'tweak': 'keep',
                'width': {'offset': 0, 'size': 30},
                'length': {'offset': 31, 'size': 30},
            },
            'left_top': {
                'tweak': 'square',
                'width': {'offset': 0, 'size': 3},
                'length': {'offset': 0, 'size': 5}
            },
            'left_bottom': {
                'tweak': 'square',
                'width': {'offset': 27, 'size': 3},
                'length': {'offset': 0, 'size': 5}
            },
            'right_top': {
                'tweak': 'square',
                'width': {'offset': 0, 'size': 3},
                'length': {'offset': 87, 'size': 5}
            },
            'right_bottom': {
                'tweak': 'square',
                'width': {'offset': 27, 'size': 3},
                'length': {'offset': 87, 'size': 5}
            },
        }
    },
    '20x30': {
        'time': '00:30:00',
        'width': 20,
        'length': 30,
        'graphene_length': 3,
        'matlab': '20x30',
        'meep_linput': 2,
        'meep_loutput': 2,
        'meep_input_waveguide': '(center (- (/ (+ dpml linput) 2) 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_output_waveguide': '(center (- (+ dpml linput lPIC (/ (+ loutput dpml) 2)) 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_ez': '(component Ez) (center (- dpml 0x) 0 0) (size 0 winput hsilicon)',
        'parts': {
            'main': {
                'tweak': 'fish_bone',
                'width': {'offset': 0, 'size': 20},
                'length': {'offset': 0, 'size': 30}
            }
        }
    },
    '20x60': {
        'time': '00:30:00',
        'width': 20,
        'length': 60,
        'graphene_length': 6,
        'matlab': '20x60',
        'meep_linput': 2,
        'meep_loutput': 2,
        'meep_input_waveguide': '(center (- (/ (+ dpml linput) 2) 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_output_waveguide': '(center (- (+ dpml linput lPIC (/ (+ loutput dpml) 2)) 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_ez': '(component Ez) (center (- dpml 0x) 0 0) (size 0 winput hsilicon)',
        'parts': {
            'main': {
                'tweak': 'fish_bone',
                'width': {'offset': 0, 'size': 20},
                'length': {'offset': 0, 'size': 60}
            }
        }
    },
    '20x30r': {
        'time': '00:30:00',
        'width': 20,
        'length': 30,
        'graphene_length': 3,
        'matlab': '20x30',
        'meep_linput': 2,
        'meep_loutput': 2,
        'meep_input_waveguide': '(center (- (/ (+ dpml linput) 2) 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_output_waveguide': '(center (- (+ dpml linput lPIC (/ (+ loutput dpml) 2)) 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_ez': '(component Ez) (center (- dpml 0x) 0 0) (size 0 winput hsilicon)',
        'parts': {
            'main': {
                'tweak': 'square',
                'width': {'offset': 0, 'size': 20},
                'length': {'offset': 0, 'size': 30}
            }
        }
    },
    '20x60r': {
        'time': '00:30:00',
        'width': 20,
        'length': 60,
        'graphene_length': 6,
        'matlab': '20x60',
        'meep_linput': 2,
        'meep_loutput': 2,
        'meep_input_waveguide': '(center (- (/ (+ dpml linput) 2) 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_output_waveguide': '(center (- (+ dpml linput lPIC (/ (+ loutput dpml) 2)) 0x) 0 (- (+ dpml wairbound (/ hsilicon 2)) 0z))',
        'meep_ez': '(component Ez) (center (- dpml 0x) 0 0) (size 0 winput hsilicon)',
        'parts': {
            'main': {
                'tweak': 'square',
                'width': {'offset': 0, 'size': 20},
                'length': {'offset': 0, 'size': 60}
            }
        }
    },
}
