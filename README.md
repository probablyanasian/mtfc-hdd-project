# MTFC HDD Project

---

Analysis of Backblaze HDD data to find failure trends.

Data: https://www.backblaze.com/b2/hard-drive-test-data.html

```
<Project Root>/db$ sqlite3 drive_stats.db
sqlite> .read ../create_tables/create_all_tables.sql
sqlite> .read ../imports/import_all_tables.sql
```

