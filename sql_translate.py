import sqlglot

def translate(sql: str, source: str = None) -> str:
    return sqlglot.transpile(sql, read=source, write="postgres", pretty=True)[0]

def section(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)

def show(label: str, sql: str, source: str = None) -> None:
    print(f"\n-- {label}")
    print(f"-- Source ({source or 'generic'}):")
    print(sql.strip())
    print(f"-- Translated (postgres):")
    print(translate(sql, source))


# ── 1. Data types ────────────────────────────────────────────────
section("1. Data Types")

show("INT AUTO_INCREMENT -> SERIAL", """
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    created_at DATETIME
)
""", source="mysql")

show("TINYINT / MEDIUMTEXT (MySQL)", """
CREATE TABLE posts (
    id     BIGINT AUTO_INCREMENT PRIMARY KEY,
    body   MEDIUMTEXT,
    active TINYINT(1) DEFAULT 1
)
""", source="mysql")


# ── 2. String functions ──────────────────────────────────────────
section("2. String Functions")

show("IFNULL -> COALESCE", """
SELECT IFNULL(email, 'unknown') AS email FROM users
""", source="mysql")

show("GROUP_CONCAT -> STRING_AGG", """
SELECT department, GROUP_CONCAT(name ORDER BY name SEPARATOR ', ') AS members
FROM employees
GROUP BY department
""", source="mysql")

show("DATE_FORMAT -> TO_CHAR", """
SELECT DATE_FORMAT(created_at, '%Y-%m') AS month FROM orders
""", source="mysql")


# ── 3. Limiting rows ─────────────────────────────────────────────
section("3. LIMIT / TOP")

show("LIMIT with OFFSET (generic)", """
SELECT id, name FROM products
ORDER BY price DESC
LIMIT 10 OFFSET 20
""")

show("TOP (T-SQL / SQL Server)", """
SELECT TOP 5 id, name, salary FROM employees ORDER BY salary DESC
""", source="tsql")


# ── 4. Conditional logic ─────────────────────────────────────────
section("4. Conditional Logic")

show("IF() -> CASE WHEN", """
SELECT name, IF(score >= 50, 'pass', 'fail') AS result FROM students
""", source="mysql")

show("IIF (T-SQL) -> CASE WHEN", """
SELECT name, IIF(active = 1, 'active', 'inactive') AS status FROM users
""", source="tsql")


# ── 5. JSON functions ────────────────────────────────────────────
section("5. JSON Functions")

show("JSON_EXTRACT (MySQL) -> -> operator", """
SELECT JSON_EXTRACT(metadata, '$.color') AS color FROM products
""", source="mysql")


# ── 6. Date arithmetic ───────────────────────────────────────────
section("6. Date Arithmetic")

show("DATE_ADD -> INTERVAL syntax", """
SELECT DATE_ADD(created_at, INTERVAL 7 DAY) AS expires_at FROM subscriptions
""", source="mysql")

show("DATEDIFF (MySQL)", """
SELECT DATEDIFF(end_date, start_date) AS duration FROM projects
""", source="mysql")


# ── 7. Upsert ────────────────────────────────────────────────────
section("7. Upsert")

show("INSERT IGNORE (MySQL) -> ON CONFLICT DO NOTHING", """
INSERT IGNORE INTO users (email, name) VALUES ('a@b.com', 'Alice')
""", source="mysql")


# ── 8. Parsing without translation ──────────────────────────────
section("8. Parse & Inspect AST (no translation)")

sql = "SELECT id, SUM(amount) AS total FROM orders WHERE status = 'paid' GROUP BY id"
ast = sqlglot.parse_one(sql)

print(f"\nSQL: {sql}")
print(f"Tables referenced : {[t.name for t in ast.find_all(sqlglot.exp.Table)]}")
print(f"Columns selected  : {[c.alias_or_name for c in ast.find_all(sqlglot.exp.Column)]}")
print(f"Aggregations      : {[str(a) for a in ast.find_all(sqlglot.exp.AggFunc)]}")
