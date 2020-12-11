import re


if __name__ == "__main__":

    with open("data/quote_fields.txt", "r") as infile, open("./tmp.txt", "w") as outfile:
        for line in infile:
            match = re.search(r"\s(?P<field>\w+)\s\w+,", line)
            if match is not None:
                outfile.write(f"EXCLUDED.{match.group('field')}, ")
