SELECT x.column_name
FROM (SELECT column_name FROM information_schema.columns AS col
		WHERE table_schema = 'public' AND table_name = {0}
     	ORDER BY ordinal_position ASC) as x
LEFT JOIN (SELECT column_name FROM information_schema.key_column_usage
		WHERE table_schema = 'public' AND table_name = {0}
		AND CONSTRAINT_NAME LIKE '%pkey' OR CONSTRAINT_NAME LIKE '%fkey'
        ORDER BY ordinal_position ASC) AS y
ON x.column_name = y.column_name
WHERE y.column_name is NULL;
