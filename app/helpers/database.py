import pymysql
import sys
import simplejson as json

# Returns MySQL database connection
def con_db(host, port, user, passwd, db):
    try:
        con = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)

    except pymysql.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    return con


def query_db(con, dict, usercat):
    data_array = []

    # Request args
    category = dict["category"]
    goal = dict["goal"]
    tshirt = dict["tshirt"]
    order_by = dict["order_by"]
    sort = dict["sort"]

    # Query database
    cur = con.cursor()
    cur.execute(
        """
        SELECT body_length, category, goal, tshirt, nlinks
        FROM kickdata
        WHERE tshirt = {0}
        """.format(usercat, category, goal, tshirt, order_by, sort)
    )

    data = cur.fetchall()
    for campaign in data:
        index = {}

        index["body_length"] = campaign[0]
        index["category"] = campaign[1]
        index["goal"] = float(json.dumps(campaign[2]))
        index["tshirt"] = campaign[3]
        index["nlinks"] = float(json.dumps(campaign[4]))

        data_array.append(index)

    cur.close()
    con.close()
    return data_array

