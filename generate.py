#!/usr/bin/env python3
"""Generate a set of EAGLE footprints for keyboard switches.

This script generates a complete set of Cherry MX switch footprints for various
switch configurations and uses. I wrote it to make generating and changing my
switch footprints manageable.
"""
from collections import OrderedDict
from copy import copy
from decimal import Decimal
from jinja2 import Template
from pprint import pprint

switch_sizes = {
    '1': {},
    '2': {'lstab': -11.9, 'rstab': 11.9, 'tstab': 7, 'bstab': -8.24},
    '4': {'lstab': -28.625, 'rstab': 28.625, 'tstab': 7, 'bstab': -8.24},
    '6': {'lstab': -57.15, 'rstab': 38.1, 'tstab': 7, 'bstab': -8.24},
    '-6': {'lstab': -38.1, 'rstab': 57.15, 'tstab': 7, 'bstab': -8.24},
    '6.25': {'lstab': -50, 'rstab': 50, 'tstab': 7, 'bstab': -8.24},
    '6.5': {'lstab': -52.5, 'rstab': 52.5, 'tstab': 7, 'bstab': -8.24},
    '7': {'lstab': -57.15, 'rstab': 57.15, 'tstab': 7, 'bstab': -8.24}
}
connects = {
    'ALPS': [
        {'gate': 'G$1', 'pin': 'P0', 'pad': 'ALPS1'},
        {'gate': 'G$1', 'pin': 'P1', 'pad': 'ALPS2'}
    ],
    'ALPSMX': [
        {'gate': 'G$1', 'pin': 'P0', 'pad': 'ALPS1 MX1'},
        {'gate': 'G$1', 'pin': 'P1', 'pad': 'ALPS2 MX2'}
    ],
    'MX': [
        {'gate': 'G$1', 'pin': 'P0', 'pad': 'MX1'},
        {'gate': 'G$1', 'pin': 'P1', 'pad': 'MX2'}
    ]
}
package_holes = {
    'ALPS': [],
    'ALPSMX': [
        {'x': '0', 'y': '0', 'diameter': '4'},
        {'x': '-5.08', 'y': '0', 'diameter': '1.7'},
        {'x': '5.08', 'y': '0', 'diameter': '1.7'},
    ],
    'MX': [
        {'x': '0', 'y': '0', 'diameter': '4'},
        {'x': '-5.08', 'y': '0', 'diameter': '1.7'},
        {'x': '5.08', 'y': '0', 'diameter': '1.7'},
    ]
}
package_pads = {
    'ALPS': [
        {'name': 'ALPS1', 'x': '-2.5', 'y': '4', 'drill': '1.3', 'diameter': '2.54'},
        {'name': 'ALPS2', 'x': '2.5', 'y': '4.5', 'drill': '1.3', 'diameter': '2.54'}
    ],
    'ALPSMX': [
        {'name': 'MX1', 'x': '-3.81', 'y': '2.54', 'drill': '1.3', 'diameter': '2.54'},
        {'name': 'MX2', 'x': '2.54', 'y': '5.08', 'drill': '1.3', 'diameter': '2.54'},
        {'name': 'ALPS1', 'x': '-2.5', 'y': '4', 'drill': '1.3', 'diameter': '2.54'},
        {'name': 'ALPS2', 'x': '2.5', 'y': '4.5', 'drill': '1.3', 'diameter': '2.54'}
    ],
    'MX': [
        {'name': 'MX1', 'x': '-3.81', 'y': '2.54', 'drill': '1.3', 'diameter': '2.54'},
        {'name': 'MX2', 'x': '2.54', 'y': '5.08', 'drill': '1.3', 'diameter': '2.54'}
    ]
}
package_wires = {
    'ALPS': [
        {'x1': '7.75', 'y1': '7', 'x2': '7.75', 'y2': '-7', 'width': '0.127', 'layer': '47'},
        {'x1': '7.75', 'y1': '-7', 'x2': '-7.75', 'y2': '-7', 'width': '0.127', 'layer': '47'},
        {'x1': '-7.75', 'y1': '-7', 'x2': '-7.75', 'y2': '7', 'width': '0.127', 'layer': '47'},
        {'x1': '-7.75', 'y1': '7', 'x2': '7.75', 'y2': '7', 'width': '0.127', 'layer': '47'},
    ],
    'ALPSMX': [
        {'x1': '-7', 'y1': '8', 'x2': '7', 'y2': '8', 'width': '0.127', 'layer': '47'},
        {'x1': '7.75', 'y1': '7', 'x2': '7.75', 'y2': '-7', 'width': '0.127', 'layer': '47'},
        {'x1': '7', 'y1': '-8', 'x2': '-7', 'y2': '-8', 'width': '0.127', 'layer': '47'},
        {'x1': '-7.75', 'y1': '-7', 'x2': '-7.75', 'y2': '7', 'width': '0.127', 'layer': '47'},
        {'x1': '-7.75', 'y1': '7', 'x2': '-7', 'y2': '7', 'width': '0.127', 'layer': '47'},
        {'x1': '-7', 'y1': '7', 'x2': '-7', 'y2': '8', 'width': '0.127', 'layer': '47'},
        {'x1': '7', 'y1': '8', 'x2': '7', 'y2': '7', 'width': '0.127', 'layer': '47'},
        {'x1': '7', 'y1': '7', 'x2': '7.75', 'y2': '7', 'width': '0.127', 'layer': '47'},
        {'x1': '7.75', 'y1': '-7', 'x2': '7', 'y2': '-7', 'width': '0.127', 'layer': '47'},
        {'x1': '7', 'y1': '-7', 'x2': '7', 'y2': '-8', 'width': '0.127', 'layer': '47'},
        {'x1': '-7', 'y1': '-8', 'x2': '-7', 'y2': '-7', 'width': '0.127', 'layer': '47'},
        {'x1': '-7', 'y1': '-7', 'x2': '-7.75', 'y2': '-7', 'width': '0.127', 'layer': '47'}
    ],
    'MX': [
        {'x1': '-7', 'y1': '7', 'x2': '7', 'y2': '7', 'width': '0.127', 'layer': '47'},
        {'x1': '7', 'y1': '7', 'x2': '7', 'y2': '-7', 'width': '0.127', 'layer': '47'},
        {'x1': '7', 'y1': '-7', 'x2': '-7', 'y2': '-7', 'width': '0.127', 'layer': '47'},
        {'x1': '-7', 'y1': '-7', 'x2': '-7', 'y2': '7', 'width': '0.127', 'layer': '47'},
    ],
}
devices = {
    'PLAIN': {
        'switch_types': ['ALPS', 'ALPSMX', 'MX'],
        'led': None,
        'diode': False,
        'symbol': {
            'name': 'KEYSWITCH-PLAIN',
            'description': 'A simple keyboard key switch.',
            'wires': [
                {'x1': '-5', 'y1': '5', 'x2': '5', 'y2': '5', 'width': '0.254', 'layer': '94'},
                {'x1': '5', 'y1': '5', 'x2': '5', 'y2': '-5', 'width': '0.254', 'layer': '94'},
                {'x1': '5', 'y1': '-5', 'x2': '-5', 'y2': '-5', 'width': '0.254', 'layer': '94'},
                {'x1': '-5', 'y1': '-5', 'x2': '-5', 'y2': '5', 'width': '0.254', 'layer': '94'},
            ],
            'labels': [
                {'value': '&gt;NAME', 'x': '-4.27', 'y': '2.778', 'size': '1.27', 'layer': '95'}
            ],
            'pins': [
                {'name': 'P0', 'x': '-7.62', 'y': '2.54', 'visible': 'off', 'length': 'short'},
                {'name': 'P1', 'x': '-2.54', 'y': '7.62', 'visible': 'off', 'length': 'short', 'rot': 'R270'}
            ]
        },
    },
    'LED': {
        'switch_types': ['ALPSMX', 'MX'],
        'led': 'single',  # 2 pins, single color LED
        'diode': False,
        'symbol': {
            'name': 'KEYSWITCH-LED',
            'description': 'A simple keyboard key switch with LED support.',
            'wires': [
                {'x1': '-5', 'y1': '5', 'x2': '5', 'y2': '5', 'width': '0.254', 'layer': '94'},
                {'x1': '5', 'y1': '5', 'x2': '5', 'y2': '-5', 'width': '0.254', 'layer': '94'},
                {'x1': '5', 'y1': '-5', 'x2': '-5', 'y2': '-5', 'width': '0.254', 'layer': '94'},
                {'x1': '-5', 'y1': '-5', 'x2': '-5', 'y2': '5', 'width': '0.254', 'layer': '94'},
            ],
            'labels': [
                {'value': '&gt;NAME', 'x': '-4.27', 'y': '2.778', 'size': '1.27', 'layer': '95'}
            ],
            'pins': [
                {'name': 'P0', 'x': '-7.62', 'y': '2.54', 'visible': 'off', 'length': 'short'},
                {'name': 'P1', 'x': '-2.54', 'y': '7.62', 'visible': 'off', 'length': 'short', 'rot': 'R270'},
                {'name': 'LED-', 'x': '7.62', 'y': '-2.54', 'visible': 'off', 'length': 'short', 'rot': 'R180'},
                {'name': 'LED+', 'x': '2.54', 'y': '-7.62', 'visible': 'off', 'length': 'short', 'rot': 'R90'}
            ]
        },
    },
    'RGBLED': {
        'switch_types': ['ALPSMX', 'MX'],
        'led': 'rgb',  # 4 pins, RGB LED
        'diode': False,
        'symbol': {
            'name': 'KEYSWITCH-RGBLED',
            'description': 'A simple keyboard key switch with LED support.',
            'wires': [
                {'x1': '-5', 'y1': '5', 'x2': '5', 'y2': '5', 'width': '0.254', 'layer': '94'},
                {'x1': '5', 'y1': '5', 'x2': '5', 'y2': '-5', 'width': '0.254', 'layer': '94'},
                {'x1': '5', 'y1': '-5', 'x2': '-5', 'y2': '-5', 'width': '0.254', 'layer': '94'},
                {'x1': '-5', 'y1': '-5', 'x2': '-5', 'y2': '5', 'width': '0.254', 'layer': '94'},
            ],
            'labels': [
                {'value': '&gt;NAME', 'x': '-4.27', 'y': '2.778', 'size': '1.27', 'layer': '95'}
            ],
            'pins': [
                {'name': 'P0', 'x': '-7.62', 'y': '2.54', 'visible': 'off', 'length': 'short'},
                {'name': 'P1', 'x': '-2.54', 'y': '7.62', 'visible': 'off', 'length': 'short', 'rot': 'R270'},
                {'name': 'LED+', 'x': '7.62', 'y': '-2.54', 'visible': 'off', 'length': 'short', 'rot': 'R180'},
                {'name': 'R-', 'x': '-2.54', 'y': '-7.62', 'visible': 'off', 'length': 'short', 'rot': 'R90'},
                {'name': 'G-', 'x': '0', 'y': '-7.62', 'visible': 'off', 'length': 'short', 'rot': 'R90'},
                {'name': 'B-', 'x': '2.54', 'y': '-7.62', 'visible': 'off', 'length': 'short', 'rot': 'R90'}
            ]
        },
    },
    'RGBSMDLED': {
        'switch_types': ['ALPSMX', 'MX'],
        'led': 'rgb-smd',  # 4 pins, RGB LED, SMD shining through PCB
        'diode': False,
        'symbol': {
            'name': 'KEYSWITCH-RGBSMDLED',
            'description': 'A simple keyboard key switch with SMD RGB LED support.',
            'wires': [
                {'x1': '-5', 'y1': '5', 'x2': '5', 'y2': '5', 'width': '0.254', 'layer': '94'},
                {'x1': '5', 'y1': '5', 'x2': '5', 'y2': '-5', 'width': '0.254', 'layer': '94'},
                {'x1': '5', 'y1': '-5', 'x2': '-5', 'y2': '-5', 'width': '0.254', 'layer': '94'},
                {'x1': '-5', 'y1': '-5', 'x2': '-5', 'y2': '5', 'width': '0.254', 'layer': '94'},
            ],
            'labels': [
                {'value': '&gt;NAME', 'x': '-4.27', 'y': '2.778', 'size': '1.27', 'layer': '95'}
            ],
            'pins': [
                {'name': 'P0', 'x': '-7.62', 'y': '2.54', 'visible': 'off', 'length': 'short'},
                {'name': 'P1', 'x': '-2.54', 'y': '7.62', 'visible': 'off', 'length': 'short', 'rot': 'R270'},
                {'name': 'LED+', 'x': '7.62', 'y': '-2.54', 'visible': 'off', 'length': 'short', 'rot': 'R180'},
                {'name': 'R-', 'x': '-2.54', 'y': '-7.62', 'visible': 'off', 'length': 'short', 'rot': 'R90'},
                {'name': 'G-', 'x': '0', 'y': '-7.62', 'visible': 'off', 'length': 'short', 'rot': 'R90'},
                {'name': 'B-', 'x': '2.54', 'y': '-7.62', 'visible': 'off', 'length': 'short', 'rot': 'R90'}
            ]
        },
    },
    'SMDLED': {
        'switch_types': ['ALPSMX', 'MX'],
        'led': 'single-smd',  # 2 pins, single color SMD LED
        'diode': False,
        'symbol': {
            'name': 'KEYSWITCH-SMDLED',
            'description': 'A simple keyboard key switch with SMD LED support.',
            'wires': [
                {'x1': '-5', 'y1': '5', 'x2': '5', 'y2': '5', 'width': '0.254', 'layer': '94'},
                {'x1': '5', 'y1': '5', 'x2': '5', 'y2': '-5', 'width': '0.254', 'layer': '94'},
                {'x1': '5', 'y1': '-5', 'x2': '-5', 'y2': '-5', 'width': '0.254', 'layer': '94'},
                {'x1': '-5', 'y1': '-5', 'x2': '-5', 'y2': '5', 'width': '0.254', 'layer': '94'},
            ],
            'labels': [
                {'value': '&gt;NAME', 'x': '-4.27', 'y': '2.778', 'size': '1.27', 'layer': '95'}
            ],
            'pins': [
                {'name': 'P0', 'x': '-7.62', 'y': '2.54', 'visible': 'off', 'length': 'short'},
                {'name': 'P1', 'x': '-2.54', 'y': '7.62', 'visible': 'off', 'length': 'short', 'rot': 'R270'},
                {'name': 'LED-', 'x': '7.62', 'y': '-2.54', 'visible': 'off', 'length': 'short', 'rot': 'R180'},
                {'name': 'LED+', 'x': '2.54', 'y': '-7.62', 'visible': 'off', 'length': 'short', 'rot': 'R90'}
            ]
        },
    },
    'THTSMDLED': {
        'switch_types': ['ALPSMX', 'MX'],
        'led': 'single-tht-smd',  # 2 pins, single color LED, THT or SMD
        'diode': False,
        'symbol': {
            'name': 'KEYSWITCH-THTSMDLED',
            'description': 'A simple keyboard key switch with THT and SMD LED support.',
            'wires': [
                {'x1': '-5', 'y1': '5', 'x2': '5', 'y2': '5', 'width': '0.254', 'layer': '94'},
                {'x1': '5', 'y1': '5', 'x2': '5', 'y2': '-5', 'width': '0.254', 'layer': '94'},
                {'x1': '5', 'y1': '-5', 'x2': '-5', 'y2': '-5', 'width': '0.254', 'layer': '94'},
                {'x1': '-5', 'y1': '-5', 'x2': '-5', 'y2': '5', 'width': '0.254', 'layer': '94'},
            ],
            'labels': [
                {'value': '&gt;NAME', 'x': '-4.27', 'y': '2.778', 'size': '1.27', 'layer': '95'}
            ],
            'pins': [
                {'name': 'P0', 'x': '-7.62', 'y': '2.54', 'visible': 'off', 'length': 'short'},
                {'name': 'P1', 'x': '-2.54', 'y': '7.62', 'visible': 'off', 'length': 'short', 'rot': 'R270'},
                {'name': 'LED-', 'x': '7.62', 'y': '-2.54', 'visible': 'off', 'length': 'short', 'rot': 'R180'},
                {'name': 'LED+', 'x': '2.54', 'y': '-7.62', 'visible': 'off', 'length': 'short', 'rot': 'R90'}
            ]
        },
    },
    'DIODE': {
        'switch_types': ['MX'],
        'led': None,
        'diode': True,
        'symbol': {
            'name': 'KEYSWITCH-DIODE',
            'description': 'A simple keyboard key switch with LED support.',
            'wires': [
                {'x1': '-5', 'y1': '5', 'x2': '5', 'y2': '5', 'width': '0.254', 'layer': '94'},
                {'x1': '5', 'y1': '5', 'x2': '5', 'y2': '-5', 'width': '0.254', 'layer': '94'},
                {'x1': '5', 'y1': '-5', 'x2': '-5', 'y2': '-5', 'width': '0.254', 'layer': '94'},
                {'x1': '-5', 'y1': '-5', 'x2': '-5', 'y2': '5', 'width': '0.254', 'layer': '94'},
            ],
            'labels': [
                {'value': '&gt;NAME', 'x': '-4.27', 'y': '2.778', 'size': '1.27', 'layer': '95'}
            ],
            'pins': [
                {'name': 'P0', 'x': '-7.62', 'y': '2.54', 'visible': 'off', 'length': 'short'},
                {'name': 'P1', 'x': '-2.54', 'y': '7.62', 'visible': 'off', 'length': 'short', 'rot': 'R270'},
                {'name': 'D-', 'x': '7.62', 'y': '-2.54', 'visible': 'off', 'length': 'short', 'rot': 'R180'},
                {'name': 'D+', 'x': '2.54', 'y': '-7.62', 'visible': 'off', 'length': 'short', 'rot': 'R90'}
            ]
        },
    }
}

template = {
    'description': 'Keyboard Keyswitch PCB footprints for MX and Alps switches.',
    'packages': [],
    'symbols': [],
    'devicesets': []
}
packages = OrderedDict()

# Fill in our template entries
for device in sorted(devices):
    template['symbols'].append(devices[device]['symbol'])
    footprints = []
    for switch_type in devices[device]['switch_types']:
        for key_size in sorted(switch_sizes):
            connections = copy(connects[switch_type])
            footprint_name = '-%s-%sU' % (switch_type, key_size)
            if devices[device]['diode']:
                connections.insert(0, {'gate': 'G$1', 'pin': 'D-', 'pad': 'D-'})
                connections.insert(0, {'gate': 'G$1', 'pin': 'D+', 'pad': 'D+'})
                footprint_name = footprint_name + '-DIODE'
            elif devices[device]['led'] == 'rgb':
                connections.insert(0, {'gate': 'G$1', 'pin': 'R-', 'pad': 'R-'})
                connections.insert(0, {'gate': 'G$1', 'pin': 'LED+', 'pad': 'LED+'})
                connections.insert(0, {'gate': 'G$1', 'pin': 'G-', 'pad': 'G-'})
                connections.insert(0, {'gate': 'G$1', 'pin': 'B-', 'pad': 'B-'})
                footprint_name = footprint_name + '-RGB'
            elif devices[device]['led'] == 'single':
                connections.insert(0, {'gate': 'G$1', 'pin': 'LED-', 'pad': 'LED-'})
                connections.insert(0, {'gate': 'G$1', 'pin': 'LED+', 'pad': 'LED+'})
                footprint_name = footprint_name + '-LED'
            elif devices[device]['led'] == 'single-smd':
                connections.insert(0, {'gate': 'G$1', 'pin': 'LED-', 'pad': 'SMDLED-'})
                connections.insert(0, {'gate': 'G$1', 'pin': 'LED+', 'pad': 'SMDLED+'})
                footprint_name = footprint_name + '-SMDLED'
            elif devices[device]['led'] == 'single-tht-smd':
                connections.insert(0, {'gate': 'G$1', 'pin': 'LED-', 'pad': 'LED- SMDLED-'})
                connections.insert(0, {'gate': 'G$1', 'pin': 'LED+', 'pad': 'LED+ SMDLED+'})
                footprint_name = footprint_name + '-THTSMDLED'
            elif devices[device]['led'] == 'rgb-smd':
                connections.insert(0, {'gate': 'G$1', 'pin': 'R-', 'pad': 'R-'})
                connections.insert(0, {'gate': 'G$1', 'pin': 'LED+', 'pad': 'LED+'})
                connections.insert(0, {'gate': 'G$1', 'pin': 'G-', 'pad': 'G-'})
                connections.insert(0, {'gate': 'G$1', 'pin': 'B-', 'pad': 'B-'})
                footprint_name = footprint_name + '-SMDRGB'
            package_name = footprint_name[1:]
            if '--' in package_name:
                package_name = package_name.replace('--', '-REVERSED-')
            packages[package_name] = copy(devices[device])
            packages[package_name].update({'name': package_name, 'device': device, 'switch_type': switch_type, 'size': key_size, 'flipped': 1})
            footprints.append({
                'name': footprint_name,
                'package': package_name,
                'connects': connections
            })
            if key_size != '1':
                footprint_name = footprint_name + '-FLIPPED'
                package_name = package_name + '-FLIPPED'
                packages[package_name] = copy(devices[device])
                packages[package_name].update({'name': package_name, 'device': device, 'switch_type': switch_type, 'size': key_size, 'flipped': -1})
                footprints.append({
                    'name': footprint_name,
                    'package': package_name,
                    'connects': connections
                })
    template['devicesets'].append({
        'name': 'KEYSWITCH-' + device,
        'devices': footprints
    })

schematic_script = []
board_script = ['grid mm 19.05;', 'grid alt mm 4.7625;']
current_x = Decimal('0')
current_x_mm = Decimal('0')
current_y = Decimal('0')
current_y_mm = Decimal('0')
last_row = None

for package in packages:
    pkg = packages[package]
    #pprint(pkg)
    current_row = pkg['symbol']['name'] + '-' + pkg['name'].split('-')[0]
    if current_row != last_row:
        current_x = Decimal('0')
        current_x_mm = Decimal('0')
        current_y += Decimal('1.5')
        current_y_mm += Decimal('38.1')
    last_row = current_row
    if 'FLIPPED' in pkg['name']:
        schematic_script.append('ADD *%s-%s %s (%s -%s);' % (pkg['symbol']['name'], pkg['name'], pkg['name'], current_x, current_y + Decimal('0.75')))
        board_script.append('MOVE %s (%s -%s);' % (pkg['name'], current_x_mm, current_y_mm + Decimal('19.05')))
    current_x += Decimal('0.75')
    if 'FLIPPED' not in pkg['name']:
        current_x_mm += Decimal('19.05') * abs(Decimal(pkg['size']))
        schematic_script.append('ADD *%s-%s %s (%s -%s);' % (pkg['symbol']['name'], pkg['name'], pkg['name'], current_x, current_y))
        board_script.append('MOVE %s (%s -%s);' % (pkg['name'], current_x_mm, current_y_mm))

    template['packages'].append({
        'name': pkg['name'],
        'description': 'Keyboard switch package!',
        'wires': copy(package_wires[pkg['switch_type']]),
        'holes': copy(package_holes[pkg['switch_type']]),
        'pads': copy(package_pads[pkg['switch_type']]),
        'smds': [],
        'labels': []
    })
    if pkg['led'] in ['rgb-smd']:
        template['packages'][-1]['labels'].append({'value': '&gt;NAME', 'x': '0', 'y': '-7', 'size': '1.27', 'layer': '21', 'align': 'center'}),
        template['packages'][-1]['labels'].append({'value': '&gt;NAME', 'x': '0', 'y': '-7', 'size': '1.27', 'layer': '22', 'align': 'center', 'rot': 'MR0'})
    else:
        template['packages'][-1]['labels'].append({'value': '&gt;NAME', 'x': '0', 'y': '-3.175', 'size': '1.27', 'layer': '21', 'align': 'center'}),
        template['packages'][-1]['labels'].append({'value': '&gt;NAME', 'x': '0', 'y': '-3.175', 'size': '1.27', 'layer': '22', 'align': 'center', 'rot': 'MR0'})

    if pkg['diode']:
        template['packages'][-1]['pads'].append({'name': 'D+', 'x': '-3.81', 'y': '-5.08', 'drill': '1', 'diameter': '2'})
        template['packages'][-1]['labels'].append({'value': '+', 'x': '-1.905', 'y': '-5.08', 'size': '1.27', 'layer': '21', 'align': 'center'})
        template['packages'][-1]['labels'].append({'value': '+', 'x': '-1.905', 'y': '-5.08', 'size': '1.27', 'layer': '22', 'align': 'center', 'rot': 'MR0'})
        template['packages'][-1]['pads'].append({'name': 'D-', 'x': '3.81', 'y': '-5.08', 'drill': '1', 'diameter': '2', 'shape': 'square'})
        template['packages'][-1]['labels'].append({'value': '-', 'x': '1.905', 'y': '-5.08', 'size': '1.27', 'layer': '21', 'align': 'center'})
        template['packages'][-1]['labels'].append({'value': '-', 'x': '1.905', 'y': '-5.08', 'size': '1.27', 'layer': '22', 'align': 'center', 'rot': 'MR0'})
    elif pkg['led'] == 'single':
        template['packages'][-1]['pads'].append({'name': 'LED+', 'x': '-1.27', 'y': '-5.08', 'drill': '1', 'diameter': '2'})
        template['packages'][-1]['labels'].append({'value': '+', 'x': '-3.175', 'y': '-5.08', 'size': '1.27', 'layer': '21', 'align': 'center'})
        template['packages'][-1]['labels'].append({'value': '+', 'x': '-3.175', 'y': '-5.08', 'size': '1.27', 'layer': '22', 'align': 'center', 'rot': 'MR0'})
        template['packages'][-1]['pads'].append({'name': 'LED-', 'x': '1.27', 'y': '-5.08', 'drill': '1', 'diameter': '2', 'shape': 'square'})
        template['packages'][-1]['labels'].append({'value': '-', 'x': '3.175', 'y': '-5.08', 'size': '1.27', 'layer': '21', 'align': 'center'})
        template['packages'][-1]['labels'].append({'value': '-', 'x': '3.175', 'y': '-5.08', 'size': '1.27', 'layer': '22', 'align': 'center', 'rot': 'MR0'})
    elif pkg['led'] == 'single-smd':
        template['packages'][-1]['smds'].append({'name': 'SMDLED+', 'x': '-1.3', 'y': '-7.42', 'dx': '2', 'dy': '1.3', 'layer': '1'})
        template['packages'][-1]['labels'].append({'value': '+', 'x': '-3.175', 'y': '-7.42', 'size': '1.27', 'layer': '21', 'align': 'center'})
        template['packages'][-1]['smds'].append({'name': 'SMDLED-', 'x': '1.3', 'y': '-7.42', 'dx': '2', 'dy': '1.3', 'layer': '1'})
        template['packages'][-1]['labels'].append({'value': '-', 'x': '3.175', 'y': '-7.42', 'size': '1.27', 'layer': '21', 'align': 'center'})
    elif pkg['led'] == 'single-tht-smd':
        template['packages'][-1]['pads'].append({'name': 'LED+', 'x': '-1.27', 'y': '-5.08', 'drill': '1', 'diameter': '2'})
        template['packages'][-1]['labels'].append({'value': '+', 'x': '-3.175', 'y': '-5.08', 'size': '1.27', 'layer': '21', 'align': 'center'})
        template['packages'][-1]['labels'].append({'value': '+', 'x': '-3.175', 'y': '-5.08', 'size': '1.27', 'layer': '22', 'align': 'center', 'rot': 'MR0'})
        template['packages'][-1]['pads'].append({'name': 'LED-', 'x': '1.27', 'y': '-5.08', 'drill': '1', 'diameter': '2', 'shape': 'square'})
        template['packages'][-1]['labels'].append({'value': '-', 'x': '3.175', 'y': '-5.08', 'size': '1.27', 'layer': '21', 'align': 'center'})
        template['packages'][-1]['labels'].append({'value': '-', 'x': '3.175', 'y': '-5.08', 'size': '1.27', 'layer': '22', 'align': 'center', 'rot': 'MR0'})
        template['packages'][-1]['smds'].append({'name': 'SMDLED+', 'x': '-1.3', 'y': '-7.42', 'dx': '2', 'dy': '1.3', 'layer': '1'})
        template['packages'][-1]['labels'].append({'value': '+', 'x': '-3.175', 'y': '-7.42', 'size': '1.27', 'layer': '21', 'align': 'center'})
        template['packages'][-1]['smds'].append({'name': 'SMDLED-', 'x': '1.3', 'y': '-7.42', 'dx': '2', 'dy': '1.3', 'layer': '1'})
        template['packages'][-1]['labels'].append({'value': '-', 'x': '3.175', 'y': '-7.42', 'size': '1.27', 'layer': '21', 'align': 'center'})
    elif pkg['led'] == 'rgb-smd':
        template['packages'][-1]['holes'].append({'x': '0', 'y': '-4.5', 'diameter': '2.4'})
        template['packages'][-1]['smds'].append({'name': 'LED+', 'x': '2.1', 'y': '-3.775', 'dx': '1', 'dy': '0.75', 'layer': '16'})
        template['packages'][-1]['smds'].append({'name': 'R-', 'x': '-2.1', 'y': '-3.775', 'dx': '1', 'dy': '0.75', 'layer': '16'})
        template['packages'][-1]['smds'].append({'name': 'G-', 'x': '-2.1', 'y': '-5.225', 'dx': '1', 'dy': '0.75', 'layer': '16'})
        template['packages'][-1]['smds'].append({'name': 'B-', 'x': '2.1', 'y': '-5.225', 'dx': '1', 'dy': '0.75', 'layer': '16'})
        template['packages'][-1]['wires'].append({'x1': '-1.6', 'y1': '-5.9', 'x2': '-1.6', 'y2': '-3.9', 'width': '0.127', 'layer': '22'})
        template['packages'][-1]['wires'].append({'x1': '-0.8', 'y1': '-3.1', 'x2': '-1.6', 'y2': '-3.9', 'width': '0.127', 'layer': '22'})
        template['packages'][-1]['wires'].append({'x1': '-0.8', 'y1': '-3.1', 'x2': '1.6', 'y2': '-3.1', 'width': '0.127', 'layer': '22'})
        template['packages'][-1]['wires'].append({'x1': '1.6', 'y1': '-3.1', 'x2': '1.6', 'y2': '-5.9', 'width': '0.127', 'layer': '22'})
        template['packages'][-1]['wires'].append({'x1': '1.6', 'y1': '-5.9', 'x2': '-1.6', 'y2': '-5.9', 'width': '0.127', 'layer': '22'})
    elif pkg['led'] == 'rgb':
        template['packages'][-1]['pads'].append({'name': 'R-', 'x': '-3.81', 'y': '-5.08', 'drill': '1', 'diameter': '2'})
        template['packages'][-1]['labels'].append({'value': 'R-', 'x': '-3.955', 'y': '-6.985', 'size': '1.27', 'layer': '21', 'align': 'center'})
        template['packages'][-1]['labels'].append({'value': 'R-', 'x': '-3.955', 'y': '-6.985', 'size': '1.27', 'layer': '22', 'align': 'center', 'rot': 'MR0'})
        template['packages'][-1]['pads'].append({'name': 'LED+', 'x': '-1.27', 'y': '-5.08', 'drill': '1', 'diameter': '2', 'shape': 'square'})
        template['packages'][-1]['labels'].append({'value': '+', 'x': '-1.125', 'y': '-6.985', 'size': '1.27', 'layer': '21', 'align': 'center'})
        template['packages'][-1]['labels'].append({'value': '+', 'x': '-1.125', 'y': '-6.985', 'size': '1.27', 'layer': '22', 'align': 'center', 'rot': 'MR0'})
        template['packages'][-1]['pads'].append({'name': 'G-', 'x': '1.27', 'y': '-5.08', 'drill': '1', 'diameter': '2'})
        template['packages'][-1]['labels'].append({'value': 'G-', 'x': '1.125', 'y': '-6.985', 'size': '1.27', 'layer': '21', 'align': 'center'})
        template['packages'][-1]['labels'].append({'value': 'G-', 'x': '1.125', 'y': '-6.985', 'size': '1.27', 'layer': '22', 'align': 'center', 'rot': 'MR0'})
        template['packages'][-1]['pads'].append({'name': 'B-', 'x': '3.81', 'y': '-5.08', 'drill': '1', 'diameter': '2'})
        template['packages'][-1]['labels'].append({'value': 'B-', 'x': '3.955', 'y': '-6.985', 'size': '1.27', 'layer': '21', 'align': 'center'})
        template['packages'][-1]['labels'].append({'value': 'B-', 'x': '3.955', 'y': '-6.985', 'size': '1.27', 'layer': '22', 'align': 'center', 'rot': 'MR0'})

    if pkg['size'] != '1':
        c = switch_sizes[pkg['size']]
        template['packages'][-1]['holes'].append({'x': c['lstab'], 'y': c['tstab']*pkg['flipped'], 'diameter': '3.05'})
        template['packages'][-1]['holes'].append({'x': c['rstab'], 'y': c['tstab']*pkg['flipped'], 'diameter': '3.05'})
        template['packages'][-1]['holes'].append({'x': c['lstab'], 'y': c['bstab']*pkg['flipped'], 'diameter': '4'})
        template['packages'][-1]['holes'].append({'x': c['rstab'], 'y': c['bstab']*pkg['flipped'], 'diameter': '4'})

if __name__ == '__main__':
    t = Template(open('Keyboard.lbr.jinja2').read())
    with open('Keyboard.lbr', 'w') as fd:
        fd.seek(0, 0)
        fd.write(t.render(**template))

    print('*** You can use this script to add every single footprint to a schematic:')
    print('\n'.join(schematic_script))
    print('\n\n\n\n\n')
    print('*** You can use this script to place every single footprint on a board:')
    print('\n'.join(board_script))
