materials = {

"3-tab Asphalt": {
    "failure_mode": "bruise",
    "damage_type": "functional",
    "threshold": 1.0,
    "relative_hardness": 2,
    "brittleness": 3,
    "damage_sensitivity": 1.0
},

"Architectural Asphalt Shingles": {
    "failure_mode": "bruise",
    "damage_type": "functional",
    "threshold": 1.25,
    "relative_hardness": 3,
    "brittleness": 3,
    "damage_sensitivity": 0.90
},

"Impact Resistant Shingles": {
    "failure_mode": "bruise",
    "damage_type": "functional",
    "threshold": 2.00,
    "relative_hardness": 5,
    "brittleness": 2,
    "damage_sensitivity": 0.60
},

"Standing Seam Steel": {
    "failure_mode": "dent",
    "damage_type": "cosmetic",
    "threshold": 2.50,
    "relative_hardness": 8,
    "brittleness": 1,
    "damage_sensitivity": 0.55
},

"Corrugated Steel": {
    "failure_mode": "dent",
    "damage_type": "cosmetic",
    "threshold": 2.25,
    "relative_hardness": 7,
    "brittleness": 2,
    "damage_sensitivity": 0.60
},

"Aluminum Roofing": {
    "failure_mode": "dent",
    "damage_type": "cosmetic",
    "threshold": 1.75,
    "relative_hardness": 5,
    "brittleness": 2,
    "damage_sensitivity": 0.80
},

"Copper Roofing": {
    "failure_mode": "dent",
    "damage_type": "cosmetic",
    "threshold": 1.50,
    "relative_hardness": 4,
    "brittleness": 2,
    "damage_sensitivity": 0.85
},

"Clay Tile": {
    "failure_mode": "fracture",
    "damage_type": "functional",
    "threshold": 1.50,
    "relative_hardness": 9,
    "brittleness": 10,
    "damage_sensitivity": 0.90
},

"Concrete Tile": {
    "failure_mode": "fracture",
    "damage_type": "functional",
    "threshold": 1.75,
    "relative_hardness": 8,
    "brittleness": 8,
    "damage_sensitivity": 0.75
},

"Slate": {
    "failure_mode": "fracture",
    "damage_type": "functional",
    "threshold": 2.00,
    "relative_hardness": 10,
    "brittleness": 10,
    "damage_sensitivity": 0.90
},

"Wood Shake": {
    "failure_mode": "split",
    "damage_type": "functional",
    "threshold": 1.50,
    "relative_hardness": 4,
    "brittleness": 7,
    "damage_sensitivity": 0.90
}

}

exterior_materials = {

"Aluminum Gutters": {
    "failure_mode": "dent",
    "damage_type": "cosmetic",
    "threshold": 1.00,
    "relative_hardness": 6,
    "brittleness": 2,
    "damage_sensitivity": 1.00
},

"Steel Gutters": {
    "failure_mode": "dent",
    "damage_type": "cosmetic",
    "threshold": 1.50,
    "relative_hardness": 6,
    "brittleness": 2,
    "damage_sensitivity": 0.75
},

"Vinyl Siding": {
    "failure_mode": "crack",
    "damage_type": "functional",
    "threshold": 1.50,
    "relative_hardness": 4,
    "brittleness": 6,
    "damage_sensitivity": 0.80
},

"Fiber Cement Siding": {
    "failure_mode": "fracture",
    "damage_type": "functional",
    "threshold": 2.00,
    "relative_hardness": 8,
    "brittleness": 8,
    "damage_sensitivity": 0.55
},

"Brick": {
    "failure_mode": "chip",
    "damage_type": "cosmetic",
    "threshold": 2.50,
    "relative_hardness": 9,
    "brittleness": 9,
    "damage_sensitivity": 0.30
},

"Stucco": {
    "failure_mode": "crack",
    "damage_type": "functional",
    "threshold": 1.75,
    "relative_hardness": 7,
    "brittleness": 8,
    "damage_sensitivity": 0.65
}

}

vehicle_materials = {

"Steel Body Panel": {
    "failure_mode": "dent",
    "damage_type": "cosmetic",
    "threshold": 1.75,
    "relative_hardness": 8,
    "brittleness": 1,
    "damage_sensitivity": 0.70
},

"Aluminum Body Panel": {
    "failure_mode": "dent",
    "damage_type": "cosmetic",
    "threshold": 1.50,
    "relative_hardness": 6,
    "brittleness": 2,
    "damage_sensitivity": 0.85
},

"Tempered Glass": {
    "failure_mode": "shatter",
    "damage_type": "functional",
    "threshold": 2.50,
    "relative_hardness": 10,
    "brittleness": 10,
    "damage_sensitivity": 0.25
},

"Laminated Windshield": {
    "failure_mode": "crack",
    "damage_type": "functional",
    "threshold": 3.00,
    "relative_hardness": 10,
    "brittleness": 9,
    "damage_sensitivity": 0.20
},

"Plastic Bumper": {
    "failure_mode": "crack",
    "damage_type": "cosmetic",
    "threshold": 2.00,
    "relative_hardness": 5,
    "brittleness": 5,
    "damage_sensitivity": 0.50
},

"Carbon Fiber Panel": {
    "failure_mode": "fracture",
    "damage_type": "functional",
    "threshold": 2.25,
    "relative_hardness": 9,
    "brittleness": 8,
    "damage_sensitivity": 0.40
}

}

all_materials = {}
all_materials.update(materials)
all_materials.update(exterior_materials)
all_materials.update(vehicle_materials)
