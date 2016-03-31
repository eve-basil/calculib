class IndustryException(Exception):
    pass

decryptors = [{id: 123456, 'name': 'Accelerant', 'runs': 1, 'me': 2, 'te': 10,
               'chance': 20},
              {id: 123456, 'name': 'Attainment', 'runs': 4, 'me': -1, 'te': 4,
               'chance': 80},
              {id: 123456, 'name': 'Augmentation', 'runs': 9, 'me': -2,
               'te': 2, 'chance': -40},
              {id: 123456, 'name': 'Parity', 'runs': 3, 'me': 1, 'te': -2,
               'chance': 50},
              {id: 123456, 'name': 'Process', 'runs': 0, 'me': 3, 'te': 6,
               'chance': 10},
              {id: 123456, 'name': 'Symmetry', 'runs': 2, 'me': 1, 'te': 8,
               'chance': 0},
              {id: 123456, 'name': 'Optimized Attainment', 'runs': 2, 'me': 1,
               'te': -2, 'chance': 90},
              {id: 123456, 'name': 'Optimized Augmentation', 'runs': 7,
               'me': 2, 'te': 0, 'chance': -10}]

skills = {'science': {3403: 'Research',
                      3409: 'Metallurgy',
                      3402: 'Science',
                      3406: 'Laboratory Operation',
                      3409: 'Metallurgy',
                      3408: 'Sleeper Encryption Methods',
                      11447: 'Laser Physics',
                      11433: 'High Enery Physics',
                      11441: 'Plasma Physics',
                      11442: 'Nanite Engineering',
                      11443: 'Hydromagnetic Physics',
                      11444: 'Amarr Starship Engineering',
                      11445: 'Minmatar Starship Engineering',
                      11446: 'Graviton Physics',
                      11448: 'Electromagnetic Physics',
                      11449: 'Rocket Science',
                      11450: 'Gallente Starship Engineering',
                      11451: 'Nuclear Physics',
                      11452: 'Mechanical Engineering',
                      11453: 'Electronic Engineering',
                      11454: 'Caldari Starship Engineering',
                      11455: 'Quantum Physics',
                      11487: 'Astronautic Engineering',
                      11529: 'Molecular Engineering',
                      11858: 'Hypernet Science',
                      12179: 'Research Project Management',
                      20433: 'Talocan Technology',
                      21789: 'Sleeper Technology',
                      21790: 'Caldari Encryption Methods',
                      21791: 'Minmatar Encryption Methods',
                      23087: 'Amarr Encryption Methods',
                      23121: 'Gallente Encryption Methods',
                      23123: 'Takmahl Technology',
                      23124: 'Yan Jung Technology',
                      24270: 'Scientific Networking',
                      24624: 'Advanced Laboratory Operation',
                      30324: 'Defensive Subsystem Technology',
                      30325: 'Engineering Subsystem Technology',
                      30326: 'Electronic Subsystem Technology',
                      30327: 'Offensive Subsystem Technology',
                      30788: 'Propulsion Subsystem Technology'}}
