FROM django
WORKDIR /TODOPROJECT/
COPY . /TODOPROJECT/
RUN pip install -r requirements.txt
CMD [ "python" "manage.py" "runserver" ]