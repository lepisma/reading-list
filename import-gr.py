"""
Import goodreads export to org file

Usage:
  import-gr <gr-csv> <org-file>
"""

import pandas as pd
from docopt import docopt


def append_items(items, fp):
    for it in items:
        # Heading
        fp.write("* ")
        if it["read"]:
            fp.write("READ ")
        fp.write(it["title"] + "\n")

        if it["read"]:
            fp.write("CLOSED: [{}]\n".format(it["read"]))

        fp.write(":PROPERTIES:\n")
        fp.write(":AUTHOR:    {}\n".format(it["author"]))
        fp.write(":ADDED:     <{}>\n".format(it["added"]))
        if it["rating"] > 0:
            rating = ":star:" * it["rating"]
            fp.write(":RATING:     {}\n".format(rating))
        fp.write(":GOODREADS: {}\n".format(it["goodreads"]))
        fp.write(":END:\n\n")

        if it["review"]:
            fp.write(it["review"] + "\n\n")


if __name__ == "__main__":
    args = docopt(__doc__)

    df = pd.read_csv(args["<gr-csv>"])

    for dt_key in ["Date Added", "Date Read"]:
        df[dt_key] = pd.to_datetime(df[dt_key]).dt.strftime("%Y-%m-%d")

    items = []
    for i, row in df.iterrows():
        url = "https://www.goodreads.com/book/show/" + str(row["Book Id"])
        author = row["Author"]
        if not pd.isnull(row["Additional Authors"]):
            author += ", " + row["Additional Authors"]
        items.append({
            "title": row["Title"],
            "author": author,
            "added": row["Date Added"],
            "read": row["Date Read"] if row["Date Read"] != "NaT" else None,
            "rating": row["My Rating"],
            "review": row["My Review"] if not pd.isnull(row["My Review"]) else None,
            "goodreads": url
        })

    with open(args["<org-file>"], "a") as fp:
        append_items(items, fp)
