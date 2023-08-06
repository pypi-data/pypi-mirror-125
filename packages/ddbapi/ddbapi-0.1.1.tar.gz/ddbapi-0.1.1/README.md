# Wrapper for the DDB API

- Query the DDB API for Newspapers
- returns a Pandas Dataframe Object

Usage:

```
from ddbapi import zp_api_call

df = zp_api_call(publication_date='[1600-09-01T12:00:00Z TO 1699-12-31T12:00:00Z]')
print(df)
```

Use any combination of these keyword arguments:

- `plainpagefulltext`: Search inside the OCR Fulltext (Use a list for multiple search-words)
- `language`: Use ISO Codes, currently `ger`, `eng`, `fre`, `spa`, `ita`
- `place_of_distribution`: Search inside "Verbreitungsort", use a list for multiple search-words
- `publication_date`: Get newspapers by publication date. Use the following format: `1900-12-31T12:00:00Z` for a specific date, use square brackets and `TO` between two dates to get a daterange like so: `publication_date='[1935-09-01T12:00:00Z TO 1935-09-22T12:00:00Z]'` - time is always `12:00:00Z`.
- `zdb_id`: Search by ZDB-ID
- `provider`: Search by Data Provider
- `paper_title`: Search inside the title of the Newspaper

Values of keyword arguments may contain lists to combine queries.