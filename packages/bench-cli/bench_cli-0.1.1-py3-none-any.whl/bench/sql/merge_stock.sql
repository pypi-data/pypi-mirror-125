WITH tmp AS (SELECT {0} FROM tstock WHERE symbol = {1})
INSERT INTO stock AS prod ({0})
SELECT * FROM tmp
  ON CONFLICT (symbol) DO UPDATE
  SET last_updated = excluded.last_updated;
