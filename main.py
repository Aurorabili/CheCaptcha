import random, uvicorn, requests

from urllib.parse import urlparse, urljoin
from fastapi import FastAPI
from lxml import etree

appservice = FastAPI()


@appservice.get("/api")
def AppLoaded():
    return {"code": 200, "data": "Hello!"}


@appservice.get("/api/checaptcha")
def GetcheCaptcha():
    page = random.randint(1, 500)
    rqg = requests.get(f"https://www.inno-chem.com.cn/baike/?p={page}")
    list = etree.HTML(rqg.content).xpath("//div[@class='alink']/a/text()")
    rqg = requests.get(
        f"https://www.inno-chem.com.cn/baike/{list[random.randint(1,len(list))]}.html"
    )
    imgurl = etree.HTML(rqg.content).xpath(
        "//div[@class='section clear']/div/div[@class='base_info']/dl/dt/img/@src"
    )[0]
    imgurl = "https:" + urljoin(imgurl, urlparse(imgurl).path)
    ans = etree.HTML(
        rqg.content).xpath("//div[@class='box goods']/table/tbody/tr/td")[5]

    return {"code": 200, "data": {"imgurl": imgurl, "ans": ans.text}}


if __name__ == '__main__':
    uvicorn.run('main:appservice')
