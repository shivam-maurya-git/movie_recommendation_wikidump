import pandas as pd


df = pd.read_csv("movies_new.csv")


df['infobox'] = (
    df["infobox"]
    .str.replace(r"[\'\"\{\},]", "", regex=True)   # remove ', ", { }, ,
    .str.replace(r"\n", " ", regex=True)           # remove newline
    .str.replace(r"<br>", " ", regex=True)    # remove <br>
)
df["vector_text"] = (
    df["infobox"].fillna("").astype(str) +
    " year: " + df["year"].fillna("").astype(str) +
    df["plot"].fillna("").apply(lambda x: f" plot: {x}" if x != "" else "")
)
df.to_csv("movie1.csv")