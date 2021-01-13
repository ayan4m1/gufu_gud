from gufugud import parse
from gufugud import temp
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

parser = argparse.ArgumentParser(description='Compare multiple puffs')
parser.add_argument('paths', nargs='*', required=True)
parser.add_argument('--resistance', '-r', type=float,
                    help='Cold resistance of the atomizer', required=True)
parser.add_argument('--temperature', '--temp', '-t',
                    type=float, help='Set temperature in C')

args = parser.parse_args()

if len(args.paths) < 2:
    raise ValueError(f'Must supply two or more paths! Paths given: {args.paths}')

dfs = []

for path in args.paths:
    # Load each file into a dataframe
    df = pd.read_csv(path)
    # Parse, temp-calculate, and decimate the data
    parse.parse_df(df)
    temp.calculate_temp(df, args.resistance, 'ss316l', 'tfr')
    df = parse.decimate_df(df)
    # Get the series name for the legend
    underscore_pos = path.rindex('_')
    df['name'] = path[0:underscore_pos]
    # Add to list of dataframes
    dfs.append(df)

combined_df = pd.concat(dfs)

# Graph each temp curve against each other
plt.figure(figsize=(32, 18))
pp = sns.relplot(data = combined_df, x='t_quant', y='temp', hue='name', kind='line', markers=False, height=16)
plt.grid(b=True)
if args.temperature
    plt.axhline(linewidth=2, color='r', y=args.temperature)
plt.tight_layout()
plt.savefig('compare.png', dpi=256)
print('Wrote compare.png')
