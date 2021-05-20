from datetime import datetime
import argparse
import math
import msgpack
import numpy as np
import pandas as pd
import scipy.interpolate as interp
import scipy.signal as signal
import seaborn as sns
import serial
import sys

parser = argparse.ArgumentParser(description='Log gufu_gud data.')
parser.add_argument('device', help='Device name')
parser.add_argument('--port', '-p', help='Serial port to communicate over', required=True)

args = parser.parse_args()

filename = f'{args.device}_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.csv'

print("Press Ctrl-C to finish data collection!", flush=True)

# Configure Serial port with 100 ms timeout
ser = serial.Serial(args.port, timeout=0.1)

# Configure msgpack unpacker for data stream decode
unpacker = msgpack.Unpacker(raw=False)
data_list = []

try:
    while True:
        # Read some bytes in
        buf = ser.read(256)

        if not buf:
            # Try again later
            continue

        # Feed data to deserialization
        unpacker.feed(buf)

        try:
            # Process new objects
            for obj in unpacker:
                if not isinstance(obj, dict):
                    # We only want dicts!
                    print(f'Rejecting {obj}', flush=True)
                    break

                if 'debug' in obj:
                    # Debug message, display it but don't save it
                    print(f'DEBUG: {obj}', flush=True)
                else:
                    # Save data
                    data_list.append(obj)
        except (msgpack.ExtraData, msgpack.OutOfData, msgpack.FormatError, msgpack.StackError, UnicodeDecodeError) as ex:
            # These should all be (maybe?) ok?
            print(ex)
            continue
except KeyboardInterrupt:
    print(f'Captured {len(data_list)} frames')

    # Make dataframe
    df = pd.DataFrame(data_list)
    # Add power calc
    df['p'] = df['v'] * df['i']
    # Remove bias, create elapsed time
    df['t'] -= df.t.iloc[0]
    # Shift t=0 to the start of the puff (first time when power > half the max power in the data)
    df.t -= df[df.p.gt(df.p.max() / 2.0)].t.iloc[0]

    df.to_csv(filename)
    print(f'Wrote {filename}')