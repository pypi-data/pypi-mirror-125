UPDATE {}
SET stock_id = sub.num
FROM (
    SELECT id as num
  	FROM stock
  	WHERE symbol = {}
) AS sub
WHERE stock_id IS NULL;
