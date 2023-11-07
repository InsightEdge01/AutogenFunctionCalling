from autogen import AssistantAgent, UserProxyAgent
import yfinance as yf


config_list = [
    {
        'api_type': 'open_ai',
        'api_base':'http://localhost:1234/v1',
        'api_key': 'NULL'
    }
]

llm_config = {"config_list": config_list, "seed": 42, "request_timeout": 600,
              "temperature": 0,}


def stock_price(symbol: str) -> float:
    stock = yf.Ticker(symbol)
    price = stock.history(period="id")['Close'].iloc[-1]
    return price

custom_function = [
   {
       "name" : "stock_price",
       "description":"Retrieve the most recent closing price of a stock using its ticker symbol.",
       "parameters":{
           "type":"object",
           "properties":{
               "symbol":{
                   "type":"string",
                   "description":"The ticker symbol of the stock"
               }
            },
            "required":["symbol"]
    } 
}
]

agent_proxy = UserProxyAgent(
    name="DataInsightEdge",
    human_input_mode="ALWAYS",           # NEVER, TERMINATE, or ALWAYS 
                                            # TERMINATE - human input needed when assistant sends TERMINATE 
    max_consecutive_auto_reply=200,
    code_execution_config={
        "work_dir": "agent_output",     # path for file output of program
        "use_docker": False,            # True or image name like "python:3" to use docker image
    },
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
                      Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
    function_map = {"stock_price":stock_price},                 
)

agent_assistant = AssistantAgent(
    name="agent_assistant",
    system_message="""You are an Expert stock trader""",
    llm_config={
        "config_list":config_list,
        "functions":"custom_function",
   }
)

agent_proxy.initiate_chat(
    agent_assistant,
    message="""what is the latest stock price of microsoft as of January 2023.
   """,
)