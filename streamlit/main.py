import openai
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient

url = 'mongodb+srv://slugmilk:Kgi57201@cluster0.cjv05dd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(url)
# print(client)

database = client['aiproject']
collection = database['gptai']

openai.api_key = 'sk-proj-I1moSUXA4uQPjm5jyuMIT3BlbkFJdc784TuGvQCrWUkENcIe'

class AdGenerator:
    def __init__(self, engine='gpt-3.5-turbo'):
        self.engine = engine

    def using_chatgpt(self, prompt):
        system_instruction = 'assistant는 마케팅 문구 작성 도우미로 동작한다. user의 내용을 참고하여 마케팅 문구를 작성해라.'
        messages = [{"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}]
        response = openai.chat.completions.create(model=self.engine, messages=messages)
        result = response.choices[0].message.content.strip()
        return result

    def generate(self, product_name, details, tone_and_manner):
        prompt = f'제품 이름: {product_name}\n주요 내용: {details}\n 광고 문구의 스타일: {tone_and_manner} 위 내용을 참고하여 마케팅 문구를 만들어라'
        result = self.using_chatgpt(prompt=prompt)
        return result

app = FastAPI()

class Product(BaseModel):
    product_name: str
    details: str
    tone_and_manner: str

@app.post("/create_ad")
async def create_ad(product: Product):
    # print(product)
    ad_generator = AdGenerator()
    ad = ad_generator.generate(product_name=product.product_name,
                               details=product.product_details,
                               tone_and_manner=product.tone_and_manner)

    data_insert = {'product_name': product.product_name,
                   'details': product.product_details,
                   'tone_and_manner': product.tone_and_manner,
                   'ad': ad}
    result = collection.insert_one(data_insert)
    print(result.inserted_id)

    result = collection.find({})
    datas = []

    for data in result:
        data.pop('_id', None)
        datas.append(data)

    # print(datas)

    return {'ad': ad, 'datas': datas}