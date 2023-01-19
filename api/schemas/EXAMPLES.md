# Example Queries
Minimal query. Age range is given in an array.
```
{
  "biologicalSpecies": "homo sapiens",
  "anatomicalSite": "renal",
  "sex": "F",
  "age": [60, 80]
}
```
More query parameters. When a single age value is given, `ageOption` must be also given as a filter. Additional keywords can be given in `searchTerm` to lookup the dataset description.
```
{
  "biologicalSpecies": "homo sapiens",
  "anatomicalSite": "cutis",
  "sex": "M",
  "age": 30,
  "ageOption": "<",
  "searchTerm": ["melanoma","european"]
}
```
