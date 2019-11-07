# CockroachDB keyset pagination example

NOTE: This is unofficial - no warranties.  For official docs, see <https://www.cockroachlabs.com/docs>.

Uses [CockroachDB][crdb] and the [employees data set][employees].

Based on descriptions of keyset pagination (aka the "seek method") in:

<https://www.citusdata.com/blog/2016/03/30/five-ways-to-paginate/>

<https://blog.jooq.org/2013/10/26/faster-sql-paging-with-jooq-using-the-seek-method/>

## Dependencies

Written in Python 3.  Uses the following libraries:

- [psycopg2][psycopg2]

Install with:

    $ pip3 install psycopg2

## Get started

Start a local cluster with:

    $ cockroach demo

Start the SQL shell:

    $ cockroach sql --insecure

From the SQL shell, import the [employees data set][employees] as follows:

    > CREATE DATABASE employees;
    > USE employees;
    > IMPORT MYSQLDUMP 'https://s3-us-west-1.amazonaws.com/cockroachdb-movr/datasets/employees-db/mysqldump/employees-full.sql.gz';

Back in the UNIX shell, run the script as shown below.  Make sure to pass the port the demo cluster is using to the script (in this case, it's 49459).

    $ python3 pagination.py -p 49459 # or --port

You should see output like:

    DEBUG:root:------------------------------------------------
    DEBUG:root:paginate_aux.count = 0
    DEBUG:root:paginate_aux.page_count = 8
    DEBUG:root:sql:
    SELECT * FROM employees
      WHERE employees.emp_no > 10000
      ORDER BY employees.emp_no ASC
      LIMIT 5;

    DEBUG:root:paginate_aux(10000, 5) -->
    DEBUG:root:        {'emp_no': 10001, 'birth_date': datetime.date(1953, 9, 2), 'first_name': 'Georgi', 'last_name': 'Facello', 'gender': 'M', 'hire_date': datetime.date(1986, 6, 26)}
    DEBUG:root:        {'emp_no': 10002, 'birth_date': datetime.date(1964, 6, 2), 'first_name': 'Bezalel', 'last_name': 'Simmel', 'gender': 'F', 'hire_date': datetime.date(1985, 11, 21)}
    DEBUG:root:        {'emp_no': 10003, 'birth_date': datetime.date(1959, 12, 3), 'first_name': 'Parto', 'last_name': 'Bamford', 'gender': 'M', 'hire_date': datetime.date(1986, 8, 28)}
    DEBUG:root:        {'emp_no': 10004, 'birth_date': datetime.date(1954, 5, 1), 'first_name': 'Chirstian', 'last_name': 'Koblick', 'gender': 'M', 'hire_date': datetime.date(1986, 12, 1)}
    DEBUG:root:        {'emp_no': 10005, 'birth_date': datetime.date(1955, 1, 21), 'first_name': 'Kyoichi', 'last_name': 'Maliniak', 'gender': 'M', 'hire_date': datetime.date(1989, 9, 12)}
    DEBUG:root:------------------------------------------------
    DEBUG:root:paginate_aux.count = 1
    DEBUG:root:paginate_aux.page_count = 8
    DEBUG:root:sql:
    SELECT * FROM employees
      WHERE employees.emp_no > 10005
      ORDER BY employees.emp_no ASC
      LIMIT 5;

    DEBUG:root:paginate_aux(10005, 5) -->
    DEBUG:root:        {'emp_no': 10006, 'birth_date': datetime.date(1953, 4, 20), 'first_name': 'Anneke', 'last_name': 'Preusig', 'gender': 'F', 'hire_date': datetime.date(1989, 6, 2)}
    DEBUG:root:        {'emp_no': 10007, 'birth_date': datetime.date(1957, 5, 23), 'first_name': 'Tzvetan', 'last_name': 'Zielinski', 'gender': 'F', 'hire_date': datetime.date(1989, 2, 10)}
    DEBUG:root:        {'emp_no': 10008, 'birth_date': datetime.date(1958, 2, 19), 'first_name': 'Saniya', 'last_name': 'Kalloufi', 'gender': 'M', 'hire_date': datetime.date(1994, 9, 15)}
    DEBUG:root:        {'emp_no': 10009, 'birth_date': datetime.date(1952, 4, 19), 'first_name': 'Sumant', 'last_name': 'Peac', 'gender': 'F', 'hire_date': datetime.date(1985, 2, 18)}
    DEBUG:root:        {'emp_no': 10010, 'birth_date': datetime.date(1963, 6, 1), 'first_name': 'Duangkaew', 'last_name': 'Piveteau', 'gender': 'F', 'hire_date': datetime.date(1989, 8, 24)}

    ... snip ...

    OK: First 40 IDs returned match expected output


[psycopg2]: https://pypi.org/project/psycopg2/
[employees]: https://github.com/datacharmer/test_db
[crdb]: https://www.cockroachlabs.com
