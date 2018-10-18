FROM python
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
CMD ["python", "test.py"]