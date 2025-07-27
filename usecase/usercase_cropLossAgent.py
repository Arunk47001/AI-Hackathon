# importing the libraries
from infra.FM.Text.GoogleVertexText import llm_vertex_cropLoss, llm_vertex_marketComp, llm_vertex_cropSubsidy


def cropLossAgent():
    try:
        response = llm_vertex_cropLoss()
        return response
    except ValueError as err:
        print(err)
        raise ValueError("Error in cropLossAgent")


def cropLossMarketPriceComp():
    try:
        response = llm_vertex_marketComp()
        return response
    except ValueError as err:
        print(err)
        raise ValueError("Error in cropLossMarketPriceComp")
    
def cropLossSubsidy():
    try:
        response = llm_vertex_cropSubsidy()
        return response
    except ValueError as err:
        print(err)
        raise ValueError("Error in cropLossSubsidy")