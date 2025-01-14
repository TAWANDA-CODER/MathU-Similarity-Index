from server.db.connect_db import MySQLDatabase
from datetime import datetime
from server.config import *

import latex2mathml.converter

def resolve_api_status(obj, info):
    return f'API is running'

def resolve_get_all_equations(obj, info):
    # get all equations from database
    sql = "SELECT * FROM mathu_similarity_index_database.problems;"

    db = MySQLDatabase()
    db.set_default()
    db.connect_to_db()
    results = db.execute_query(sql)

    payload = []

    for id, problem in results:
        # print(str(id) + problem)
        payload.append({
            "id": str(id),
            "mathml": problem,
            "latex": problem,
            "type": "unknown",
            "category": "unknown"
        })

    # payload = [
    #     {
    #         "id": 3,
    #         "mathml": f'<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mrow><mn>1</mn><mo>+</mo><mn>2</mn></mrow></math>',
    #         "latex": "1+2",
    #         "type": "Equation",
    #         "category": "Addition"
    #     },
    #     {
    #         "id": 2,
    #         "mathml": f'<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mrow><mn>3</mn><mo>-</mo><mn>2</mn></mrow></math>',
    #         "latex": "3-2",
    #         "type": "Equation",
    #         "category": "Subtraction"
    #     }
    # ]
    return payload

def resolve_search(obj, info, input, islogedin, useremail, apikey):
    print("input:", input, "\tislogedin", islogedin, "\tuseremail", useremail, "\tapikey",apikey)

    sql = "SELECT problem_id, problem, levenshtein2(problem, '" + input + "') AS distance FROM problems ORDER BY distance ASC"
    db = MySQLDatabase()
    db.set_default()
    db.print_config_db()
    db.connect_to_db()
    results = db.execute_query(sql)

    ids = []
    problems = []
    similarities = []
    indexed_problems = []
    for id, problem, similarity in results:
        ids.append(id)
        problems.append(problem)
        similarities.append(similarity)

        # print(id)

        # indexed_prob = {
        #     "id" : id,
        #     "problem" : problem,
        #     "similarity" : similarity
        # }

        # indexed_problems.append(indexed_prob)
    
    db.commit()

    # mark problem for insert problem if not in db
    insert_problem = False
    if similarities[0] > 0:
        insert_problem = True
    
    # sql = "INSERT INTO problems(problem) VALUES('" + input + "');"
    db_insert = MySQLDatabase()
    db_insert.set_default()
    db_insert.print_config_db()
    db_insert.connect_to_db()
    try:
        sql = "INSERT INTO mathu_similarity_index_database.history (user_email, search_input, date_time) VALUES ('" + useremail + "', '" + input + "', '" + str(datetime.now()) + "');"
        print("insert sql: ",sql)
        db_insert.execute_query(sql)
    except:
        print("sql error")
    finally:
        db_insert.commit()

    indexed_problems_len = len(ids)

    min_sim = 0
    max_sim = similarities[indexed_problems_len-1]

    if(max_sim == 0):
        max_sim = 1

    equations = []

    for i in range(indexed_problems_len):
        sim = similarities[i]
        inverse_sim = max_sim - sim
        normalized_sim = inverse_sim / (max_sim) * 100

        similarities[i] = normalized_sim

        equations.append({
            "equation": {
                "id": ids[i],
                "mathml": problems[i],
                "latex": problems[i],
                "type": "unknown",
                "category": "unknown"
            },
            "similarity": similarities[i]
        })
    
    payload = {
        "numberofresults": indexed_problems_len,
        "equations": equations
    }

    # payload = {
    #     "numberofresults": 2,
    #     "equations": [
    #         {
    #             "equation": {
    #                 "id": 1,
    #                 "mathml": "<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mrow><mn>1</mn><mo>+</mo><mn>2</mn></mrow></math>",
    #                 "latex": "1+2",
    #                 "type": "Equation",
    #                 "category": "Addition"
    #             },
    #             "similarity": 0
    #         },
    #         {
    #             "equation": {
    #                 "id": 2,
    #                 "mathml": "<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mrow><mn>3</mn><mo>-</mo><mn>2</mn></mrow></math>",
    #                 "latex": "3-2",
    #                 "type": "Equation",
    #                 "category": "Subtraction"
    #             },
    #             "similarity": 0
    #         }
    #     ]
    # }
    return payload

def resolve_get_user_history(obj, info, useremail, apikey):
    # payload = [{
    #         "id": 3,
    #         "mathml": f'<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mrow><mn>1</mn><mo>+</mo><mn>2</mn></mrow></math>',
    #         "latex": "1+2",
    #         "type": "Equation",
    #         "category": "Addition"
    #     },
    #     {
    #         "id": 2,
    #         "mathml": f'<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mrow><mn>3</mn><mo>-</mo><mn>2</mn></mrow></math>',
    #         "latex": "3-2",
    #         "type": "Equation",
    #         "category": "Subtraction"
    #     }]
    payload = []

    # print(useremail)

    sql = "SELECT * FROM mathu_similarity_index_database.history where user_email LIKE '" + useremail + "' ORDER BY date_time desc;"
    db = MySQLDatabase()
    db.set_default()
    db.connect_to_db()
    results = db.execute_query(sql)

    ids = []
    problems = []
    dates = []
    for id, problem, date in results:
        ids.append(id)
        problems.append(problem)
        dates.append(date)

        eq = {
            "id": 0,
            "mathml": "",
            "latex": problem,
            "type": "Equation",
            "category": "Subtraction"
        }

        payload.append(eq)

    return payload

def resolve_get_all_comments(obj, info):
    payload = [
        {
            "problemid": 0,
            "datetiem": {
                "year": 0,
                "month": 0,
                "day": 0,
                "hour": 0,
                "minute": 0,
                "second": 0,
                "timezone": "",
            },
            "useremail": "test@email.com",
            "comment": "test comment"
        },
        {
            "problemid": 0,
            "datetiem": {
                "year": 0,
                "month": 0,
                "day": 0,
                "hour": 0,
                "minute": 0,
                "second": 1,
                "timezone": "",
            },
            "useremail": "test@email.com",
            "comment": "test comment 2"
        },
        {
            "problemid": 1,
            "datetiem": {
                "year": 0,
                "month": 0,
                "day": 0,
                "hour": 0,
                "minute": 0,
                "second": 1,
                "timezone": "",
            },
            "useremail": "test@email.com",
            "comment": "test comment 3"
        }
    ]
    return payload

def resolve_get_comments(obj, info, problemid):
    payload = [
        {
            "problemid": 0,
            "datetiem": {
                "year": 0,
                "month": 0,
                "day": 0,
                "hour": 0,
                "minute": 0,
                "second": 0,
                "timezone": "",
            },
            "useremail": "test@email.com",
            "comment": "test comment"
        },
        {
            "problemid": 0,
            "datetiem": {
                "year": 0,
                "month": 0,
                "day": 0,
                "hour": 0,
                "minute": 0,
                "second": 1,
                "timezone": "",
            },
            "useremail": "test@email.com",
            "comment": "test comment 2"
        }
    ]
    return payload

def resolve_get_favorite_problems(obj, info, useremail):
    payload = [
        {
            "id": 3,
            "mathml": f'<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mrow><mn>1</mn><mo>+</mo><mn>2</mn></mrow></math>',
            "latex": "1+2",
            "type": "Equation",
            "category": "Addition"
        },
        {
            "id": 2,
            "mathml": f'<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><mrow><mn>3</mn><mo>-</mo><mn>2</mn></mrow></math>',
            "latex": "3-2",
            "type": "Equation",
            "category": "Subtraction"
        }
    ]
    return payload

def resolve_authenticate_login(obj, info, useremail, passwordsalt):
    payload = {
        "success": True,
        "msg": "Login Success",
        "user": {
            "useremail": "test@email.com",
            "username": "none",
            "apikey": "testkey",
            "isadmin": False,
            "darktheme": False
        }
    }
    return payload

def resolve_get_server_settings(obj, info, useremail, apikey):
    payload = {
        "autocaching": True
    }
    return payload