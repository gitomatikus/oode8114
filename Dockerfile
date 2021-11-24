FROM gorialis/discord.py:extras

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt


RUN mkdir ffmpeg
RUN wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz
RUN tar -C ./ffmpeg -xvf ffmpeg-git-amd64-static.tar.xz --strip-components 1
RUN sudo mv ffmpeg/ffmpeg ffmpeg/ffprobe /usr/local/bin/



COPY . .

CMD ["python", "bot.py"]
