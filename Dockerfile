FROM gorialis/discord.py:extras

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

COPY . .

CMD ["python", "bot.py"]
