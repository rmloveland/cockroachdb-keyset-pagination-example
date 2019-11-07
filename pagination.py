#!python3

import psycopg2
import psycopg2.errorcodes
import logging
import argparse


def get_page_of_employees(conn, emp_no, limit):
    # The employee ID returned should be the value passed to the
    # `get_next_page()` function.
    sqltext = '''
SELECT * FROM employees
  WHERE employees.emp_no > {}
  ORDER BY employees.emp_no ASC
  LIMIT {};
'''
    query = sqltext.format(emp_no, limit)
    answer = []
    with conn.cursor() as cur:
        rowcount = cur.execute(query)
        logging.debug("sql: {}".format(query))
        # logging.debug("get_page_of_employees(): status message: {}"
        #               .format(cur.statusmessage))
        if rowcount is None:
            answer = [dict(zip([column[0] for column in cur.description], row))
                      for row in cur.fetchall()]
        conn.commit()
    return answer


# for checking unique IDs
seen = {}
seen_prime = {}


def get_first_forty_ids(conn):
    query = '''
SELECT * FROM employees
  ORDER BY employees.emp_no ASC
  LIMIT 40;
'''
    answer = []
    with conn.cursor() as cur:
        rowcount = cur.execute(query)
        logging.debug("get_first_forty_ids(): status message: {}"
                      .format(cur.statusmessage))
        if rowcount is None:
            answer = [dict(zip([column[0] for column in cur.description], row))
                      for row in cur.fetchall()]
        conn.commit()
    for a in answer:
        id = a['emp_no']
        seen_prime[id] = 1


def paginate(conn, start, page_count):
    count = 0
    limit = 5

    def paginate_aux(conn, start, count, limit, page_count):
        logging.debug('------------------------------------------------')
        logging.debug("paginate_aux.count = {}".format(count))
        logging.debug("paginate_aux.page_count = {}".format(page_count))
        if count == page_count:
            return
        page = get_page_of_employees(conn, start, limit)
        if page:
            sorted_page = sorted(page, key=lambda kv: kv['emp_no'])
            logging.debug("paginate_aux({}, {}) --> ".format(start, limit))
            for sp in sorted_page:
                logging.debug("        {}".format(sp))
            last = page[-1]
            for p in page:
                # process results here
                id = p['emp_no']
                seen[id] = 1
                if p is last:
                    # If this is the last element, capture the start_time for the next
                    # page
                    start = p['emp_no']
                    paginate_aux(conn, start, count + 1, limit, page_count)
        else:
            return

    paginate_aux(conn, start, count, limit, page_count)


def main(args):
    PORT = args.port

    dsn = 'postgresql://root@localhost:{}/employees?sslmode=disable'.format(PORT)
    conn = psycopg2.connect(dsn)

    log_level = getattr(logging, 'DEBUG', None)
    logging.basicConfig(level=log_level)

    try:
        paginate(conn, 10000, 8)          # 10001 is the first / lowest employee ID.
        get_first_forty_ids(conn)

        # Code below was used during debugging, and is not necessary once
        # pagination is returning correct results.

        # print('------------------------------------------------')
        # print('First 40 IDs seen during pagination')
        # for k in seen.keys():
        #     print(k)

        # print('------------------------------------------------')
        # print('First 40 actual IDs')
        # for k in seen_prime.keys():
        #     print(k)

        if set(seen.keys()) == set(seen_prime.keys()):
            print('OK: First 40 IDs returned match expected output')
        else:
            print('NOT OK: First 40 IDs returned DO NOT match expected output')

    except ValueError as ve:
        # Below, we print the error and continue on so this example is easy to
        # run (and run, and run...).  In real code you should handle this error
        # and any others thrown by the database interaction.
        logging.debug(" failed: {}".format(ve))
        pass

    # Close communication with the database.
    conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port')
    args = parser.parse_args()
    main(args)
