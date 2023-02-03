FROM public.ecr.aws/lambda/python:3.9
WORKDIR /var/task
COPY . .
RUN pip install -r requirements.txt
CMD ["src.main.main"]