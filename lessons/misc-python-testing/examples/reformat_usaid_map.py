import argparse
import csv

TABLENAME = 'datamaps'
COLUMNS = [
    'Map_Name',
    'Item_Name',
    'Item_Label',
    'Start',
    'Len',
    'Data_Type',
    'Item_Type',
    'Occ',
    'Dec',
    'Dec_Char',
    'Zero_Fill',
    'Values',
    ]

def generate_csv(inf, outf):
    o = csv.writer(outf)
    o.writerow(COLUMNS)
    for row in reformat_data(inf):
        o.writerow([inf.name] + row)

def reformat_data(inp):
    lines = iter(inp)

    # First, find the start of the map records, which we assume for the moment
    # is the line that starts with 'CASEID'.
    for line in lines:
        if line.startswith('CASEID'):
            break
    else:
        print("CASEID record not found")
        return

    while True:
        specline = line.strip()
        values = []
        for line in lines:
            if line[0].strip():
                # Start of next block.
                break
            values.append(line.strip())
        yield reformat_block(specline, values)
        if not line[0].strip() or line.startswith('-------------'):
            # End of data, because either we've seen the line introducing
            # the footer, or 'line' still has the last line in it, that
            # didn't have a non-blank first character.
            break

def reformat_block(specline, values):
    data = reformat_spec_line(specline)
    desc = '\n'.join(values)
    data.append(desc)
    return data

def reformat_spec_line(line):
    qname, qlabel = line[:71].split(None, 1)
    qlabel = qlabel.strip()
    spec = line[71:].split()
    return [qname, qlabel] + spec


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Convert USAID MAP files to csv format")
    parser.add_argument('input_file', type=argparse.FileType('r'),
                        help="USAID MAP file to convert")
    parser.add_argument('output_file', type=argparse.FileType('w'),
                        help="Where to write the transformed data")
    args = parser.parse_args()

    generate_csv(args.input_file, args.output_file)
