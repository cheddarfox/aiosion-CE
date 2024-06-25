FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml .
RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "aiosion", "/bin/bash", "-c"]

COPY . .

EXPOSE 8000

CMD ["conda", "run", "-n", "aiosion", "python", "src/main.py"]