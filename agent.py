import sqlite3
from datetime import datetime,timedelta
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client=Groq()
DB_PATH="business.db"

def get_schema():
    conn=sqlite3.connect(DB_PATH)
    cursor=conn.cursor()
    cursor.execute("select name from sqlite_master where type='table'")
    tables=cursor.fetchall()
    schema=""
    for (table_name,) in tables:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns=cursor.fetchall()
        col_defs=",".join(f"{col[1]}{col[2]}" for col in columns)
        schema+=f"Table: {table_name}\nColumns:{col_defs}\n\n"
    conn.close()
    return schema

def run_sql(query:str):
    try:
        conn=sqlite3.connect(DB_PATH)
        cursor=conn.cursor()
        cursor.execute(query)
        rows=cursor.fetchall()
        columns=[desc[0] for desc in cursor.description] if cursor.description else []
        conn.close()
        return {"columns":columns,"rows":rows,"error":None}
    except Exception as e:
        return {"columns":[],"rows":[],"error":str(e)}
    
def ask_query(question:str):
    schema=get_schema()
    today=datetime.now().strftime("%Y-%m-%d")

    tools=[
        {
            "type":"function",
            "function":{
                "name":"run_sql",
                "description":"It Runs a query on the business database and gives response in human language",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "query":{
                            "type":"string",
                            "description":"Valid SQL Query"
                        }
                    },
                    "required":["query"]
                }
            }
        }
    ]

    system_prompt=f"""You are an SQL Expert Assistant.
    You have access to a business database. Use the run_sql tool to answer questions.Always use
    the tool- never guess or make up data.

    Today's date is {today}

    Database Schema: {schema}
    """
    messages=[
        {"role":"system","content":system_prompt},
        {"role":"user","content":question}
    ]

    response=client.chat.completions.create(
        model="openai/gpt-oss-120b",
        max_tokens=500,
        tools=tools,
        messages=messages
    )

    choice=response.choices[0]

    if choice.finish_reason=="tool_calls":
        tool_call=choice.message.tool_calls[0]
        import json
        query=json.loads(tool_call.function.arguments)["query"]
        print("Executing the SQL Query")

        result=run_sql(query)

        if result["error"]:
            return f"SQL Error:{result["error"]}"
        
        messages.append(choice.message)
        messages.append({
            "role":"tool",
            "tool_call_id":tool_call.id,
            "content":str(result)
        })
        final=client.chat.completions.create(
        model="openai/gpt-oss-120b",
        max_tokens=500,
        messages=messages
        )

        return final.choices[0].message.content
    return choice.message.content


if __name__=="__main__":
    print("Our SQL Agent is ready!!! Go hit your questions. Type 'quit' to exit")

    while True:
        question=input("You:").strip()
        if question.lower()=='quit':
            break
        if not question:
            continue
        answer=ask_query(question)
        print(f"\n Answer:\n{answer}\n")
        print("-"*50)