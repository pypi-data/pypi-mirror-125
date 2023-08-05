-- most commits
SELECT
    repo_path,
    count(*)
FROM raw
GROUP BY repo_path
ORDER BY 2 DESC
;

-- latest commits
SELECT
    dt,
    repo_path,
    file_path
FROM raw
ORDER BY dt DESC
;

