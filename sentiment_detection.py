import malaya

class Sentiment_detection:

    def __init__(self):
        self.message = ""

    async def getSentiment(self, message):
        model = malaya.sentiment.multinomial()
        sentiment = model.predict(message, add_neutral = False)
        message = ' '.join(message)

        return await sentiment