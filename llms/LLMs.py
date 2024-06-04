from llama_index.llms.openai import OpenAI


# OpenAI一套统一的大模型访问接口组件，并不是只能访问GPT
# 下列模型都是兼容OpenAI组件的

def openai_llm(**kwargs):
    llm = OpenAI(
        model="gpt-3.5-turbo-0613",
        api_key="sk-JxLAjLyiAoUAfgFE901c6b823bC84e8bA81042CbA0Bd8178",
        api_base="https://api.xty.app/v1",
        **kwargs
    )
    return llm


def moonshot_llm(**kwargs):
    llm = OpenAI(
        model="moonshot-v1-8k",
        api_key="sk-CoeOW7QSFzoFs66vrDKHSYOfKvIZVoXqAGmw15PyEgEfYbS2",
        api_base="https://api.moonshot.cn/v1",
        **kwargs
    )
    return llm


def deepseek_llm(**kwargs):
    llm = OpenAI(
        model="deepseek-chat",
        api_key="sk-149bf3c0b0e543609274d93ffec44824",
        api_base="https://api.deepseek.com/v1",
        **kwargs
    )
    return llm


def llama3_8B_llm(**kwargs):
    llm = OpenAI(
        model="llama3-8b-8192",
        api_key="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",
        api_base="https://api.groq.com/openai/v1",
        **kwargs
    )
    return llm


def llama3_70B_llm(**kwargs):
    llm = OpenAI(
        model="llama3-70b-8192",
        api_key="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",
        api_base="https://api.groq.com/openai/v1",
        **kwargs
    )
    return llm

# def groq_llama3_8B_llm(**kwargs):
#     llm = Groq(model="llama3-8b-8192",
#                api_key="gsk_23DzHO0lY8Rvm8LhsV2DWGdyb31FY8CsaFigyyaX5Kqs2JsAVlFlO",
#                **kwargs
#                )
#     return llm
#
#
# def groq_llama3_70B_llm(**kwargs):
#     llm = Groq(model="llama3-70b-8192",
#                api_key="gsk_23DzHO0lY8Rvm8LhsV2DWGdyb3F1Y8CsaFigyyaX5Kqs2JsAVlFlO",
#                **kwargs
#                )
#     return llm