from flask import Flask
app=Flask(__name__) #__name__目前執行的模組

@app.route("/") #函式的裝飾
def home():
    return "Hello World! 2"

@app.route("/test")
def test():
    return "This is test 2"


if __name__=="__main__": #如果以上程式執行
    app.run() #執行app
