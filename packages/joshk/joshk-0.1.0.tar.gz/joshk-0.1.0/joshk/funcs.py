import requests
import json
import os
import re

EXAMPLE_TEXT_IN="""@article{Pecci2019,
   abstract = {This manuscript investigates the problem of optimal placement of control valves in water supply networks, where the objective is to minimize average zone pressure. The problem formulation results in a nonconvex mixed integer nonlinear program (MINLP). Due to its complex mathematical structure, previous literature has solved this nonconvex MINLP using heuristics or local optimization methods, which do not provide guarantees on the global optimality of the computed valve configurations. In our approach, we implement a branch and bound method to obtain certified bounds on the optimality gap of the solutions. The algorithm relies on the solution of mixed integer linear programs, whose formulations include linear relaxations of the nonconvex hydraulic constraints. We investigate the implementation and performance of different linear relaxation schemes. In addition, a tailored domain reduction procedure is implemented to tighten the relaxations. The developed methods are evaluated using two benchmark water supply networks and an operational water supply network from the UK. The proposed approaches are shown to outperform state-of-the-art global optimization solvers for the considered benchmark water supply networks. The branch and bound algorithm converges to good quality feasible solutions in most instances, with bounds on the optimality gap that are comparable to the level of parameter uncertainty usually experienced in water supply network models.},
   author = {Filippo Pecci and Edo Abraham and Ivan Stoianov},
   doi = {10.1007/s11081-018-9412-7},
   issn = {15732924},
   issue = {2},
   journal = {Optimization and Engineering},
   keywords = {Global optimization,Mixed-integer nonlinear programming,Pressure management,Valve placement,Water supply networks},
   month = {6},
   pages = {457-495},
   publisher = {Springer New York LLC},
   title = {Global optimality bounds for the placement of control valves in water supply networks},
   volume = {20},
   year = {2019},
}
"""


def txt_to_json(txt):
   txt = re.sub(r"^@.*?,","", txt)
   txt = re.sub(r"\n   ","", txt)
   txt = txt.replace('{','"').replace('}','"').replace('=',':')
   txt = re.sub(',\n"\n', '', txt)

   txt ='{"'+txt+'}'
   txt = txt.replace('",','","')
   txt = txt.replace(' : ','":')
   
   return json.loads(txt)

def to_properties(bibtext_d):

    properties = {
        "properties":{
            "Name":{
                "title": [
                    {
                        "text":{
                            "content": bibtext_d['title']
                        }
                    }
                ]
            },
            "authors":{
                "multi_select":[{'name':keyword} for keyword in bibtext_d['author'].split(' and ')]
            },
            # ! Should go in body
            # "abstract":{
            #     "rich_text": [
            #         {
            #             "text":{
            #                 "content":bibtext_d['abstract']
            #             }
            #         }
            #     ]
            # },
            "doi":{
                "url": bibtext_d['doi']
            },
            "issn":{
                "number": int(bibtext_d['issn'])
            },
            "issue":{
                "number": int(bibtext_d['issue'])
            },
            "journal":{
                "rich_text": [
                    {
                        "text":{
                            "content":bibtext_d['journal']
                        }
                    }
                ]
            },
            "month":{
                "number": int(bibtext_d['month'])
            },
            "year":{
                "number": int(bibtext_d['year'])
            },
            "pages":{
                "rich_text": [
                    {
                        "text":{
                            "content":bibtext_d['pages']
                        }
                    }
                ]
            },
            "publisher":{
                "rich_text": [
                    {
                        "text":{
                            "content":bibtext_d['publisher']
                        }
                    }
                ]
            },
            "volume":{
                "number": int(bibtext_d['volume'])
            },
            "Tags":{
                "multi_select":[{'name':keyword} for keyword in bibtext_d['keywords'].split(',')]
            }

        }
            
    }
    return properties


def make_request(properties):

    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {os.getenv('NOTION_KEY')}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-08-16"
    }

    data = {
        "parent": {"database_id": f"{os.getenv('NOTION_DATABASE_ID')}"},
        **properties
    }
    data=json.dumps(data)
    r = requests.post(url, data=data, headers=headers)
    print(r.status_code)
    if r.status_code!=200:
        print(r.content)