# bullseye
bullseye is a customer relationship manager (CRM) designed from the ground up to support special education (SPED) services.

## About bullseye
The software is built on Django 2.0, using postgresql as the database backend, bootstrap 4 combined with React for front-facing UI.

### Recent
* (5/24)
  * Altered id/pk fields for models to use UUIDField rather than IntegerField, altered URL pagination to support UUID based URLs. This should obfuscate the database models such that the information is non-iterable  
  * Reconfigured DB, drop database and create new with permissions
    ```
    (venv) chandler [mysite] psql --username=bullseyeuser --dbname=postgres --password
    Password for user bullseyeuser:
    postgres=> DROP DATABASE bullseye_db;
    DROP DATABASE
    postgres=> CREATE DATABASE bullseye_db;
    CREATE DATABASE
    postgres=> GRANT ALL PRIVILEGES ON DATABASE bullseye_db TO bullseyeuser;
    GRANT
    ```
* (5/21) Configured Notes with GenericForeignKey field using the django built-in contenttype framework  
  * GenericRelation field is then applied to applicable models such as Student and Evaluation, may extend to School/Districts later  
  * Example:  
  ```python
  >>> johnny = Student.objects.get(first_name='Johnny', last_name='Appleseed')
  >>> note = Note(content_object=johnny, title='Note Title', note='This is my note')
  >>> note.save()
  >>> note = Note(content_object=johnny, title='New Note Title', note='This is my new note')
  >>> note.save()
  >>> johnny.notes.all()
  <QuerySet [<Note: Note Title>, <Note: New Note Title>]>
  >>> johnny_eval = Evaluation.objects.get(student=johnny)
  >>> note = Note(content_object=johnny_eval, title='Third note', note='This is my third note!')
  >>> note.save()
  >>> johnny_eval.notes.all()
  <QuerySet [<Note: Third note>]>
  ```  
  * For reverse GenericRelation lookup, apply following syntax:
  ```python
  >>> student_type = ContentType.objects.get_for_model(johnny)
  >>> Note.objects.filter(content_type__pk=student_type.id, object_id=johnny.id)
  <QuerySet [<Note: Note Title>, <Note: New Note Title>]>
  >>> eval_type = ContentType.objects.get_for_model(johnny_eval)
  >>> Note.objects.filter(content_type__pk=eval_type.id, object_id=johnny_eval.id)
  <QuerySet [<Note: Third note>]>
  ```

* (5/15) Designed basic data models  
  * Configured following models:  
    * Districts  
    * Schools  
    * Students  
    * Evaluations  
    * Notes  
  * Installed bullseye app to settings.py following django 2.0 syntax  
  * Setup admin site, added superuser, added additional user (Zach) and registered models with admin.py  

* (5/14) Configured with local postgres DB  
  * username: __bullseyeuser__  
  * password:   
