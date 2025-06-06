import sys
import argparse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--infile", type=str, default="-")
    ap.add_argument("-o", "--outfile", type=argparse.FileType("wt"), default=sys.stdout)
    args = ap.parse_args()
    infile = sys.stdin if args.infile == "-" else open(args.infile, "rt")
    outfile = args.outfile
    
    # init indexes
    new_bed_list = []
    prev_start = 0
    prev_end = 0
    prev_score = 0
    prev_length = 0

    for line in infile:
        if line[:5] == "track":
            continue

        # read line
        line = line.strip()
        if not line:
            continue
        hor = line.split("\t")
        start = int(hor[1])
        end = int(hor[2])
        length = end - start
        score = float(hor[4])
        # check if starts or ends match
        if start in range(prev_start - 10, prev_start + 10) or end in range(
            prev_end - 10, prev_end + 10
        ):
            if prev_score - 0.01 < score < prev_score + 0.01:
                # print(start, prev_score, score)
                # scores are same, look at length
                if length > prev_length:
                    new_bed_list.pop()
                else:
                    continue
            elif score > prev_score:
                # delete previous hor if list is not empy
                if len(new_bed_list) > 0:
                    new_bed_list.pop()
            else:
                # don't add current hor
                continue
                # add hor
        new_bed_list.append(line)
        # update indexes
        prev_start = start
        prev_end = end
        prev_score = score
        prev_length = length

    for hor in new_bed_list:
        print(hor.strip(), file=outfile)
    
    infile.close()

if __name__ == "__main__":
    raise SystemExit(main())
